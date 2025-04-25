import os
import asyncio
import aiohttp
import json
import xmltodict
import hashlib
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Set

class AsyncNextCloudClient:
    """Lightweight asynchronous NextCloud client for meeting management.
    
    This client focuses on the core functionality needed for the meeting chair
    with native async support.
    """
    
    def __init__(self, 
                 nextcloud_host: str,
                 username: str, 
                 password: str,
                 poll_interval: int = 1):
        """Initialize the async NextCloud client.
        
        Args:
            nextcloud_host: Nextcloud server host URL
            username: Username for authentication
            password: Password for authentication
            poll_interval: Minimum interval between polling operations in seconds
        """
        self.nextcloud_host = nextcloud_host.rstrip('/')
        self.username = username.lower()
        self.password = password
        self.poll_interval = poll_interval
        self.poll_response_cache = {}
        
        # Current meeting info
        self.meeting_id = None
        self.meeting_name = None
        self.last_message_id = None
        
        # Current board info
        self.board_id = None
        self.board_title = None
        self.board_stacks = {}  # Dictionary of stack_id -> stack_title
        
        # Setup for rate limiting and caching
        self.last_chat_poll = 0
        self.last_attendees_poll = 0
        self.last_meeting_state_poll = 0
        self.processed_message_ids: Set[str] = set()
        
        # Create a session for connection pooling
        self._session = None
    
    async def _ensure_session(self):
        """Ensure an aiohttp session exists."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session
    
    async def close(self):
        """Close the aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def _request(self, method: str, url: str, **kwargs) -> Any:
        """Make an HTTP request and handle response parsing.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            url: URL to request
            **kwargs: Additional arguments for the request
            
        Returns:
            Parsed response data
            
        Raises:
            ValueError: If the request fails or the response is invalid
        """
        session = await self._ensure_session()
        
        # Add default headers if not provided
        headers = kwargs.pop('headers', {})
        headers.update({
            "OCS-APIRequest": 'true',
            "Accept": 'application/json'
        })
        
        # Add auth if not provided
        auth = kwargs.pop('auth', None)
        if auth is None:
            if 'Authorization' not in headers:
                auth = aiohttp.BasicAuth(self.username, self.password)
        
        try:
            async with session.request(method, url, headers=headers, auth=auth, **kwargs) as response:
                # Check status code
                if response.status >= 400:
                    error_text = await response.text()
                    raise ValueError(f"Request failed with status {response.status}: {error_text}")
                
                # Get content
                content = await response.read()
                
                # Check if response is empty
                if not content or content.isspace():
                    return {}
                
                # Try to parse as JSON first
                if content.strip().startswith(b'{'):
                    data = json.loads(content)
                    
                    # Handle OCS response format
                    if 'ocs' in data:
                        status = data.get('ocs', {}).get('meta', {}).get('status', '').lower()
                        if status != 'ok':
                            error_msg = data.get('ocs', {}).get('meta', {}).get('message', 'Unknown error')
                            raise ValueError(f"API error: {error_msg}")
                        
                        # Return the data part of the response
                        return data.get('ocs', {}).get('data', {})
                    
                    # Direct JSON response
                    return data
                
                # Fall back to XML parsing
                try:
                    data = xmltodict.parse(content)
                    
                    # Handle OCS response format
                    if 'ocs' in data:
                        if data.get('ocs', {}).get('meta', {}).get('status') != 'OK':
                            error_msg = data.get('ocs', {}).get('meta', {}).get('message', 'Unknown error')
                            raise ValueError(f"API error: {error_msg}")
                        
                        # Return the data part of the response
                        return data.get('ocs', {}).get('data', {})
                    
                    # Direct XML response
                    return data
                except Exception as xml_error:
                    error_details = f"Response content: {content[:100]}..."
                    raise ValueError(f"Failed to parse response: {str(xml_error)}. {error_details}")
                
        except aiohttp.ClientError as e:
            raise ValueError(f"Request error: {str(e)}")
    
    async def create_or_join_meeting(self, meeting_info: Dict[str, Any]) -> str:
        """Create or join a NextCloud meeting.
        
        Args:
            meeting_info: Dictionary with meeting details including 'name'
            
        Returns:
            Meeting ID/token
            
        Raises:
            ValueError: If the request fails or the response is invalid
        """
        # Check if we already have a meeting ID
        
        if self.meeting_id:
            # Verify if meeting still exists
            try:
                await self._request('GET', f"{self.nextcloud_host}/ocs/v2.php/apps/spreed/api/v4/room/{self.meeting_id}")
                return self.meeting_id
            except ValueError:
                # Meeting doesn't exist, create a new one
                pass
        
        # Create a new meeting
        meeting_name = meeting_info.get('name', 'New Meeting')
        data = {
            "roomType": 2,  # ROOM_TYPE_SHARED
            "roomName": meeting_name
        }
        
        # Use form data, not JSON
        result = await self._request('POST', f"{self.nextcloud_host}/ocs/v2.php/apps/spreed/api/v4/room", data=data)
        
        # Extract meeting token
        token = result.get('token')
        if not token:
            raise ValueError(f"Failed to get meeting token from response: {result}")
        
        # Save meeting info
        self.meeting_id = token
        self.meeting_name = meeting_name
        
        return token
    
    async def add_message(self, message: str, participant_username: Optional[str] = None, participant_password: Optional[str] = None) -> bool:
        """Add a message to the meeting chat.
        
        Args:
            message: Message text
            participant_username: Username of the sender (defaults to client user)
            participant_password: Password of the sender (defaults to client password)
            
        Returns:
            Success status
            
        Raises:
            ValueError: If the meeting ID is not set or the request fails
        """
        if not self.meeting_id:
            raise ValueError("Meeting ID not set. Call create_or_join_meeting first.")
        
        # Set up data
        data = {"message": message}
        
        # Set up auth
        if participant_username and participant_password:
            auth = aiohttp.BasicAuth(participant_username, participant_password)
        else:
            auth = aiohttp.BasicAuth(self.username, self.password)
        
        # Make the request
        url = f"{self.nextcloud_host}/ocs/v2.php/apps/spreed/api/v1/chat/{self.meeting_id}"
        try:
            await self._request('POST', url, data=data, auth=auth)
            return True
        except ValueError:
            return False
    
    async def add_rich_message(self, message: str, content_type: str = "markdown", 
                              participant_username: Optional[str] = None, 
                              participant_password: Optional[str] = None) -> bool:
        """Add a rich-formatted message to the meeting chat.
        
        Args:
            message: Message content
            content_type: Content type (defaults to "markdown")
            participant_username: Username of the sender (defaults to client user)
            participant_password: Password of the sender (defaults to client password)
            
        Returns:
            Success status
            
        Raises:
            ValueError: If the meeting ID is not set or the request fails
        """
        # For markdown messages, use regular message API
        if content_type == "markdown":
            return await self.add_message(message, participant_username, participant_password)
        
        if not self.meeting_id:
            raise ValueError("Meeting ID not set. Call create_or_join_meeting first.")
        
        # Generate a hash for the message
        message_hash = hashlib.md5(f"{message}-{datetime.now().isoformat()}".encode()).hexdigest()
        
        # Set up data
        message_data = {
            "objectType": content_type,
            "objectId": message_hash,
            "metaData": {
                "content": message
            }
        }
        
        # Set up auth
        if participant_username and participant_password:
            auth = aiohttp.BasicAuth(participant_username, participant_password)
        else:
            auth = aiohttp.BasicAuth(self.username, self.password)
        
        # Set up headers
        headers = {
            "OCS-APIRequest": 'true',
            "Accept": 'application/json',
            "Content-Type": 'application/json'
        }
        
        # Make the request
        url = f"{self.nextcloud_host}/ocs/v2.php/apps/spreed/api/v1/chat/{self.meeting_id}/share"
        try:
            await self._request('POST', url, json=message_data, headers=headers, auth=auth)
            return True
        except ValueError:
            return False
    
    async def get_chat_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get chat history from the meeting.
        
        Args:
            limit: Maximum number of messages to retrieve
            
        Returns:
            List of message dictionaries
            
        Raises:
            ValueError: If the meeting ID is not set or the request fails
        """
        # Check if we've polled within the interval
        current_time = time.time()
        
        # Enforce minimum poll interval to prevent too many requests
        if current_time - self.last_chat_poll < self.poll_interval:
            return self.poll_response_cache
        
        # Update last poll time
        self.last_chat_poll = current_time
        
        # Simple request for recent messages
        params = {
            'lookIntoFuture': 1,  # We want past messages
            'timeout': 1,         # poll for onl 1 second
            'limit': limit,       # Maximum number of messages
            'lastKnownMessageId': str(self.last_message_id)
           }
        
        # Make the request
        url = f"{self.nextcloud_host}/ocs/v2.php/apps/spreed/api/v1/chat/{self.meeting_id}"
        headers = {
            "Accept": "application/json",  # Ensure we get JSON responses
        }
        
        result = await self._request('GET', url, params=params, headers=headers)
        
        # Process the result
        messages = result if isinstance(result, list) else []
        print(f"Client got {len(messages)} messages")
        self.poll_response_cache = messages
        return messages

    async def process_new_messages(self) -> List[Dict[str, Any]]:
        """Process new messages from NextCloud.
        
        Returns:
            List of new messages that haven't been processed yet
        """
        try:
            # Get all recent messages
            all_messages = await self.get_chat_history()
            # Find which messages are new
            new_messages = []
            for message in all_messages:
                message_id = str(message.get('id'))
                print(f"Processing message {message_id}")
                # Skip messages we've already processed
                if message_id in self.processed_message_ids:
                    continue
                
                # Add to processed set
                self.processed_message_ids.add(message_id)
                self.last_message_id = message_id
                
                # Format the message for chat history
                entry = {
                    "sender": message.get('actorDisplayName', 'Unknown'),
                    "content": message.get('message', ''),
                    "timestamp": str(message.get('timestamp', 0)),
                    "id": message_id
                }
                
                # Add to new messages
                new_messages.append(entry)
            
            print(f"Found {len(new_messages)} new messages")
            return new_messages
            
        except Exception as e:
            print(f"Error processing new messages: {str(e)}")
            return []
            
    async def check_for_new_messages(self) -> bool:
        """Check for new messages.
        
        Returns:
            True if new messages were found, False otherwise
        """
        # Get recent messages
        all_messages = await self.get_chat_history()
        
        # Check if any message has not been processed yet
        for message in all_messages:
            message_id = str(message.get('id', ''))
            if message_id not in self.processed_message_ids:
                return True
        
        return False
    
    async def get_participants(self) -> List[Dict[str, Any]]:
        """Get participants in the meeting.
        
        Returns:
            List of participant dictionaries
            
        Raises:
            ValueError: If the meeting ID is not set or the request fails
        """
        # Check if we've polled within the interval
        current_time = time.time()
        if current_time - self.last_attendees_poll < self.poll_interval:
            return []
        
        # Update last poll time
        self.last_attendees_poll = current_time
        
        if not self.meeting_id:
            raise ValueError("Meeting ID not set. Call create_or_join_meeting first.")
        
        # Make the request
        url = f"{self.nextcloud_host}/ocs/v2.php/apps/spreed/api/v4/room/{self.meeting_id}/participants?includeStatus=true"
        result = await self._request('GET', url)
        
        # Process the result
        if isinstance(result, dict):
            return [result]
        elif isinstance(result, list):
            return result
        else:
            return []
    
    async def get_attendees(self) -> List[Dict[str, Any]]:
        """Get active attendees in the meeting.
        
        Returns:
            List of attendee dictionaries (participants with active sessions)
            
        Raises:
            ValueError: If the meeting ID is not set or the request fails
        """
        # Get all participants
        all_participants = await self.get_participants()
        
        # Filter to only include participants who are in the call
        attendees = [
            participant for participant in all_participants 
            if len(participant.get('sessionIds', [])) > 0
        ]
        
        return attendees
    
    async def add_participant(self, username: str) -> bool:
        """Add a participant to the meeting.
        
        Args:
            username: Username of the participant to add
            
        Returns:
            Success status
            
        Raises:
            ValueError: If the meeting ID is not set or the request fails
        """
        if not self.meeting_id:
            raise ValueError("Meeting ID not set. Call create_or_join_meeting first.")
        
        # Make the request to add participant
        url = f"{self.nextcloud_host}/ocs/v2.php/apps/spreed/api/v4/room/{self.meeting_id}/participants"
        data = {
            "newParticipant": username,
            "source": "users"
        }
        
        try:
            # Use form data, not JSON
            await self._request('POST', url, data=data)
            return True
        except ValueError as e:
            print(f"Error adding participant {username}: {e}")
            return False
    
    async def get_meeting_state(self) -> Dict[str, Any]:
        """Get the current meeting state.
        
        Returns:
            Dictionary with meeting details
            
        Raises:
            ValueError: If the meeting ID is not set or the request fails
        """
        # Check if we've polled within the interval
        current_time = time.time()
        if current_time - self.last_meeting_state_poll < self.poll_interval:
            return {}
        
        # Update last poll time
        self.last_meeting_state_poll = current_time
        
        if not self.meeting_id:
            raise ValueError("Meeting ID not set. Call create_or_join_meeting first.")
        
        # Make the request
        url = f"{self.nextcloud_host}/ocs/v2.php/apps/spreed/api/v4/room/{self.meeting_id}"
        return await self._request('GET', url)

    async def create_poll(self, question: str, options: List[str], max_votes: int = 1, result_mode: str = "public") -> Dict[str, Any]:
        """Create a poll in a Nextcloud meeting chat.
        
        Args:
            question: The poll question
            options: List of poll options/choices
            max_votes: Maximum number of options a user can vote for (default: 1)
            result_mode: Visibility of results, either "public" or "hidden" (default: "public")
            
        Returns:
            Dictionary containing poll details including the poll ID
            
        Raises:
            ValueError: If the meeting ID is not set or the request fails
        """
        if not self.meeting_id:
            raise ValueError("Meeting ID not set. Call create_or_join_meeting first.")
            
        # Validate inputs
        if not question:
            raise ValueError("Poll question is required")
        if not options or len(options) < 2:
            raise ValueError("At least 2 poll options are required")
        if max_votes < 1:
            raise ValueError("max_votes must be at least 1")
        if result_mode not in ["public", "hidden"]:
            raise ValueError("result_mode must be either 'public' or 'hidden'")
            
        # Prepare poll data
        poll_data = {
            "question": question,
            "options": options,
            "maxVotes": max_votes,
            "resultMode": result_mode
        }
        
        # Set up headers
        headers = {
            "Content-Type": 'application/json'
        }
        
        # Make the request
        url = f"{self.nextcloud_host}/ocs/v2.php/apps/spreed/api/v1/poll/{self.meeting_id}"
        
        try:
            # Use JSON data for this endpoint
            return await self._request('POST', url, json=poll_data, headers=headers)
        except ValueError as e:
            raise ValueError(f"Failed to create poll: {str(e)}")

    async def vote_on_poll(self, poll_id: str, option_ids: List[int]) -> Dict[str, Any]:
        """Vote on an existing poll in a Nextcloud meeting.
        
        Args:
            poll_id: ID of the poll to vote on
            option_ids: List of option IDs to vote for (indexes of the options, typically starting from 0)
            
        Returns:
            Dictionary containing the result of the vote operation
            
        Raises:
            ValueError: If the meeting ID is not set, the poll ID is not found, or the request fails
        """
        if not self.meeting_id:
            raise ValueError("Meeting ID not set. Call create_or_join_meeting first.")
            
        # Validate inputs
        if not poll_id:
            raise ValueError("Poll ID is required")
            
        # Handle case where a single option (string or int) is provided instead of a list
        if not isinstance(option_ids, list):
            if isinstance(option_ids, (str, int)):
                # Get poll details to find index of the option
                try:
                    poll_details = await self.get_poll_results(str(poll_id))
                    options = poll_details.get("options", [])
                    if option_ids in options:
                        option_ids = [options.index(option_ids)]
                    else:
                        # If not found, assume it might be an index passed as string
                        try:
                            option_ids = [int(option_ids)]
                        except ValueError:
                            raise ValueError(f"Option '{option_ids}' not found in poll options")
                except ValueError:
                    # If poll details can't be retrieved, assume it's an index passed as string
                    try:
                        option_ids = [int(option_ids)]
                    except ValueError:
                        raise ValueError("Option IDs must be integers or valid option strings")
            else:
                raise ValueError("option_ids must be a list of integers, a single integer, or option text")
        
        # Convert any remaining string values to integers if needed
        processed_option_ids = []
        for opt_id in option_ids:
            if isinstance(opt_id, int):
                processed_option_ids.append(opt_id)
            else:
                try:
                    processed_option_ids.append(int(opt_id))
                except ValueError:
                    raise ValueError(f"Invalid option ID: {opt_id}. Must be an integer or convertible to integer.")
        
        # Prepare vote data
        vote_data = {
            "optionIds": processed_option_ids
        }
        
        # Set up headers
        headers = {
            "Content-Type": 'application/json'
        }
        
        # Make the request
        url = f"{self.nextcloud_host}/ocs/v2.php/apps/spreed/api/v1/poll/{self.meeting_id}/{poll_id}"
        
        try:
            # Use JSON data for this endpoint
            return await self._request('POST', url, json=vote_data, headers=headers)
        except ValueError as e:
            raise ValueError(f"Failed to vote on poll: {str(e)}")

    async def get_poll_results(self, poll_id: str) -> Dict[str, Any]:
        """Get the results of a poll in a Nextcloud meeting.
        
        Args:
            poll_id: ID of the poll to get results for
            
        Returns:
            Dictionary containing poll results including vote counts and option details.
            Note: The 'votes' field might be empty if:
            1. No one has voted yet
            2. The poll has resultMode = "hidden" (0) and you're not the poll creator
            3. The poll hasn't been closed yet
            
        Raises:
            ValueError: If the meeting ID is not set, the poll ID is not found, or the request fails
        """
        if not self.meeting_id:
            raise ValueError("Meeting ID not set. Call create_or_join_meeting first.")
            
        # Validate inputs
        if not poll_id:
            raise ValueError("Poll ID is required")
            
        # Make the request
        url = f"{self.nextcloud_host}/ocs/v2.php/apps/spreed/api/v1/poll/{self.meeting_id}/{poll_id}"
        
        try:
            return await self._request('GET', url)
        except ValueError as e:
            raise ValueError(f"Failed to get poll results: {str(e)}")

    async def close_poll(self, poll_id: str) -> bool:
        """Close a poll in a Nextcloud meeting.
        
        Args:
            poll_id: ID of the poll to close
            
        Returns:
            Boolean indicating success
            
        Raises:
            ValueError: If the meeting ID is not set, the poll ID is not found, or the request fails
        """
        if not self.meeting_id:
            raise ValueError("Meeting ID not set. Call create_or_join_meeting first.")
            
        # Validate inputs
        if not poll_id:
            raise ValueError("Poll ID is required")
            
        # Make the request (DELETE method to close the poll)
        url = f"{self.nextcloud_host}/ocs/v2.php/apps/spreed/api/v1/poll/{self.meeting_id}/{poll_id}"
        
        try:
            await self._request('DELETE', url)
            return True
        except ValueError:
            return False

    async def share_calendar_event(self, calendar_id: str, event_id: str) -> bool:
        """Share a calendar event in the meeting chat.
        
        Args:
            calendar_id: ID of the calendar containing the event
            event_id: ID of the event to share
            
        Returns:
            Boolean indicating success
            
        Raises:
            ValueError: If the meeting ID is not set or the request fails
        """
        if not self.meeting_id:
            raise ValueError("Meeting ID not set. Call create_or_join_meeting first.")
            
        # Generate a unique ID for this rich object
        object_id = hashlib.md5(f"calendar-{calendar_id}-{event_id}-{datetime.now().isoformat()}".encode()).hexdigest()
        
        # Set up the rich object data
        rich_object = {
            "objectType": "calendar-event", 
            "objectId": object_id,
            "metaData": {
                "id": event_id,
                "calendarId": calendar_id
            }
        }
        
        # Set up headers
        headers = {
            "Content-Type": 'application/json'
        }
        
        # Make the request
        url = f"{self.nextcloud_host}/ocs/v2.php/apps/spreed/api/v1/chat/{self.meeting_id}/share"
        
        try:
            await self._request('POST', url, json=rich_object, headers=headers)
            return True
        except ValueError as e:
            raise ValueError(f"Failed to share calendar event: {str(e)}")
            
    async def share_file_reference(self, file_id: str, path: str, name: Optional[str] = None) -> bool:
        """Share a reference to a file in the meeting chat.
        
        Args:
            file_id: ID of the file to share
            path: Path to the file in Nextcloud
            name: Optional display name for the file (defaults to filename)
            
        Returns:
            Boolean indicating success
            
        Raises:
            ValueError: If the meeting ID is not set or the request fails
        """
        if not self.meeting_id:
            raise ValueError("Meeting ID not set. Call create_or_join_meeting first.")
            
        # Extract filename from path if name not provided
        if not name:
            name = path.split('/')[-1]
            
        # Generate a unique ID for this rich object
        object_id = hashlib.md5(f"file-{file_id}-{datetime.now().isoformat()}".encode()).hexdigest()
        
        # Set up the rich object data
        rich_object = {
            "objectType": "file",
            "objectId": object_id,
            "metaData": {
                "id": file_id,
                "name": name,
                "path": path
            }
        }
        
        # Set up headers
        headers = {
            "Content-Type": 'application/json'
        }
        
        # Make the request
        url = f"{self.nextcloud_host}/ocs/v2.php/apps/spreed/api/v1/chat/{self.meeting_id}/share"
        
        try:
            await self._request('POST', url, json=rich_object, headers=headers)
            return True
        except ValueError as e:
            raise ValueError(f"Failed to share file reference: {str(e)}")
            
    async def share_deck_card(self, board_id: str, stack_id: str, card_id: str) -> bool:
        """Share a Deck card in the meeting chat.
        
        Args:
            board_id: ID of the Deck board
            stack_id: ID of the stack containing the card
            card_id: ID of the card to share
            
        Returns:
            Boolean indicating success
            
        Raises:
            ValueError: If the meeting ID is not set or the request fails
        """
        if not self.meeting_id:
            raise ValueError("Meeting ID not set. Call create_or_join_meeting first.")
            
        # Generate a unique ID for this rich object
        object_id = hashlib.md5(f"deck-card-{board_id}-{stack_id}-{card_id}-{datetime.now().isoformat()}".encode()).hexdigest()
        
        # Set up the rich object data
        rich_object = {
            "objectType": "deck-card",
            "objectId": object_id,
            "metaData": {
                "id": card_id,
                "boardId": board_id,
                "stackId": stack_id
            }
        }
        
        # Set up headers
        headers = {
            "Content-Type": 'application/json'
        }
        
        # Make the request
        url = f"{self.nextcloud_host}/ocs/v2.php/apps/spreed/api/v1/chat/{self.meeting_id}/share"
        
        try:
            await self._request('POST', url, json=rich_object, headers=headers)
            return True
        except ValueError as e:
            raise ValueError(f"Failed to share deck card: {str(e)}")
            
    async def create_and_share_location(self, name: str, latitude: float, longitude: float, address: Optional[str] = None) -> bool:
        """Share a location in the meeting chat.
        
        Args:
            name: Name of the location
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            address: Optional address text
            
        Returns:
            Boolean indicating success
            
        Raises:
            ValueError: If the meeting ID is not set or the request fails
        """
        if not self.meeting_id:
            raise ValueError("Meeting ID not set. Call create_or_join_meeting first.")
            
        # Generate a unique ID for this rich object
        object_id = hashlib.md5(f"geo-location-{latitude}-{longitude}-{datetime.now().isoformat()}".encode()).hexdigest()
        
        # Set up the rich object data
        location_data = {
            "objectType": "geo-location",
            "objectId": object_id,
            "metaData": {
                "name": name,
                "latitude": latitude,
                "longitude": longitude
            }
        }
        
        # Add address if provided
        if address:
            location_data["metaData"]["address"] = address
            
        # Set up headers
        headers = {
            "Content-Type": 'application/json'
        }
        
        # Make the request
        url = f"{self.nextcloud_host}/ocs/v2.php/apps/spreed/api/v1/chat/{self.meeting_id}/share"
        
        try:
            await self._request('POST', url, json=location_data, headers=headers)
            return True
        except ValueError as e:
            raise ValueError(f"Failed to share location: {str(e)}")

    # ---------- Deck Board Operations ----------
    
    async def is_deck_available(self) -> bool:
        """Check if the Deck app is available on this Nextcloud instance.
        
        Returns:
            Boolean indicating whether the Deck app is available
        """
        # Use the standard Deck API endpoint
        url = f"{self.nextcloud_host}/index.php/apps/deck/api/v1.0/boards"
        
        # Set up headers as specified in the docs
        headers = {
            "OCS-APIRequest": "true"
        }
        
        try:
            # Just make a HEAD request to check if the endpoint exists
            session = await self._ensure_session()
            async with session.head(url, auth=aiohttp.BasicAuth(self.username, self.password), headers=headers) as response:
                return response.status < 400
        except Exception as e:
            print(f"Deck app appears to be unavailable: {str(e)}")
            return False
        
    async def get_deck_boards(self) -> List[Dict[str, Any]]:
        """Get all accessible Deck boards.
        
        Returns:
            List of deck board dictionaries
            
        Raises:
            ValueError: If the request fails
        """
        # Set up API endpoint
        url = f"{self.nextcloud_host}/index.php/apps/deck/api/v1.0/boards"
        
        # Set up headers as specified in the docs
        headers = {
            "Content-Type": "application/json",
            "OCS-APIRequest": "true"
        }
        
        try:
            # Handle the response directly to avoid JSON parsing issues
            session = await self._ensure_session()
            async with session.get(
                url, 
                auth=aiohttp.BasicAuth(self.username, self.password),
                headers=headers
            ) as response:
                if response.status >= 400:
                    raise ValueError(f"Request failed with status {response.status}: {await response.text()}")
                
                # Get text response and parse it
                text = await response.text()
                if not text.strip():
                    return []
                    
                try:
                    return json.loads(text)
                except json.JSONDecodeError as e:
                    print(f"Failed to parse response: {str(e)}. Response content: {text[:100]}...")
                    return []
        except Exception as e:
            print(f"Failed to get deck boards: {str(e)}")
            return []
            
    async def get_board_details(self, board_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific Deck board.
        
        Args:
            board_id: ID of the board to retrieve
            
        Returns:
            Dictionary containing board details
            
        Raises:
            ValueError: If the request fails
        """
        # Set up API endpoint
        url = f"{self.nextcloud_host}/index.php/apps/deck/api/v1.0/boards/{board_id}"
        
        # Set up headers as specified in the docs
        headers = {
            "Content-Type": "application/json",
            "OCS-APIRequest": "true"
        }
        
        try:
            return await self._request('GET', url, headers=headers)
        except ValueError as e:
            raise ValueError(f"Failed to get board details: {str(e)}")
    
    async def create_deck_board(self, title: str, color: str = "0082c9") -> Dict[str, Any]:
        """Create a new Deck board.
        
        Args:
            title: Title of the board
            color: Color of the board in hex format (default: Nextcloud blue)
            
        Returns:
            Dictionary containing new board details
            
        Raises:
            ValueError: If the request fails
        """
        # Validate inputs
        if not title:
            raise ValueError("Board title is required")
            
        # Set up the request data
        board_data = {
            "title": title,
            "color": color
        }
        
        # Set up headers
        headers = {
            "Content-Type": "application/json",
            "OCS-APIRequest": "true"
        }
        
        # Make the request
        url = f"{self.nextcloud_host}/index.php/apps/deck/api/v1.0/boards"
        
        try:
            result = await self._request('POST', url, json=board_data, headers=headers)
            
            # Cache the board details
            if result and 'id' in result:
                self.board_id = result['id']
                self.board_title = title
                
            return result
        except ValueError as e:
            raise ValueError(f"Failed to create deck board: {str(e)}")
    
    async def get_board_stacks(self, board_id: str) -> List[Dict[str, Any]]:
        """Get stacks in a Deck board.
        
        Args:
            board_id: ID of the board
            
        Returns:
            List of stack dictionaries
            
        Raises:
            ValueError: If the request fails
        """
        # Set up API endpoint
        url = f"{self.nextcloud_host}/index.php/apps/deck/api/v1.0/boards/{board_id}/stacks"
        
        # Set up headers as specified in the docs
        headers = {
            "Content-Type": "application/json",
            "OCS-APIRequest": "true"
        }
        
        try:
            result = await self._request('GET', url, headers=headers)
            
            # Cache the stacks if this is our current board
            if board_id == self.board_id and isinstance(result, list):
                self.board_stacks = {}
                for stack in result:
                    if 'id' in stack and 'title' in stack:
                        self.board_stacks[stack['id']] = stack['title']
            
            if isinstance(result, list):
                return result
            return []
        except ValueError as e:
            print(f"Failed to get board stacks: {str(e)}")
            return []
    
    async def create_stack(self, board_id: str, title: str, order: int = 0) -> Dict[str, Any]:
        """Create a new stack in a Deck board.
        
        Args:
            board_id: ID of the board
            title: Title of the stack
            order: Order/position of the stack (default: 0)
            
        Returns:
            Dictionary containing new stack details
            
        Raises:
            ValueError: If the request fails
        """
        # Validate inputs
        if not board_id:
            raise ValueError("Board ID is required")
        if not title:
            raise ValueError("Stack title is required")
            
        # Set up the request data
        stack_data = {
            "title": title,
            "order": order
        }
        
        # Set up headers
        headers = {
            "Content-Type": "application/json",
            "OCS-APIRequest": "true"
        }
        
        # Make the request
        url = f"{self.nextcloud_host}/index.php/apps/deck/api/v1.0/boards/{board_id}/stacks"
        
        try:
            result = await self._request('POST', url, json=stack_data, headers=headers)
            
            # Cache the stack details if this is for our cached board
            if board_id == self.board_id and result and 'id' in result:
                self.board_stacks[result['id']] = result['title']
                
            return result
        except ValueError as e:
            raise ValueError(f"Failed to create stack: {str(e)}")
    
    async def get_stack_cards(self, board_id: str, stack_id: str) -> List[Dict[str, Any]]:
        """Get cards in a stack.
        
        Args:
            board_id: ID of the board
            stack_id: ID of the stack
            
        Returns:
            List of card dictionaries
            
        Raises:
            ValueError: If the request fails
        """
        # Check if Deck app is available first
        if not await self.is_deck_available():
            print("Deck app is not available on this Nextcloud instance")
            return []
            
        # Set up API endpoint
        url = f"{self.nextcloud_host}/index.php/apps/deck/api/v1.0/boards/{board_id}/stacks/{stack_id}/cards"
        
        # Set up headers as specified in the docs
        headers = {
            "Content-Type": "application/json",
            "OCS-APIRequest": "true"
        }
        
        try:
            result = await self._request('GET', url, headers=headers)
            if isinstance(result, list):
                return result
            return []
        except ValueError as e:
            print(f"Failed to get stack cards: {str(e)}")
            return []
    
    async def create_card(self, board_id: str, stack_id: str, title: str, description: str = "", 
                          due_date: Optional[str] = None, labels: Optional[List[int]] = None) -> Dict[str, Any]:
        """Create a new card in a stack.
        
        Args:
            board_id: ID of the board
            stack_id: ID of the stack
            title: Title of the card
            description: Description of the card (default: empty)
            due_date: Due date in ISO format (default: None)
            labels: List of label IDs to assign to the card (default: None)
            
        Returns:
            Dictionary containing new card details
            
        Raises:
            ValueError: If the request fails
        """
        # Check if Deck app is available first
        if not await self.is_deck_available():
            raise ValueError("Deck app is not available on this Nextcloud instance")
            
        # Validate inputs
        if not board_id:
            raise ValueError("Board ID is required")
        if not stack_id:
            raise ValueError("Stack ID is required")
        if not title:
            raise ValueError("Card title is required")
            
        # Set up the request data according to API docs
        card_data = {
            "title": title,
            "description": description,
            "type": "plain"  # Use plain text as default format
        }
        
        # Add optional fields if provided
        if due_date:
            card_data["duedate"] = due_date
        if labels:
            card_data["labels"] = labels
            
        # Set up headers as specified in the docs
        headers = {
            "Content-Type": "application/json",
            "OCS-APIRequest": "true"
        }
        
        # Make the request
        url = f"{self.nextcloud_host}/index.php/apps/deck/api/v1.0/boards/{board_id}/stacks/{stack_id}/cards"
        
        try:
            return await self._request('POST', url, json=card_data, headers=headers)
        except ValueError as e:
            raise ValueError(f"Failed to create card: {str(e)}")            
    
    async def create_action_item_card(self, title: str, description: str, assignee: Optional[str] = None, 
                                      due_date: Optional[str] = None) -> Dict[str, Any]:
        """Create an action item as a card in a Deck board.
        
        This is a convenience method that creates a special "Action Items" board and stack
        if they don't exist yet, and then creates a card for the action item.
        
        Args:
            title: Title of the action item
            description: Description of the action item
            assignee: Username of the person assigned to the action item (default: None)
            due_date: Due date in ISO format (default: None)
            
        Returns:
            Dictionary containing new card details
            
        Raises:
            ValueError: If the request fails
        """
        # Validate inputs
        if not title:
            raise ValueError("Action item title is required")
        if not description:
            raise ValueError("Action item description is required")
            
        # Get or create the Action Items board
        board_id = await self._get_or_create_action_items_board()
        
        # Get or create the To Do stack
        stack_id = await self._get_or_create_todo_stack(board_id)
        
        # Create the card
        card = await self.create_card(
            board_id=board_id,
            stack_id=stack_id,
            title=title,
            description=description,
            due_date=due_date
        )
        
        # If assignee is provided, assign the card to them
        if assignee and "id" in card:
            await self._assign_card(board_id, stack_id, card["id"], assignee)
            
        # Share the board with all meeting participants if it's not already shared
        await self._share_board_with_participants(board_id)
            
        return card
    
    async def _get_or_create_action_items_board(self) -> str:
        """Get or create the Action Items board.
        
        Returns:
            ID of the Action Items board
        """
        # Check for existing Action Items board
        boards = await self.get_deck_boards()
        
        for board in boards:
            if board.get("title") == "Action Items":
                return str(board.get("id"))
                
        # If no existing board, create one
        try:
            board = await self.create_deck_board(title="Action Items", color="0082c9")
            return str(board.get("id"))
        except ValueError:
            # If API fails, try a second time with explicit handling
            print("Failed to create Action Items board on first attempt, trying again...")
            try:
                # Make the request directly with explicit headers
                url = f"{self.nextcloud_host}/index.php/apps/deck/api/v1.0/boards"
                
                headers = {
                    "Content-Type": "application/json",
                    "OCS-APIRequest": "true"
                }
                
                board_data = {
                    "title": "Action Items",
                    "color": "0082c9"
                }
                
                session = await self._ensure_session()
                async with session.post(
                    url, 
                    json=board_data, 
                    auth=aiohttp.BasicAuth(self.username, self.password),
                    headers=headers
                ) as response:
                    if response.status >= 400:
                        print(f"Failed to create Action Items board: {response.status}")
                        raise ValueError(f"Failed to create Action Items board: {response.status}")
                    board = await response.json()
                    return str(board.get("id"))
            except Exception as e:
                print(f"Failed to create Action Items board: {str(e)}")
                raise ValueError(f"Failed to create Action Items board: {str(e)}")
    
    async def _get_or_create_todo_stack(self, board_id: str) -> str:
        """Get or create the To Do stack in the specified board.
        
        Args:
            board_id: ID of the board
            
        Returns:
            ID of the To Do stack
        """
        # Check for existing To Do stack
        stacks = await self.get_board_stacks(board_id)
        
        for stack in stacks:
            if stack.get("title") == "To Do":
                return str(stack.get("id"))
                
        # If no existing stack, create one
        try:
            stack = await self.create_stack(board_id=board_id, title="To Do", order=0)
            return str(stack.get("id"))
        except ValueError:
            # If API fails, try a second time with explicit handling
            print("Failed to create To Do stack on first attempt, trying again...")
            try:
                # Make the request directly with explicit headers
                url = f"{self.nextcloud_host}/index.php/apps/deck/api/v1.0/boards/{board_id}/stacks"
                
                headers = {
                    "Content-Type": "application/json",
                    "OCS-APIRequest": "true"
                }
                
                stack_data = {
                    "title": "To Do",
                    "order": 0
                }
                
                session = await self._ensure_session()
                async with session.post(
                    url, 
                    json=stack_data, 
                    auth=aiohttp.BasicAuth(self.username, self.password),
                    headers=headers
                ) as response:
                    if response.status >= 400:
                        print(f"Failed to create To Do stack: {response.status}")
                        raise ValueError(f"Failed to create To Do stack: {response.status}")
                    stack = await response.json()
                    return str(stack.get("id"))
            except Exception as e:
                print(f"Failed to create To Do stack: {str(e)}")
                raise ValueError(f"Failed to create To Do stack: {str(e)}")
                
    async def _assign_card(self, board_id: str, stack_id: str, card_id: str, user_id: str) -> None:
        """Assign a card to a user.
        
        Args:
            board_id: ID of the board
            stack_id: ID of the stack
            card_id: ID of the card
            user_id: ID of the user to assign the card to
            
        Raises:
            ValueError: If the request fails
        """
        # Set up API endpoint
        url = f"{self.nextcloud_host}/index.php/apps/deck/api/v1.0/boards/{board_id}/stacks/{stack_id}/cards/{card_id}/assignUser"
        
        # Set up headers
        headers = {
            "Content-Type": "application/json",
            "OCS-APIRequest": "true"
        }
        
        # Set up data
        data = {
            "userId": user_id
        }
        
        try:
            await self._request('PUT', url, json=data, headers=headers)
        except ValueError as e:
            print(f"Failed to assign card: {str(e)}")
    
    async def _share_board_with_participants(self, board_id: str) -> None:
        """Share a board with all meeting participants.
        
        Args:
            board_id: ID of the board
            
        Raises:
            ValueError: If the request fails
        """
        # Get participants
        try:
            participants = await self.get_participants()
        except ValueError as e:
            print(f"Failed to get participants: {str(e)}")
            return
            
        for participant in participants:
            user_id = participant.get("userId")
            if user_id and user_id != self.username:  # Don't share with self
                await self._share_board_with_user(board_id, user_id)
    
    async def _share_board_with_user(self, board_id: str, user_id: str, permission: int = 3) -> None:
        """Share a board with a user.
        
        Args:
            board_id: ID of the board
            user_id: ID of the user to share with
            permission: Permission level (default: 3 = read/write)
                1 = read
                2 = edit
                3 = manage
                4 = manage + share
                
        Raises:
            ValueError: If the request fails
        """
        # Set up API endpoint
        url = f"{self.nextcloud_host}/index.php/apps/deck/api/v1.0/boards/{board_id}/acl"
        
        # Set up headers
        headers = {
            "Content-Type": "application/json",
            "OCS-APIRequest": "true"
        }
        
        # Set up data
        data = {
            "type": 0,  # 0 = user
            "participant": user_id,
            "permissionEdit": permission >= 2,
            "permissionShare": permission >= 4,
            "permissionManage": permission >= 3
        }
        
        try:
            await self._request('POST', url, json=data, headers=headers)
        except ValueError as e:
            # Ignore if already shared (status 409)
            if "409" not in str(e):
                print(f"Failed to share board with user {user_id}: {str(e)}")            
    
    async def share_board_with_user(self, board_id: str, user_id: str, permission_level: str = "read") -> bool:
        """Share a Deck board with a specific user.
        
        Args:
            board_id: ID of the board to share
            user_id: User ID to share with
            permission_level: Permission level (read, edit, manage, or share)
            
        Returns:
            Boolean indicating success
            
        Raises:
            ValueError: If the request fails
        """
        # Validate permission level
        if permission_level not in ["read", "edit", "manage", "share"]:
            raise ValueError(f"Invalid permission level. Must be one of: read, edit, manage, share")
            
        # Map permission levels
        permissions = {
            "read": {
                "permissionEdit": False,
                "permissionShare": False,
                "permissionManage": False
            },
            "edit": {
                "permissionEdit": True,
                "permissionShare": False,
                "permissionManage": False
            },
            "manage": {
                "permissionEdit": True,
                "permissionShare": False,
                "permissionManage": True
            },
            "share": {
                "permissionEdit": True,
                "permissionShare": True,
                "permissionManage": True
            }
        }
            
        # Set up the request data
        share_data = {
            "type": 0,  # 0 = user
            "participant": user_id,
            **permissions[permission_level]
        }
        
        # Set up headers
        headers = {
            "Content-Type": "application/json",
            "OCS-APIRequest": "true"
        }
        
        # Make the request
        url = f"{self.nextcloud_host}/index.php/apps/deck/api/v1.0/boards/{board_id}/acl"
        
        try:
            session = await self._ensure_session()
            async with session.post(
                url, 
                json=share_data, 
                auth=aiohttp.BasicAuth(self.username, self.password),
                headers=headers
            ) as response:
                if response.status >= 400:
                    text = await response.text()
                    raise ValueError(f"Request failed with status {response.status}: {text}")
                
                # Get text response and parse it
                result = await response.json()
                return isinstance(result, dict) and "id" in result
        except Exception as e:
            raise ValueError(f"Failed to share board: {str(e)}")
            
    async def share_board_with_group(self, board_id: str, group_id: str, permission_level: str = "read") -> bool:
        """Share a Deck board with a group.
        
        Args:
            board_id: ID of the board to share
            group_id: Group ID to share with
            permission_level: Permission level (read, edit, manage, or share)
            
        Returns:
            Boolean indicating success
            
        Raises:
            ValueError: If the request fails
        """
        # Validate permission level
        if permission_level not in ["read", "edit", "manage", "share"]:
            raise ValueError(f"Invalid permission level. Must be one of: read, edit, manage, share")
            
        # Map permission levels
        permissions = {
            "read": {
                "permissionEdit": False,
                "permissionShare": False,
                "permissionManage": False
            },
            "edit": {
                "permissionEdit": True,
                "permissionShare": False,
                "permissionManage": False
            },
            "manage": {
                "permissionEdit": True,
                "permissionShare": False,
                "permissionManage": True
            },
            "share": {
                "permissionEdit": True,
                "permissionShare": True,
                "permissionManage": True
            }
        }
            
        # Set up the request data
        share_data = {
            "type": 1,  # 1 = group
            "participant": group_id,
            **permissions[permission_level]
        }
        
        # Set up headers
        headers = {
            "Content-Type": "application/json",
            "OCS-APIRequest": "true"
        }
        
        # Make the request
        url = f"{self.nextcloud_host}/index.php/apps/deck/api/v1.0/boards/{board_id}/acl"
        
        try:
            session = await self._ensure_session()
            async with session.post(
                url, 
                json=share_data, 
                auth=aiohttp.BasicAuth(self.username, self.password),
                headers=headers
            ) as response:
                if response.status >= 400:
                    text = await response.text()
                    raise ValueError(f"Request failed with status {response.status}: {text}")
                
                # Get text response and parse it
                result = await response.json()
                return isinstance(result, dict) and "id" in result
        except Exception as e:
            raise ValueError(f"Failed to share board with group: {str(e)}")

    async def share_board_with_meeting_participants(self, board_id: str, permission_level: str = "edit") -> List[Dict[str, Any]]:
        """Share a Deck board with all meeting participants.
        
        Args:
            board_id: ID of the board to share
            permission_level: Permission level (read, edit, manage, or share)
            
        Returns:
            List of participant dictionaries
            
        Raises:
            ValueError: If the request fails
        """
        # Validate permission level
        if permission_level not in ["read", "edit", "manage", "share"]:
            raise ValueError(f"Invalid permission level. Must be one of: read, edit, manage, share")
            
        # Map permission levels
        permissions = {
            "read": {
                "permissionEdit": False,
                "permissionShare": False,
                "permissionManage": False
            },
            "edit": {
                "permissionEdit": True,
                "permissionShare": False,
                "permissionManage": False
            },
            "manage": {
                "permissionEdit": True,
                "permissionShare": False,
                "permissionManage": True
            },
            "share": {
                "permissionEdit": True,
                "permissionShare": True,
                "permissionManage": True
            }
        }
            
        # Get participants
        try:
            participants = await self.get_participants()
        except ValueError as e:
            print(f"Failed to get participants: {str(e)}")
            return []
            
        # Share the board with each participant
        shared_participants = []
        for participant in participants:
            user_id = participant.get("userId")
            if user_id and user_id != self.username:  # Don't share with self
                try:
                    await self._share_board_with_user(board_id, user_id, permission_level)
                    shared_participants.append(participant)
                except ValueError as e:
                    print(f"Failed to share board with user {user_id}: {str(e)}")
                    
        return shared_participants

    async def share_cached_board_with_user(self, user_id: str, permission_level: str = "edit") -> bool:
        """Share the currently cached board with a user.
        
        Args:
            user_id: User ID to share with
            permission_level: Permission level (read, edit, manage, or share)
            
        Returns:
            Boolean indicating success
            
        Raises:
            ValueError: If the request fails
        """
        # Validate permission level
        if permission_level not in ["read", "edit", "manage", "share"]:
            raise ValueError(f"Invalid permission level. Must be one of: read, edit, manage, share")
            
        # Map permission levels
        permissions = {
            "read": {
                "permissionEdit": False,
                "permissionShare": False,
                "permissionManage": False
            },
            "edit": {
                "permissionEdit": True,
                "permissionShare": False,
                "permissionManage": False
            },
            "manage": {
                "permissionEdit": True,
                "permissionShare": False,
                "permissionManage": True
            },
            "share": {
                "permissionEdit": True,
                "permissionShare": True,
                "permissionManage": True
            }
        }
            
        # Set up the request data
        share_data = {
            "type": 0,  # 0 = user
            "participant": user_id,
            **permissions[permission_level]
        }
        
        # Set up headers
        headers = {
            "Content-Type": "application/json",
            "OCS-APIRequest": "true"
        }
        
        # Make the request
        url = f"{self.nextcloud_host}/index.php/apps/deck/api/v1.0/boards/{self.board_id}/acl"
        
        try:
            session = await self._ensure_session()
            async with session.post(
                url, 
                json=share_data, 
                auth=aiohttp.BasicAuth(self.username, self.password),
                headers=headers
            ) as response:
                if response.status >= 400:
                    text = await response.text()
                    raise ValueError(f"Request failed with status {response.status}: {text}")
                
                # Get text response and parse it
                result = await response.json()
                return isinstance(result, dict) and "id" in result
        except Exception as e:
            raise ValueError(f"Failed to share board: {str(e)}")

    async def create_default_board_stacks(self, board_id: str) -> List[Dict[str, Any]]:
        """Create default stacks in a Deck board if they don't already exist.
        
        Default stacks are: "To Do", "In Progress", "Done"
        
        Args:
            board_id: ID of the board
            
        Returns:
            List of created or existing stacks
            
        Raises:
            ValueError: If the request fails
        """
        # First get existing stacks to avoid duplicates
        existing_stacks = await self.get_board_stacks(board_id)
        existing_titles = set(stack['title'] for stack in existing_stacks if 'title' in stack)
        
        # Define default stacks
        default_stacks = [
            {"title": "To Do", "order": 0},
            {"title": "In Progress", "order": 1},
            {"title": "Done", "order": 2}
        ]
        
        # Create missing stacks
        results = []
        for i, stack_info in enumerate(default_stacks):
            if stack_info["title"] not in existing_titles:
                try:
                    new_stack = await self.create_stack(
                        board_id=board_id,
                        title=stack_info["title"],
                        order=stack_info["order"]
                    )
                    results.append(new_stack)
                    print(f"Created stack: {stack_info['title']}")
                except ValueError as e:
                    print(f"Failed to create stack {stack_info['title']}: {str(e)}")
            else:
                # Find the existing stack by title
                matching_stack = next(
                    (stack for stack in existing_stacks if stack.get('title') == stack_info["title"]), 
                    None
                )
                if matching_stack:
                    results.append(matching_stack)
                    print(f"Stack already exists: {stack_info['title']}")
                    
        return results

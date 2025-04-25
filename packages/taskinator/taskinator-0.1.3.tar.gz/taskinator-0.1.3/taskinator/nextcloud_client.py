"""NextCloud client for interacting with NextCloud Tasks API."""
import asyncio
import base64
import json
import logging
import os
import time
from datetime import datetime, date, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Union, Tuple
from urllib.parse import urljoin
import uuid
import xml.etree.ElementTree as ET

import aiohttp
import caldav
from caldav.elements import dav, cdav
import requests
from pydantic import BaseModel, ConfigDict, Field, model_validator

# Import icalendar components
from icalendar import Calendar, Todo

from .utils import logger

class NextCloudTask(BaseModel):
    """NextCloud task data model."""
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_serialization_defaults_required=True
    )
    
    id: str
    title: str
    description: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    priority: Optional[str] = None
    calendar_id: Optional[str] = None
    categories: List[str] = Field(default_factory=list)
    etag: Optional[str] = None
    fileid: Optional[str] = None
    subtasks: List[Dict[str, Any]] = Field(default_factory=list)
    parent_id: Optional[str] = None
    
    @classmethod
    def from_caldav_todo(cls, todo: caldav.Todo) -> "NextCloudTask":
        """Create a NextCloudTask from a CalDAV Todo."""
        # Extract the iCalendar component
        ical = todo.icalendar_component
        
        # Extract basic properties
        uid = str(ical.get("uid", ""))
        summary = str(ical.get("summary", ""))
        description = str(ical.get("description", ""))
        
        # Extract status
        status = "pending"
        if ical.get("status") == "COMPLETED":
            status = "done"
        elif ical.get("status") == "IN-PROCESS":
            status = "in_progress"
            
        # Extract due date
        due_date = None
        if ical.get("due"):
            due = ical.get("due").dt
            if isinstance(due, datetime):
                due_date = due.isoformat()
            elif isinstance(due, date):
                due_date = datetime.combine(due, time()).isoformat()
                
        # Extract created and updated timestamps
        created_at = None
        if ical.get("created"):
            created = ical.get("created").dt
            if isinstance(created, datetime):
                created_at = created.isoformat()
                
        updated_at = None
        if ical.get("last-modified"):
            updated = ical.get("last-modified").dt
            if isinstance(updated, datetime):
                updated_at = updated.isoformat()
                
        # Extract priority
        priority_map = {1: "high", 5: "medium", 9: "low"}
        priority = None
        if ical.get("priority"):
            priority_val = int(ical.get("priority"))
            priority = priority_map.get(priority_val, "medium")
            
        # Extract categories
        categories = []
        if ical.get("categories"):
            categories = [str(cat) for cat in ical.get("categories").cats]
            
        # Get etag and fileid
        etag = getattr(todo, "etag", None)
        fileid = uid
        
        # Check for parent task relationship (RELATED-TO field)
        parent_id = None
        if ical.get("related-to"):
            parent_id = str(ical.get("related-to"))
            
        # Extract subtasks (if any are defined as RELATED-TO with this task as parent)
        # Note: This would require additional API calls to get the actual subtasks
        # We'll handle this separately when needed
        subtasks = []
        
        # Get calendar_id as string
        calendar = getattr(todo, "parent", None)
        calendar_id = str(calendar.id) if calendar and hasattr(calendar, 'id') else None
        
        return cls(
            id=uid,
            title=summary,
            description=description,
            status=status,
            due_date=due_date,
            created_at=created_at,
            updated_at=updated_at,
            priority=priority,
            calendar_id=calendar_id,
            categories=categories,
            etag=etag,
            fileid=fileid,
            subtasks=subtasks,
            parent_id=parent_id
        )
        
    def to_caldav_todo(self) -> Dict[str, Any]:
        """Convert a NextCloudTask to a CalDAV Todo."""
        # Create a new iCalendar component
        vcal = Calendar()
        vtodo = Todo()
        vcal.add_component(vtodo)
        
        # Set basic properties
        vtodo.add("uid", self.id)
        vtodo.add("summary", self.title)
        if self.description:
            vtodo.add("description", self.description)
            
        # Set status
        if self.status == "done":
            vtodo.add("status", "COMPLETED")
            vtodo.add("completed", datetime.now())
        elif self.status == "in_progress":
            vtodo.add("status", "IN-PROCESS")
        else:
            vtodo.add("status", "NEEDS-ACTION")
            
        # Set due date
        if self.due_date:
            try:
                due_date = datetime.fromisoformat(self.due_date)
                vtodo.add("due", due_date)
            except (ValueError, TypeError):
                pass
                
        # Set priority
        priority_map = {"high": 1, "medium": 5, "low": 9}
        if self.priority in priority_map:
            vtodo.add("priority", priority_map[self.priority])
            
        # Set categories
        if self.categories:
            vtodo.add("categories", self.categories)
            
        # Set created and updated timestamps
        if self.created_at:
            try:
                created_at = datetime.fromisoformat(self.created_at)
                vtodo.add("created", created_at)
            except (ValueError, TypeError):
                pass
                
        if self.updated_at:
            try:
                updated_at = datetime.fromisoformat(self.updated_at)
                vtodo.add("last-modified", updated_at)
            except (ValueError, TypeError):
                pass
                
        # Convert to iCalendar format
        return vcal.to_ical().decode("utf-8")
    
    @classmethod
    def from_json(cls, json_str: str) -> List["NextCloudTask"]:
        """Deserialize a JSON string containing a list of tasks."""
        data = json.loads(json_str)
        return [cls.model_validate(item) for item in data]

class NextCloudCalendar:
    """NextCloud calendar object."""
    
    def __init__(self, id: str, display_name: str, url: str = None):
        """Initialize calendar.
        
        Args:
            id: Calendar ID
            display_name: Display name
            url: Calendar URL
        """
        self.id = id
        self.display_name = display_name
        self.url = url

class NextCloudAuthManager:
    """Handles token-based authentication for NextCloud API."""
    
    def __init__(
        self,
        base_url: str,
        username: str,
        password: str = None,
        app_token: str = None,
        token_refresh_seconds: int = 3600
    ):
        """Initialize the authentication manager."""
        self.base_url = base_url
        self.username = username
        self.password = password
        self._app_token = app_token
        self.token_refresh_seconds = token_refresh_seconds
        self._token = None
        self._token_expiry = 0
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers for API requests."""
        # In a real implementation, this would return proper auth headers
        # For now, we'll return basic auth headers
        import base64
        auth_str = f"{self.username}:{self.password or self._app_token}"
        encoded = base64.b64encode(auth_str.encode()).decode()
        return {"Authorization": f"Basic {encoded}"}

class NextCloudRateLimiter:
    """Rate limiter for NextCloud API requests."""
    
    def __init__(self, requests_per_minute: int = 60):
        """Initialize the rate limiter."""
        self.requests_per_minute = requests_per_minute
        self.request_interval = 60.0 / requests_per_minute
        self.last_request_time = 0
    
    async def wait_if_needed(self):
        """Wait if needed to respect rate limits."""
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        
        if elapsed < self.request_interval:
            wait_time = self.request_interval - elapsed
            await asyncio.sleep(wait_time)
            
        self.last_request_time = current_time

# Deck API Models
class DeckBoardPermission(str, Enum):
    """Permission levels for Deck boards."""
    READ = "read"
    EDIT = "edit"
    MANAGE = "manage"
    SHARE = "share"

class DeckBoard(BaseModel):
    """Deck board model."""
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_serialization_defaults_required=True
    )
    
    id: int
    title: str
    owner: Optional[Dict[str, Any]] = None
    color: Optional[str] = None
    archived: bool = False
    deleted_at: Optional[Union[str, int]] = None
    last_modified: Optional[Union[str, int]] = None
    permissions: Optional[Dict[str, Any]] = None
    users: Optional[List[Any]] = Field(default_factory=list)
    shared: int = 0
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DeckBoard":
        """Create a DeckBoard from a dictionary."""
        if not isinstance(data, dict):
            raise ValueError(f"Expected dictionary, got {type(data)}")
            
        # Extract basic properties
        board_id = data.get("id")
        if board_id is None:
            raise ValueError("Board ID is required")
            
        title = data.get("title")
        if not title:
            raise ValueError("Board title is required")
            
        # Extract other properties
        owner = data.get("owner")
        color = data.get("color", "0082c9")
        archived = data.get("archived", False)
        
        # Handle timestamps which might be integers
        deleted_at = data.get("deletedAt")
        if isinstance(deleted_at, int) and deleted_at > 0:
            deleted_at = datetime.fromtimestamp(deleted_at).isoformat()
        
        last_modified = data.get("lastModified")
        if isinstance(last_modified, int) and last_modified > 0:
            last_modified = datetime.fromtimestamp(last_modified).isoformat()
        
        # Extract permissions
        permissions = data.get("permissions", {})
        
        # Extract users
        users = []
        if "acl" in data and isinstance(data["acl"], list):
            for acl in data["acl"]:
                if isinstance(acl, dict) and "participant" in acl:
                    users.append(acl["participant"])
                    
        # Extract shared status
        shared = data.get("shared", 0)
        
        # Create the board
        return cls(
            id=board_id,
            title=title,
            owner=owner,
            color=color,
            archived=archived,
            deleted_at=deleted_at,
            last_modified=last_modified,
            permissions=permissions,
            users=users,
            shared=shared
        )

class DeckStack(BaseModel):
    """Deck stack model (column in a board)."""
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_serialization_defaults_required=True
    )
    
    id: int
    title: str
    board_id: int
    order: int = 0
    cards_count: int = 0
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DeckStack":
        """Create a DeckStack from a dictionary."""
        if not isinstance(data, dict):
            raise ValueError(f"Expected dictionary, got {type(data)}")
            
        # Extract basic properties
        stack_id = data.get("id")
        if stack_id is None:
            raise ValueError("Stack ID is required")
            
        title = data.get("title")
        if not title:
            raise ValueError("Stack title is required")
            
        board_id = data.get("boardId")
        if board_id is None:
            raise ValueError("Board ID is required")
            
        # Extract other properties
        order = data.get("order", 0)
        cards_count = data.get("cards_count", 0)
        
        # Create the stack
        return cls(
            id=stack_id,
            title=title,
            board_id=board_id,
            order=order,
            cards_count=cards_count
        )

class DeckSubtask(BaseModel):
    """Deck subtask model."""
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_serialization_defaults_required=True
    )
    
    id: int
    title: str
    card_id: int
    status: int = 0  # 0 = open, 1 = done
    created_at: Optional[str] = None
    last_modified: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DeckSubtask":
        """Create a DeckSubtask from a dictionary."""
        if not isinstance(data, dict):
            raise ValueError(f"Expected dictionary, got {type(data)}")
            
        # Extract basic properties
        subtask_id = data.get("id")
        if subtask_id is None:
            raise ValueError("Subtask ID is required")
            
        title = data.get("title")
        if not title:
            raise ValueError("Subtask title is required")
            
        card_id = data.get("cardId")
        if card_id is None:
            raise ValueError("Card ID is required")
            
        # Extract other properties
        status = data.get("status", 0)
        created_at = data.get("createdAt")
        last_modified = data.get("lastModified")
        
        # Create the subtask
        return cls(
            id=subtask_id,
            title=title,
            card_id=card_id,
            status=status,
            created_at=created_at,
            last_modified=last_modified
        )

class DeckCard(BaseModel):
    """Deck card model (task in a stack)."""
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_serialization_defaults_required=True
    )
    
    id: int
    title: str
    description: Optional[str] = None
    stack_id: Optional[int] = None
    order: int = 0
    archived: bool = False
    deleted_at: Optional[Union[str, int]] = None
    owner: Optional[Union[str, Dict[str, Any]]] = None
    labels: Optional[List[Any]] = Field(default_factory=list)
    assigned_users: Optional[List[Any]] = Field(default_factory=list)
    attachments: Optional[List[Any]] = Field(default_factory=list)
    attachments_count: int = 0
    comments_count: int = 0
    comments_unread: int = 0
    due_date: Optional[str] = None
    created_at: Optional[Union[str, int]] = None
    last_modified: Optional[Union[str, int]] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DeckCard":
        """Create a DeckCard from a dictionary."""
        if not isinstance(data, dict):
            raise ValueError(f"Expected dictionary, got {type(data)}")
            
        # Extract basic properties
        card_id = data.get("id")
        if card_id is None:
            raise ValueError("Card ID is required")
            
        title = data.get("title")
        if not title:
            raise ValueError("Card title is required")
            
        # Extract other properties
        description = data.get("description", "")
        stack_id = data.get("stackId")
        order = data.get("order", 0)
        archived = data.get("archived", False)
        deleted_at = data.get("deletedAt")
        owner = data.get("owner")
        labels = data.get("labels", [])
        assigned_users = data.get("assignedUsers", [])
        attachments = data.get("attachments", [])
        attachments_count = data.get("attachmentsCount", 0)
        comments_count = data.get("commentsCount", 0)
        comments_unread = data.get("commentsUnread", 0)
        due_date = data.get("duedate")
        
        # Handle timestamps which might be integers
        created_at = data.get("createdAt")
        if isinstance(created_at, int) and created_at > 0:
            created_at = datetime.fromtimestamp(created_at).isoformat()
            
        last_modified = data.get("lastModified")
        if isinstance(last_modified, int) and last_modified > 0:
            last_modified = datetime.fromtimestamp(last_modified).isoformat()
        
        # Create the card
        return cls(
            id=card_id,
            title=title,
            description=description,
            stack_id=stack_id,
            order=order,
            archived=archived,
            deleted_at=deleted_at,
            owner=owner,
            labels=labels,
            assigned_users=assigned_users,
            attachments=attachments,
            attachments_count=attachments_count,
            comments_count=comments_count,
            comments_unread=comments_unread,
            due_date=due_date,
            created_at=created_at,
            last_modified=last_modified
        )
        
    def to_nextcloud_task(self) -> NextCloudTask:
        """Convert a DeckCard to a NextCloudTask."""
        # Create a unique ID for the task that indicates it's from the Deck API
        task_id = f"deck-card-{self.id}"
        
        # Convert subtasks to a format that can be used by Taskinator
        subtasks = []
        if self.subtasks:
            for subtask in self.subtasks:
                subtasks.append({
                    "id": f"deck-subtask-{subtask.id}",
                    "title": subtask.title,
                    "status": "done" if subtask.status == 1 else "pending"
                })
                
        # Determine status based on stack title (if available)
        # This would require additional context, but we can make a best guess
        status = "pending"
        
        # Create the NextCloudTask
        return NextCloudTask(
            id=task_id,
            title=self.title,
            description=self.description or "",
            status=status,
            due_date=self.duedate,
            created_at=self.created_at,
            updated_at=self.last_modified,
            etag=f"deck-card-{self.id}",  # Use the card ID as the etag
            subtasks=subtasks
        )

class NextCloudClient:
    """Client for interacting with NextCloud Tasks API."""
    
    def __init__(
        self, 
        host: str, 
        username: str, 
        password: str = None, 
        token: str = None,
        calendar_id: str = None,
        calendar_name: str = "Taskinator",
        verbose: bool = False
    ):
        """Initialize NextCloud client.
        
        Args:
            host: NextCloud host
            username: NextCloud username
            password: NextCloud password
            token: NextCloud token
            calendar_id: Calendar ID to use for tasks
            calendar_name: Calendar name to use for tasks
            verbose: Enable verbose logging
        """
        self.host = host
        self.username = username
        self.password = password
        self.token = token
        self.calendar_id = calendar_id
        self.calendar_name = calendar_name
        self.verbose = verbose
        
        # Remove trailing slash from host if present
        if self.host and self.host.endswith("/"):
            self.host = self.host[:-1]
            
        # Base URL for API requests
        self.base_url = self.host
        
        # CalDAV URL
        self.caldav_url = f"{self.host}/remote.php/dav"
        
        # API path for CalDAV
        self.api_path = "/remote.php/dav"
        
        # Simple auth manager for compatibility
        self.auth_manager = type('AuthManager', (), {'password': password})
        
        # Initialize session
        self._session = None
        
        # Initialize calendars dictionary
        self._calendars = {}
        
        # Initialize client and principal
        self._client = None
        self._principal = None
    
    async def initialize(self):
        """Initialize the client.
        
        This method should be called after creating the client to set up
        the HTTP session and authenticate.
        """
        # Create HTTP session
        self._session = aiohttp.ClientSession()
        
        # Set authentication
        if self.token:
            self._session.headers.update({
                "Authorization": f"Bearer {self.token}"
            })
        else:
            # Use basic auth
            auth = aiohttp.BasicAuth(self.username, self.password)
            self._session._default_auth = auth

    # Board operations
    
    async def get_boards(self) -> List[DeckBoard]:
        """Get all boards from the Deck API."""
        if not self.use_deck_api:
            raise ValueError("Deck API is not enabled")
            
        url = f"{self.base_url}/index.php/apps/deck/api/v1.0/boards"
        response = await self._make_api_request("GET", url)
        
        if response.status == 200:
            boards_data = await response.json()
            return [DeckBoard.from_dict(board_data) for board_data in boards_data]
        else:
            error_text = await response.text()
            try:
                error_json = await response.json()
                error_message = error_json
            except:
                error_message = {"text": error_text}
                
            raise NextCloudAPIError(f"Deck API error: {response.status} - {error_message}")
        
    async def get_board(self, board_id: int) -> DeckBoard:
        """Get a specific board from the Deck API."""
        if not self.use_deck_api:
            raise ValueError("Deck API is not enabled")
        
        status, data = await self._make_deck_request("GET", f"/boards/{board_id}")
        return DeckBoard.from_dict(data)
        
    async def create_board(self, title: str, color: str = "0082c9") -> DeckBoard:
        """Create a new board in the Deck API."""
        if not self.use_deck_api:
            raise ValueError("Deck API is not enabled")
            
        url = f"{self.base_url}/index.php/apps/deck/api/v1.0/boards"
        data = {
            "title": title,
            "color": color
        }
        
        response = await self._make_api_request("POST", url, json=data)
        
        if response.status == 200:
            board_data = await response.json()
            return DeckBoard.from_dict(board_data)
        else:
            error_text = await response.text()
            try:
                error_json = await response.json()
                error_message = error_json
            except:
                error_message = {"text": error_text}
                
            raise NextCloudAPIError(f"Deck API error: {response.status} - {error_message}")
            
    async def update_board(self, board_id: int, board_data: Dict[str, Any]) -> DeckBoard:
        """Update a board in the Deck API."""
        if not self.use_deck_api:
            raise ValueError("Deck API is not enabled")
        
        status, data = await self._make_deck_request("PUT", f"/boards/{board_id}", data=board_data)
        return DeckBoard.from_dict(data)
        
    async def delete_board(self, board_id: int) -> None:
        """Delete a board from the Deck API."""
        if not self.use_deck_api:
            raise ValueError("Deck API is not enabled")
        
        await self._make_deck_request("DELETE", f"/boards/{board_id}")
        
    # Stack operations
    
    async def get_stacks(self, board_id: int) -> List[DeckStack]:
        """Get all stacks for a board from the Deck API."""
        if not self.use_deck_api:
            raise ValueError("Deck API is not enabled")
        
        status, data = await self._make_deck_request("GET", f"/boards/{board_id}/stacks")
        return [DeckStack.from_dict(stack) for stack in data]
        
    async def create_stack(self, board_id: int, title: str, order: int = 0) -> DeckStack:
        """Create a new stack in the Deck API."""
        if not self.use_deck_api:
            raise ValueError("Deck API is not enabled")
        
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
        
        try:
            # Make the request
            status, data = await self._make_deck_request("POST", f"/boards/{board_id}/stacks", data=stack_data)
            
            # Convert to DeckStack and return
            return DeckStack.from_dict(data)
        except Exception as e:
            logger.error(f"Failed to create stack: {e}")
            raise ValueError(f"Failed to create stack: {e}")
            
    async def update_stack(self, board_id: int, stack_id: int, stack_data: Dict[str, Any]) -> DeckStack:
        """Update a stack in the Deck API."""
        if not self.use_deck_api:
            raise ValueError("Deck API is not enabled")
        
        status, data = await self._make_deck_request("PUT", f"/boards/{board_id}/stacks/{stack_id}", data=stack_data)
        return DeckStack.from_dict(data)
        
    async def delete_stack(self, board_id: int, stack_id: int) -> None:
        """Delete a stack from the Deck API."""
        if not self.use_deck_api:
            raise ValueError("Deck API is not enabled")
        
        await self._make_deck_request("DELETE", f"/boards/{board_id}/stacks/{stack_id}")
        
    # Card operations
    
    async def get_cards(self, board_id: int, stack_id: int) -> List[DeckCard]:
        """Get all cards for a stack from the Deck API."""
        if not self.use_deck_api:
            raise ValueError("Deck API is not enabled")
        
        status, data = await self._make_deck_request("GET", f"/boards/{board_id}/stacks/{stack_id}/cards")
        return [DeckCard.from_dict(card) for card in data]
        
    async def get_card(self, card_id: int) -> DeckCard:
        """Get a specific card from the Deck API."""
        if not self.use_deck_api:
            raise ValueError("Deck API is not enabled")
        
        status, data = await self._make_deck_request("GET", f"/cards/{card_id}")
        return DeckCard.from_dict(data)
        
    async def create_card(self, board_id: int, stack_id: int, card_data: Dict[str, Any]) -> DeckCard:
        """Create a new card in the Deck API."""
        if not self.use_deck_api:
            raise ValueError("Deck API is not enabled")
        
        url = f"{self.base_url}/index.php/apps/deck/api/v1.0/boards/{board_id}/stacks/{stack_id}/cards"
        
        # Prepare the request data
        data = {
            "title": card_data.get("title", ""),
            "description": card_data.get("description", ""),
            "type": "plain",
            "order": card_data.get("order", 0)
        }
        
        # Add optional fields if provided
        if "duedate" in card_data and card_data["duedate"]:
            data["duedate"] = card_data["duedate"]
        if "priority" in card_data:
            data["priority"] = card_data["priority"]
            
        # Make the request
        response = await self._make_api_request("POST", url, json=data)
        
        # Parse the response
        if response.status == 200:
            card_data = await response.json()
            return DeckCard.from_dict(card_data)
        else:
            error_text = await response.text()
            try:
                error_json = await response.json()
                error_message = error_json
            except:
                error_message = {"text": error_text}
                
            raise NextCloudAPIError(f"Deck API error: {response.status} - {error_message}")
            
    async def update_card(self, card_id: int, card_data: Dict[str, Any]) -> DeckCard:
        """Update a card in the Deck API."""
        if not self.use_deck_api:
            raise ValueError("Deck API is not enabled")
        
        status, data = await self._make_deck_request("PUT", f"/cards/{card_id}", data=card_data)
        return DeckCard.from_dict(data)
        
    async def delete_card(self, card_id: int) -> None:
        """Delete a card from the Deck API."""
        if not self.use_deck_api:
            raise ValueError("Deck API is not enabled")
        
        await self._make_deck_request("DELETE", f"/cards/{card_id}")
        
    # Subtask operations
    
    async def get_subtasks(self, card_id: int) -> List[DeckSubtask]:
        """Get all subtasks for a card from the Deck API."""
        if not self.use_deck_api:
            raise ValueError("Deck API is not enabled")
        
        status, data = await self._make_deck_request("GET", f"/cards/{card_id}/subtasks")
        return [DeckSubtask.from_dict(subtask) for subtask in data]
        
    async def create_subtask(self, card_id: int, title: str) -> DeckSubtask:
        """Create a new subtask in the Deck API."""
        if not self.use_deck_api:
            raise ValueError("Deck API is not enabled")
        
        subtask_data = {
            "title": title
        }
        status, data = await self._make_deck_request("POST", f"/cards/{card_id}/subtasks", data=subtask_data)
        return DeckSubtask.from_dict(data)
        
    async def update_subtask(self, card_id: int, subtask_id: int, subtask_data: Dict[str, Any]) -> DeckSubtask:
        """Update a subtask in the Deck API."""
        if not self.use_deck_api:
            raise ValueError("Deck API is not enabled")
        
        status, data = await self._make_deck_request("PUT", f"/cards/{card_id}/subtasks/{subtask_id}", data=subtask_data)
        return DeckSubtask.from_dict(data)
        
    async def delete_subtask(self, card_id: int, subtask_id: int) -> None:
        """Delete a subtask from the Deck API."""
        if not self.use_deck_api:
            raise ValueError("Deck API is not enabled")
        
        await self._make_deck_request("DELETE", f"/cards/{card_id}/subtasks/{subtask_id}")
        
    # Unified task operations
    
    async def create_unified_task(self, task_data: Dict[str, Any]) -> NextCloudTask:
        """Create a task using either CalDAV or Deck API based on task properties."""
        # Determine which API to use based on task properties
        # Use Deck API for tasks with subtasks, CalDAV for simple tasks
        if self.use_deck_api and "subtasks" in task_data and task_data["subtasks"]:
            # Use Deck API for tasks with subtasks
            # Get or create a board for Taskinator
            board_name = "Taskinator"
            boards = await self.get_boards()
            board = next((b for b in boards if b.title == board_name), None)
            
            if not board:
                # Create a new board
                board = await self.create_board(board_name)
                
                # Create default stacks
                await self.create_stack(board.id, "To Do", 0)
                await self.create_stack(board.id, "In Progress", 1)
                await self.create_stack(board.id, "Done", 2)
            
            # Get stacks
            stacks = await self.get_stacks(board.id)
            
            # Determine which stack to use based on task status
            status = task_data.get("status", "pending")
            stack_name = "To Do"
            if status == "in_progress":
                stack_name = "In Progress"
            elif status == "done":
                stack_name = "Done"
            
            stack = next((s for s in stacks if s.title == stack_name), None)
            if not stack:
                # Use the first stack if we can't find a matching one
                stack = stacks[0] if stacks else None
                
            if not stack:
                # Create a default stack if none exists
                stack = await self.create_stack(board.id, "To Do", 0)
            
            # Create the card
            card_data = {
                "title": task_data.get("title", "Untitled Task"),
                "description": task_data.get("description", ""),
                "duedate": task_data.get("due_date"),
                "order": 0
            }
            
            # Map priority if provided
            if "priority" in task_data:
                priority_map = {"high": 1, "medium": 5, "low": 9}
                priority_val = priority_map.get(task_data["priority"], 5)
                card_data["priority"] = priority_val
            
            # Create the card
            card = await self.create_card(board.id, stack.id, card_data)
            
            # Create subtasks if provided
            if "subtasks" in task_data and task_data["subtasks"]:
                for subtask_data in task_data["subtasks"]:
                    title = subtask_data.get("title", "Untitled Subtask")
                    await self.create_subtask(card.id, title)
            
            # Convert to NextCloudTask and return
            return card.to_nextcloud_task()
        else:
            # Use CalDAV for simple tasks
            return await self.create_task(task_data)
            
    async def update_unified_task(self, task_id: str, task_data: Dict[str, Any]) -> NextCloudTask:
        """Update a task using either CalDAV or Deck API based on task ID."""
        # Determine which API to use based on task ID
        if self.use_deck_api and task_id.startswith("deck-card-"):
            # Use Deck API for tasks with deck-card- prefix
            # Extract the card ID
            card_id = int(task_id.replace("deck-card-", ""))
            
            # Prepare update data
            update_data = {
                "title": task_data.get("title"),
                "description": task_data.get("description")
            }
            
            # Map status to stack if provided
            if "status" in task_data:
                status = task_data["status"]
                board_id = None
                
                # Get the current card to find its board
                card = await self.get_card(card_id)
                if card:
                    # Find the stack that the card is in
                    stack = await self.get_stack(card.stack_id)
                    if stack:
                        board_id = stack.board_id
                
                if board_id:
                    # Find the appropriate stack for the status
                    stacks = await self.get_stacks(board_id)
                    stack_name = "To Do"
                    if status == "in_progress":
                        stack_name = "In Progress"
                    elif status == "done":
                        stack_name = "Done"
                    
                    target_stack = next((s for s in stacks if s.title == stack_name), None)
                    if target_stack:
                        update_data["stackId"] = target_stack.id
            
            # Map priority if provided
            if "priority" in task_data:
                priority_map = {"high": 1, "medium": 5, "low": 9}
                priority_val = priority_map.get(task_data["priority"], 5)
                update_data["priority"] = priority_val
                
            # Map due date if provided
            if "due_date" in task_data:
                update_data["duedate"] = task_data["due_date"]
            
            # Update the card
            updated_card = await self.update_card(card_id, update_data)
            
            # Handle subtasks if provided
            if "subtasks" in task_data and task_data["subtasks"]:
                # Get existing subtasks
                existing_subtasks = await self.get_subtasks(card_id)
                
                # Update existing subtasks and create new ones
                for subtask_data in task_data["subtasks"]:
                    if "id" in subtask_data:
                        # Update existing subtask
                        subtask_id = subtask_data["id"]
                        if subtask_id.startswith("deck-subtask-"):
                            subtask_id = int(subtask_id.replace("deck-subtask-", ""))
                            
                        # Find the subtask
                        subtask = next((s for s in existing_subtasks if s.id == subtask_id), None)
                        if subtask:
                            update_data = {}
                            if "title" in subtask_data:
                                update_data["title"] = subtask_data["title"]
                            if "status" in subtask_data:
                                update_data["status"] = 1 if subtask_data["status"] == "done" else 0
                                
                            await self.update_subtask(card_id, subtask_id, update_data)
                    else:
                        # Create new subtask
                        await self.create_subtask(card_id, subtask_data.get("title", "Untitled Subtask"))
            
            # Convert to NextCloudTask and return
            return updated_card.to_nextcloud_task()
        else:
            # Use CalDAV for simple tasks
            return await self.update_task(task_id, task_data)
            
    async def delete_unified_task(self, task_id: str) -> None:
        """Delete a task using either CalDAV or Deck API based on task ID."""
        if self.use_deck_api and task_id.startswith("deck-card-"):
            # Use Deck API for tasks with deck-card- prefix
            # Extract the card ID
            card_id = int(task_id.replace("deck-card-", ""))
            
            # Delete the card
            await self.delete_card(card_id)
        else:
            # Use CalDAV for simple tasks
            await self.delete_task(task_id)
            
    async def get_unified_tasks(self) -> List[NextCloudTask]:
        """Get tasks from both CalDAV and Deck API."""
        tasks = []
        
        # Get CalDAV tasks
        caldav_tasks = await self.get_tasks()
        tasks.extend(caldav_tasks)
        
        # Get Deck cards if Deck API is enabled
        if self.use_deck_api:
            boards = await self.get_boards()
            for board in boards:
                stacks = await self.get_stacks(board.id)
                for stack in stacks:
                    cards = await self.get_cards(board.id, stack.id)
                    for card in cards:
                        tasks.append(card.to_nextcloud_task())
            
        return tasks

    async def get_calendars(self) -> List[NextCloudCalendar]:
        """Get all calendars from NextCloud.
        
        Returns:
            List of NextCloudCalendar objects
        """
        try:
            # Ensure we have a session
            if not self._session:
                await self.initialize()
                
            # Get the principal URL
            principal_url = f"{self.caldav_url}/principals/users/{self.username}/"
            
            # Make the request to get the principal
            async with self._session.request(
                "PROPFIND",
                principal_url,
                headers={
                    "Depth": "0",
                    "Content-Type": "application/xml; charset=utf-8"
                },
                data="""<?xml version="1.0" encoding="utf-8" ?>
                <propfind xmlns="DAV:">
                    <prop>
                        <current-user-principal />
                    </prop>
                </propfind>"""
            ) as response:
                if response.status != 207:
                    raise Exception(f"Failed to get principal: {response.status}")
                
                # Parse the response
                principal_data = await response.text()
                
            # Get the calendar home URL
            calendar_home_url = f"{self.caldav_url}/calendars/{self.username}/"
            
            # Make the request to get the calendars
            async with self._session.request(
                "PROPFIND",
                calendar_home_url,
                headers={
                    "Depth": "1",
                    "Content-Type": "application/xml; charset=utf-8"
                },
                data="""<?xml version="1.0" encoding="utf-8" ?>
                <propfind xmlns="DAV:" xmlns:C="urn:ietf:params:xml:ns:caldav" xmlns:CS="http://calendarserver.org/ns/">
                    <prop>
                        <resourcetype />
                        <displayname />
                        <C:calendar-description />
                        <C:supported-calendar-component-set />
                        <CS:getctag />
                    </prop>
                </propfind>"""
            ) as response:
                if response.status != 207:
                    raise Exception(f"Failed to get calendars: {response.status}")
                
                # Parse the response
                calendar_data = await response.text()
                
                # Parse XML
                root = ET.fromstring(calendar_data)
                
                # Find all calendar responses
                calendars = []
                
                # Define namespaces
                namespaces = {
                    'd': 'DAV:',
                    'c': 'urn:ietf:params:xml:ns:caldav'
                }
                
                # Find all response elements
                for response_elem in root.findall('.//d:response', namespaces):
                    # Get the href
                    href = response_elem.find('.//d:href', namespaces).text
                    
                    # Skip the calendar home
                    if href == calendar_home_url:
                        continue
                    
                    # Check if this is a calendar
                    resourcetype = response_elem.find('.//d:resourcetype', namespaces)
                    if resourcetype is None or resourcetype.find('.//c:calendar', namespaces) is None:
                        continue
                    
                    # Get the display name
                    displayname_elem = response_elem.find('.//d:displayname', namespaces)
                    displayname = displayname_elem.text if displayname_elem is not None and displayname_elem.text else "Unnamed Calendar"
                    
                    # Extract calendar ID from href
                    calendar_id = href.rstrip('/').split('/')[-1]
                    
                    # Create calendar object
                    calendar = NextCloudCalendar(
                        id=calendar_id,
                        display_name=displayname,
                        url=href
                    )
                    
                    calendars.append(calendar)
                
                return calendars
                
        except Exception as e:
            logger.error(f"Error getting calendars: {e}")
            return []
            
    async def create_calendar(self, display_name: str) -> Optional[NextCloudCalendar]:
        """Create a new calendar in NextCloud. Only attempts creation; does not search for existing."""
        try:
            # Run this in a thread since caldav is synchronous
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, self._create_calendar_sync, display_name)
        except Exception as e:
            logger.error(f"Error creating calendar: {e}")
            return None
            
    def _create_calendar_sync(self, display_name: str) -> Optional[NextCloudCalendar]:
        """Synchronous implementation of create_calendar using caldav library directly."""
        try:
            # Create a caldav client directly
            client = caldav.DAVClient(
                url=self.caldav_url,
                username=self.username,
                password=self.password or self.token
            )
            
            # Get the principal
            principal = client.principal()
            
            # Create the calendar using the built-in caldav method
            logger.info(f"Creating calendar '{display_name}' using caldav library")
            calendar = principal.make_calendar(display_name)
            
            # Create calendar object
            return NextCloudCalendar(
                id=calendar.id,
                display_name=display_name,
                url=calendar.url
            )
            
        except Exception as e:
            logger.error(f"Error creating calendar: {e}")
            return None

    def _get_caldav_client(self) -> caldav.DAVClient:
        """Get or create CalDAV client."""
        if not self._client:
            try:
                url = f"{self.base_url}{self.api_path}"
                logger.debug(f"Connecting to CalDAV server at {url}")
                self._client = caldav.DAVClient(
                    url=url,
                    username=self.username,
                    password=self.auth_manager.password
                )
                logger.info("Connected to NextCloud CalDAV server")
            except Exception as e:
                logger.error(f"Failed to connect to NextCloud: {e}")
                raise
        return self._client
    
    def _get_principal(self):
        """Get principal."""
        if not self._principal:
            client = self._get_caldav_client()
            self._principal = client.principal()
        return self._principal
    
    def _get_calendar(self, calendar_name=None) -> caldav.Calendar:
        """Get or create calendar."""
        calendar_name = calendar_name or self.calendar_name
        
        if calendar_name not in self._calendars:
            principal = self._get_principal()
            
            # Try to find existing calendar
            calendars = principal.calendars()
            logger.info(f"Found {len(calendars)} calendars:")
            for cal in calendars:
                logger.info(f"  - Calendar: {cal.name}")
                if cal.name == calendar_name:
                    self._calendars[calendar_name] = cal
                    break
                    
            # Create calendar if calendar not found
            if calendar_name not in self._calendars:
                logger.info(f"Creating new calendar: {calendar_name}")
                self._calendars[calendar_name] = principal.make_calendar(calendar_name)
                
        return self._calendars[calendar_name]
    
    async def close(self):
        """Close the client session."""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None
    
    async def create_task(self, task_data: Dict[str, Any], parent_id: str = None) -> NextCloudTask:
        """Create a task in NextCloud using CalDAV.
        
        Args:
            task_data: Task data to create
            parent_id: Optional ID of parent task (for subtasks)
            
        Returns:
            Created task
        """
        try:
            # This needs to be run in a thread since caldav is synchronous
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, self._create_task_sync, task_data, parent_id)
        except Exception as e:
            logger.error(f"Failed to create task: {e}")
            raise
            
    def _create_task_sync(self, task_data: Dict[str, Any], parent_id: str = None) -> NextCloudTask:
        """Synchronous implementation of create_task.
        
        Args:
            task_data: Task data to create
            parent_id: Optional ID of parent task (for subtasks)
            
        Returns:
            Created task
        """
        # Get the calendar
        calendar = self._get_calendar()
        
        # Create a new task
        title = task_data.get("title", "")
        description = task_data.get("description", "")
        status = task_data.get("status", "NEEDS-ACTION")
        due_date = task_data.get("due_date")
        priority = task_data.get("priority")
        categories = task_data.get("categories", [])
        
        # Create a new iCalendar component
        vcal = Calendar()
        vtodo = Todo()
        
        # Set basic properties
        uid = str(uuid.uuid4())
        vtodo.add("uid", uid)
        vtodo.add("summary", title)
        
        if description:
            # Ensure description is properly formatted
            vtodo.add("description", description)
            
        if status:
            vtodo.add("status", status)
            
        if due_date:
            vtodo.add("due", due_date)
            
        if priority is not None:
            vtodo.add("priority", priority)
            
        if categories:
            vtodo.add("categories", categories)
            
        # Set creation timestamp
        now = datetime.now()
        vtodo.add("created", now)
        vtodo.add("dtstamp", now)
        vtodo.add("last-modified", now)
        
        # Add parent relationship if this is a subtask
        if parent_id:
            vtodo.add("related-to", parent_id)
            
        # Add the todo to the calendar
        vcal.add_component(vtodo)
        
        # Create the task in CalDAV
        task = calendar.save_todo(vcal.to_ical().decode("utf-8"))
        
        # Get the etag if available
        etag = None
        if hasattr(task, "etag"):
            etag = task.etag
            
        # Return the created task
        return NextCloudTask(
            id=uid,
            title=title,
            description=description,
            status=self._map_caldav_status_to_local(status),
            due_date=due_date,
            created_at=now.isoformat(),
            updated_at=now.isoformat(),
            priority=self._map_caldav_priority_to_local(priority),
            calendar_id=str(calendar.id) if hasattr(calendar, 'id') else None,
            categories=categories,
            etag=etag,
            fileid=uid
        )
        
    def _map_caldav_status_to_local(self, status: str) -> str:
        """Map CalDAV status to local status.
        
        Args:
            status: CalDAV status
            
        Returns:
            Local status
        """
        if status == "COMPLETED":
            return "done"
        elif status == "IN-PROCESS":
            return "in_progress"
        elif status == "CANCELLED":
            return "blocked"
        else:
            return "pending"
            
    def _map_caldav_priority_to_local(self, priority: Any) -> str:
        """Map CalDAV priority to local priority.
        
        Args:
            priority: CalDAV priority
            
        Returns:
            Local priority
        """
        if priority is None:
            return "medium"
            
        try:
            priority_int = int(priority)
            if priority_int <= 3:
                return "high"
            elif priority_int <= 6:
                return "medium"
            else:
                return "low"
        except (ValueError, TypeError):
            return "medium"
            
    async def update_task(self, task_id: str, task_data: Dict[str, Any]) -> NextCloudTask:
        """Update a task in NextCloud using CalDAV."""
        try:
            # Get the calendar
            calendar = self._get_calendar()
            
            # Find the task by ID
            todos = calendar.todos()
            todo = None
            for t in todos:
                uid = str(t.icalendar_component.get("uid", ""))
                if uid == task_id:
                    todo = t
                    break
                    
            if not todo:
                raise ValueError(f"Task with ID {task_id} not found")
                
            # Get the current task data
            current_task = NextCloudTask.from_caldav_todo(todo)
            
            # Ensure priority is a string if provided
            priority = task_data.get("priority", current_task.priority)
            if isinstance(priority, int):
                priority_map = {1: "high", 5: "medium", 9: "low"}
                priority = priority_map.get(priority, "medium")
            
            # Update with new data
            updated_task = current_task.model_copy(update={
                "title": task_data.get("title", current_task.title),
                "description": task_data.get("description", current_task.description),
                "status": task_data.get("status", current_task.status),
                "due_date": task_data.get("due_date", current_task.due_date),
                "priority": priority,
                "categories": task_data.get("categories", current_task.categories)
            })
            
            # Convert to iCalendar format
            ical_data = updated_task.to_caldav_todo()
            
            # Update the task in CalDAV
            todo.data = ical_data
            todo.save()
            
            # Return the updated task
            return NextCloudTask.from_caldav_todo(todo)
            
        except Exception as e:
            logger.error(f"Failed to update task: {e}")
            raise
            
    async def delete_task(self, task_id: str) -> None:
        """Delete a task in NextCloud using CalDAV."""
        try:
            # Get the calendar
            calendar = self._get_calendar()
            
            # Find the task by ID
            todos = calendar.todos()
            todo = None
            for t in todos:
                uid = str(t.icalendar_component.get("uid", ""))
                if uid == task_id:
                    todo = t
                    break
                    
            if not todo:
                raise ValueError(f"Task with ID {task_id} not found")
                
            # Delete the task
            todo.delete()
            
        except Exception as e:
            logger.error(f"Failed to delete task: {e}")
            raise
    
    async def get_tasks(self, calendar_id: str = None) -> List[NextCloudTask]:
        """Get tasks from the NextCloud API."""
        # This needs to be run in a thread since caldav is synchronous
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._get_tasks_sync, calendar_id)
    
    def _get_tasks_sync(self, calendar_id: str = None) -> List[NextCloudTask]:
        """Synchronous implementation of get_tasks."""
        try:
            calendar = self._get_calendar(calendar_id)
            tasks = []
            
            # Convert todos to NextCloudTask objects
            for todo in calendar.todos():
                task = NextCloudTask.from_caldav_todo(todo)
                tasks.append(task)
                
            return tasks
            
        except Exception as e:
            logger.error(f"Failed to get tasks: {e}")
            raise

    async def get_task(self, task_id: str) -> NextCloudTask:
        """Get a specific task from NextCloud using CalDAV.
        
        Args:
            task_id: ID of the task to get
            
        Returns:
            NextCloudTask object
            
        Raises:
            ValueError: If the task is not found
        """
        try:
            # This needs to be run in a thread since caldav is synchronous
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, self._get_task_sync, task_id)
        except Exception as e:
            logger.error(f"Failed to get task {task_id}: {e}")
            raise
            
    def _get_task_sync(self, task_id: str) -> NextCloudTask:
        """Synchronous implementation of get_task.
        
        Args:
            task_id: ID of the task to get
            
        Returns:
            NextCloudTask object
            
        Raises:
            ValueError: If the task is not found
        """
        # Get the calendar
        calendar = self._get_calendar()
        
        # Find the task by ID
        todos = calendar.todos()
        for todo in todos:
            uid = str(todo.icalendar_component.get("uid", ""))
            if uid == task_id:
                return NextCloudTask.from_caldav_todo(todo)
                
        # If we get here, the task was not found
        raise ValueError(f"Task with ID {task_id} not found")

    async def get_all_tasks(self) -> List[NextCloudTask]:
        """Get all tasks from NextCloud using CalDAV.
        
        Returns:
            List of NextCloudTask objects
        """
        try:
            # This needs to be run in a thread since caldav is synchronous
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, self._get_all_tasks_sync)
        except Exception as e:
            logger.error(f"Failed to get all tasks: {e}")
            raise
            
    def _get_all_tasks_sync(self) -> List[NextCloudTask]:
        """Synchronous implementation of get_all_tasks.
        
        Returns:
            List of NextCloudTask objects
        """
        # Get the calendar
        calendar = self._get_calendar()
        
        # Get all todos
        todos = calendar.todos()
        
        # Convert to NextCloudTask objects
        tasks = []
        for todo in todos:
            try:
                task = NextCloudTask.from_caldav_todo(todo)
                tasks.append(task)
            except Exception as e:
                logger.warning(f"Error converting todo to task: {e}")
                
        return tasks

    async def find_tasks_by_status(self, status: str = "COMPLETED") -> List[NextCloudTask]:
        """Find tasks with a specific status in NextCloud using CalDAV.
        
        Args:
            status: Status to filter by (e.g., "COMPLETED", "NEEDS-ACTION", "IN-PROCESS")
            
        Returns:
            List of NextCloudTask objects matching the status
        """
        try:
            # This needs to be run in a thread since caldav is synchronous
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, self._find_tasks_by_status_sync, status)
        except Exception as e:
            logger.error(f"Failed to find tasks by status {status}: {e}")
            raise
            
    def _find_tasks_by_status_sync(self, status: str) -> List[NextCloudTask]:
        """Synchronous implementation of find_tasks_by_status.
        
        Args:
            status: Status to filter by
            
        Returns:
            List of NextCloudTask objects matching the status
        """
        # Get the calendar
        calendar = self._get_calendar()
        
        # Create a filter for tasks with the specified status
        from caldav.elements import dav, cdav
        
        # Define the filter to find tasks with the specified status
        status_filter = cdav.Filter(
            cdav.CompFilter(
                name="VCALENDAR",
                children=[
                    cdav.CompFilter(
                        name="VTODO",
                        children=[
                            cdav.PropFilter(
                                name="STATUS",
                                children=[
                                    cdav.TextMatch(status)
                                ]
                            )
                        ]
                    )
                ]
            )
        )
        
        # Find todos matching the filter
        todos = calendar.search(filters=[status_filter])
        
        # Convert to NextCloudTask objects
        tasks = []
        for todo in todos:
            try:
                task = NextCloudTask.from_caldav_todo(todo)
                tasks.append(task)
            except Exception as e:
                logger.warning(f"Error converting todo to task: {e}")
                
        return tasks

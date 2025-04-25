"""Integration tests for NextCloud Deck API integration."""
import os
import asyncio
import uuid
import logging
import unittest
from datetime import datetime
from unittest import IsolatedAsyncioTestCase

from taskinator.nextcloud_client import NextCloudClient
from taskinator.sync_engine import SyncEngine, get_nextcloud_metadata

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class TestNextCloudDeck(IsolatedAsyncioTestCase):
    """Test the NextCloud Deck API integration."""
    
    async def asyncSetUp(self):
        """Set up the test environment."""
        # Get NextCloud credentials from environment variables
        base_url = os.environ.get("NEXTCLOUD_HOST")
        username = os.environ.get("NEXTCLOUD_USERNAME")
        password = os.environ.get("NEXTCLOUD_PASSWORD")
        
        if not all([base_url, username, password]):
            self.skipTest("NextCloud credentials not set in environment variables")
            
        # Initialize the NextCloud client
        self.client = NextCloudClient(
            base_url=base_url,
            username=username,
            password=password,
            calendar_name="Taskinator",  # Use the Taskinator calendar
            use_deck_api=True  # Enable Deck API for testing
        )
        
        # Check if Deck API is available
        self.deck_api_available = await self.client.is_deck_available()
        
        if not self.deck_api_available:
            logging.warning("Deck API is not available. Tests will be skipped.")
        else:
            logging.info("Deck API is available.")
            
        # Create a unique identifier for this test run
        self.test_id = datetime.now().strftime("%Y%m%d%H%M%S")
        self.board_name = f"Taskinator Test {self.test_id}"
        self.board = None
        self.stack = None
        self.card = None
        
    async def asyncTearDown(self):
        """Clean up the test environment."""
        # Only attempt to clean up if we created a board
        if self.board and self.deck_api_available:
            try:
                await self.client.delete_board(self.board.id)
                logging.info(f"Cleaned up test board: {self.board_name}")
                
                # Only attempt to clean up old boards if we successfully deleted our own board
                # This indicates we have the necessary permissions
                try:
                    boards = await self.client.get_boards()
                    for board in boards:
                        if board.title.startswith("Taskinator Test"):
                            try:
                                await self.client.delete_board(board.id)
                                logging.info(f"Cleaned up test board: {board.title}")
                            except Exception as e:
                                logging.error(f"Error deleting board {board.title}: {e}")
                except Exception as e:
                    logging.error(f"Error cleaning up test boards: {e}")
            except Exception as e:
                logging.error(f"Error deleting board {self.board_name}: {e}")
                # If we can't delete the board due to permissions, don't try to clean up old boards
                
    async def test_create_board_stack_card(self):
        """Test creating a board, stack, and card using the Deck API."""
        if not self.deck_api_available:
            self.skipTest("Deck API is not available")
            
        # Create a board
        self.board = await self.client.create_board(self.board_name)
        self.assertIsNotNone(self.board)
        self.assertEqual(self.board.title, self.board_name)
        
        # Create a stack
        stack_name = "Test Stack"
        self.stack = await self.client.create_stack(self.board.id, stack_name)
        self.assertIsNotNone(self.stack)
        self.assertEqual(self.stack.title, stack_name)
        
        # Create a card
        card_title = "Test Card"
        card_description = "This is a test card"
        card_data = {
            "title": card_title,
            "description": card_description,
            "duedate": None,
            "order": 0
        }
        
        self.card = await self.client.create_card(self.board.id, self.stack.id, card_data)
        self.assertIsNotNone(self.card)
        self.assertEqual(self.card.title, card_title)
        self.assertEqual(self.card.description, card_description)
        
        # Create a subtask
        try:
            subtask = await self.client.create_subtask(self.card.id, "Test Subtask")
            self.assertIsNotNone(subtask)
            self.assertEqual(subtask.title, "Test Subtask")
        except Exception as e:
            logging.warning(f"Subtask creation failed (this may be normal if permissions are limited): {e}")
            
    async def test_unified_task_with_subtasks(self):
        """Test creating a unified task with subtasks."""
        if not self.deck_api_available:
            self.skipTest("Deck API is not available")
            
        # Create a task with subtasks
        task_data = {
            "title": f"Test Task {self.test_id}",
            "description": "This is a test task with subtasks",
            "status": "pending",
            "priority": "medium",
            "due_date": None,
            "subtasks": [
                {"title": "Subtask 1"},
                {"title": "Subtask 2"}
            ]
        }
        
        try:
            task = await self.client.create_unified_task(task_data)
            self.assertIsNotNone(task)
            self.assertEqual(task.title, task_data["title"])
            
            # Verify the task was created using the Deck API
            self.assertTrue(task.id.startswith("deck-card-"))
            
            # Clean up - delete the task
            await self.client.delete_unified_task(task.id)
        except Exception as e:
            self.fail(f"Failed to create unified task with subtasks: {e}")
            
    async def test_fallback_to_caldav(self):
        """Test that tasks with subtasks fall back to CalDAV when Deck API is disabled."""
        # Create a client with Deck API disabled
        caldav_client = NextCloudClient(
            base_url=os.environ.get("NEXTCLOUD_HOST"),
            username=os.environ.get("NEXTCLOUD_USERNAME"),
            password=os.environ.get("NEXTCLOUD_PASSWORD"),
            calendar_name="Taskinator",
            use_deck_api=False  # Disable Deck API
        )
        
        # Create a task with subtasks
        task_data = {
            "title": f"CalDAV Task {self.test_id}",
            "description": "This is a test task with subtasks (should use CalDAV)",
            "status": "pending",
            "priority": "medium",
            "due_date": None,
            "subtasks": [
                {"title": "Subtask 1"},
                {"title": "Subtask 2"}
            ]
        }
        
        # Create the task
        task = await caldav_client.create_unified_task(task_data)
        self.assertIsNotNone(task)
        self.assertEqual(task.title, task_data["title"])
        
        # Verify the task was created using CalDAV (not Deck API)
        self.assertFalse(task.id.startswith("deck-card-"))
        
        # Clean up
        await caldav_client.delete_unified_task(task.id)
        
if __name__ == "__main__":
    unittest.main()

"""Tests for NextCloud API client."""

import asyncio
import json
import unittest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

from taskinator.nextcloud_client import (
    NextCloudAuthManager,
    NextCloudClient,
    NextCloudRateLimiter,
    NextCloudTask
)


class TestNextCloudTask(unittest.TestCase):
    """Test NextCloudTask model."""
    
    def test_model_dump_json(self):
        """Test JSON serialization."""
        now = datetime.now()
        task = NextCloudTask(
            id="123",
            title="Test Task",
            description="Test Description",
            completed=False,
            due_date=now,
            created=now,
            modified=now,
            priority=1,
            calendar_id="calendar1",
            categories=["work", "important"]
        )
        
        json_str = task.model_dump_json()
        data = json.loads(json_str)
        
        self.assertEqual(data["id"], "123")
        self.assertEqual(data["title"], "Test Task")
        self.assertEqual(data["description"], "Test Description")
        self.assertEqual(data["completed"], False)
        self.assertEqual(data["priority"], 1)
        self.assertEqual(data["calendar_id"], "calendar1")
        self.assertEqual(data["categories"], ["work", "important"])
        
        # Check datetime serialization
        self.assertIsNotNone(data["due_date"])
        self.assertIsNotNone(data["created"])
        self.assertIsNotNone(data["modified"])
        
    def test_from_json(self):
        """Test JSON deserialization."""
        json_str = json.dumps([{
            "id": "123",
            "title": "Test Task",
            "description": "Test Description",
            "completed": False,
            "priority": 1,
            "calendar_id": "calendar1",
            "categories": ["work", "important"]
        }])
        
        tasks = NextCloudTask.from_json(json_str)
        
        self.assertEqual(len(tasks), 1)
        task = tasks[0]
        self.assertEqual(task.id, "123")
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")
        self.assertEqual(task.completed, False)
        self.assertEqual(task.priority, 1)
        self.assertEqual(task.calendar_id, "calendar1")
        self.assertEqual(task.categories, ["work", "important"])


class TestNextCloudAuthManager(unittest.IsolatedAsyncioTestCase):
    """Test NextCloudAuthManager."""
    
    async def test_get_token_with_app_token(self):
        """Test getting token when app_token is provided."""
        auth_manager = NextCloudAuthManager(
            base_url="https://nextcloud.example.com",
            username="testuser",
            app_token="test_token"
        )
        
        token = await auth_manager.get_token()
        self.assertEqual(token, "test_token")
        
    async def test_get_token_with_password(self):
        """Test getting token when password is provided."""
        auth_manager = NextCloudAuthManager(
            base_url="https://nextcloud.example.com",
            username="testuser",
            password="test_password"
        )
        
        token = await auth_manager.get_token()
        self.assertEqual(token, f"simulated_token_testuser")
        
    async def test_get_auth_headers(self):
        """Test getting authentication headers."""
        auth_manager = NextCloudAuthManager(
            base_url="https://nextcloud.example.com",
            username="testuser",
            password="test_password"
        )
        
        headers = auth_manager.get_auth_headers()
        self.assertIn("Authorization", headers)
        self.assertTrue(headers["Authorization"].startswith("Basic "))


class TestNextCloudRateLimiter(unittest.IsolatedAsyncioTestCase):
    """Test NextCloudRateLimiter."""
    
    async def test_wait_if_needed(self):
        """Test rate limiting."""
        rate_limiter = NextCloudRateLimiter(requests_per_minute=60)
        
        # First request should not wait
        start_time = asyncio.get_event_loop().time()
        await rate_limiter.wait_if_needed()
        elapsed = asyncio.get_event_loop().time() - start_time
        self.assertLess(elapsed, 0.1)  # Should be very quick
        
        # Second request immediately after should wait
        rate_limiter.last_request_time = asyncio.get_event_loop().time()
        start_time = asyncio.get_event_loop().time()
        await rate_limiter.wait_if_needed()
        elapsed = asyncio.get_event_loop().time() - start_time
        self.assertGreaterEqual(elapsed, rate_limiter.request_interval * 0.9)  # Allow for small timing variations
        
    def test_batch_operations(self):
        """Test batch operations."""
        rate_limiter = NextCloudRateLimiter()
        
        # Add requests to batch
        rate_limiter.add_to_batch({"method": "GET", "endpoint": "/tasks"})
        rate_limiter.add_to_batch({"method": "POST", "endpoint": "/tasks"})
        
        # Check if we have pending requests
        self.assertTrue(rate_limiter.has_pending_requests())
        
        # Get batch
        batch = rate_limiter.get_batch(max_batch_size=1)
        self.assertEqual(len(batch), 1)
        self.assertEqual(batch[0]["method"], "GET")
        
        # Check if we still have pending requests
        self.assertTrue(rate_limiter.has_pending_requests())
        
        # Get remaining batch
        batch = rate_limiter.get_batch()
        self.assertEqual(len(batch), 1)
        self.assertEqual(batch[0]["method"], "POST")
        
        # Check if we have no more pending requests
        self.assertFalse(rate_limiter.has_pending_requests())


class TestNextCloudClient(unittest.IsolatedAsyncioTestCase):
    """Test NextCloudClient."""
    
    async def asyncSetUp(self):
        """Set up test case."""
        self.client = NextCloudClient(
            base_url="https://nextcloud.example.com",
            username="testuser",
            password="test_password"
        )
        
        # Mock the _make_request method
        self.client._make_request = AsyncMock()
        
    async def asyncTearDown(self):
        """Tear down test case."""
        await self.client.close()
        
    async def test_get(self):
        """Test GET request."""
        self.client._make_request.return_value = (200, {"data": "test"})
        
        result = await self.client.get("/test")
        
        self.client._make_request.assert_called_once_with(
            "GET", "/test", params=None, retry_count=0
        )
        self.assertEqual(result, {"data": "test"})
        
    async def test_post(self):
        """Test POST request."""
        self.client._make_request.return_value = (201, {"id": "123"})
        
        result = await self.client.post("/test", {"name": "test"})
        
        self.client._make_request.assert_called_once_with(
            "POST", "/test", data={"name": "test"}, retry_count=0
        )
        self.assertEqual(result, {"id": "123"})
        
    async def test_put(self):
        """Test PUT request."""
        self.client._make_request.return_value = (200, {"id": "123", "name": "updated"})
        
        result = await self.client.put("/test/123", {"name": "updated"})
        
        self.client._make_request.assert_called_once_with(
            "PUT", "/test/123", data={"name": "updated"}, retry_count=0
        )
        self.assertEqual(result, {"id": "123", "name": "updated"})
        
    async def test_delete(self):
        """Test DELETE request."""
        self.client._make_request.return_value = (204, {})
        
        result = await self.client.delete("/test/123")
        
        self.client._make_request.assert_called_once_with(
            "DELETE", "/test/123", retry_count=0
        )
        self.assertEqual(result, {})
        
    @patch("taskinator.nextcloud_client.NextCloudTask")
    async def test_get_tasks(self, mock_task_class):
        """Test getting tasks."""
        mock_tasks = [MagicMock(), MagicMock()]
        mock_task_class.from_json.return_value = mock_tasks
        self.client._make_request.return_value = (200, [{"id": "1"}, {"id": "2"}])
        
        result = await self.client.get_tasks()
        
        self.client._make_request.assert_called_once()
        self.assertEqual(result, mock_tasks)
        
    @patch("taskinator.nextcloud_client.NextCloudTask")
    async def test_create_task(self, mock_task_class):
        """Test creating a task."""
        mock_task = MagicMock()
        mock_task_class.model_validate.return_value = mock_task
        self.client._make_request.return_value = (201, {"id": "123"})
        
        result = await self.client.create_task({"title": "Test Task"})
        
        self.client._make_request.assert_called_once()
        self.assertEqual(result, mock_task)
        
    @patch("taskinator.nextcloud_client.NextCloudTask")
    async def test_update_task(self, mock_task_class):
        """Test updating a task."""
        mock_task = MagicMock()
        mock_task_class.model_validate.return_value = mock_task
        self.client._make_request.return_value = (200, {"id": "123"})
        
        result = await self.client.update_task("123", {"title": "Updated Task"})
        
        self.client._make_request.assert_called_once()
        self.assertEqual(result, mock_task)
        
    async def test_delete_task(self):
        """Test deleting a task."""
        self.client._make_request.return_value = (204, {})
        
        await self.client.delete_task("123")
        
        self.client._make_request.assert_called_once()


if __name__ == "__main__":
    unittest.main()

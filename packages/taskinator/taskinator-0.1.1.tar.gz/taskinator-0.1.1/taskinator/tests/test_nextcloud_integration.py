import os
import asyncio
import unittest
import logging
from datetime import datetime
from taskinator.nextcloud_client import NextCloudClient
from taskinator.sync_engine import SyncEngine
from taskinator.nextcloud_sync import get_nextcloud_metadata

# Configure logging to show debug messages
logging.basicConfig(level=logging.DEBUG)

class TestNextCloudIntegration(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.host = os.environ.get("NEXTCLOUD_HOST")
        self.username = os.environ.get("NEXTCLOUD_USERNAME")
        self.password = os.environ.get("NEXTCLOUD_PASSWORD")
        assert self.host and self.username and self.password, (
            "NEXTCLOUD_HOST, NEXTCLOUD_USERNAME, and NEXTCLOUD_PASSWORD must be set as environment variables."
        )
        
        # Create the NextCloud client
        self.client = NextCloudClient(
            base_url=self.host,
            username=self.username,
            password=self.password
        )
        self.sync_engine = SyncEngine(self.client)
        
        # Clean up any existing test tasks
        await self.cleanup_test_tasks()

    async def asyncTearDown(self):
        # Clean up after tests
        await self.cleanup_test_tasks()
        await self.client.close()
        
    async def cleanup_test_tasks(self):
        """Clean up any test tasks that might have been created."""
        try:
            tasks = await self.client.get_tasks()
            for task in tasks:
                if task.title.startswith("Integration Test Task"):
                    await self.client.delete_task(task.id)
                    logging.info(f"Cleaned up test task: {task.id}")
        except Exception as e:
            logging.error(f"Error cleaning up test tasks: {e}")

    async def test_create_and_sync_task(self):
        # Create a new unique task
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        task = {
            "id": f"int-{now}",
            "title": f"Integration Test Task {now}",
            "description": "Created by integration test",
            "status": "pending",
            "priority": "medium",
            "nextcloud": {}
        }
        
        # Push to NextCloud
        updated_task = await self.sync_engine.sync_task(task)
        metadata = get_nextcloud_metadata(updated_task)
        
        print("ETag from NextCloud:", metadata.etag)
        print("FileID from NextCloud:", metadata.fileid)
        
        # Either etag or fileid should be present for successful sync
        self.assertTrue(metadata.etag or metadata.fileid, 
                       "Either ETag or FileID should be present after sync.")
        
        # Verify the task was created in NextCloud
        tasks = await self.client.get_tasks()
        found = False
        for remote_task in tasks:
            if remote_task.title == task["title"]:
                found = True
                break
                
        self.assertTrue(found, "Task should exist in NextCloud after sync")

if __name__ == "__main__":
    unittest.main()

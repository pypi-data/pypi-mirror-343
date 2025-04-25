#!/usr/bin/env python3
"""
Script to read a task from NextCloud and display its contents.
This helps debug synchronization issues by showing what data is actually stored in NextCloud.
"""

import asyncio
import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv
from taskinator.nextcloud_client import NextCloudClient
from taskinator.external_integration.sync_metadata_store import SyncMetadataStore
from taskinator.utils import read_json
from loguru import logger

load_dotenv()

async def main():
    # Get NextCloud credentials
    nextcloud_host = os.getenv("NEXTCLOUD_HOST")
    nextcloud_username = os.getenv("NEXTCLOUD_USERNAME")
    nextcloud_password = os.getenv("NEXTCLOUD_PASSWORD")
    nextcloud_token = os.getenv("NEXTCLOUD_TOKEN")
    
    # Check if credentials are available
    if not nextcloud_host:
        print("NextCloud host not found in environment variables.")
        print("Please set NEXTCLOUD_HOST, NEXTCLOUD_USERNAME, and either NEXTCLOUD_PASSWORD or NEXTCLOUD_TOKEN.")
        return
    
    # Initialize NextCloud client
    print(f"Connecting to NextCloud at {nextcloud_host}...")
    client = NextCloudClient(
        host=nextcloud_host,
        username=nextcloud_username or "testuser",
        password=nextcloud_password,
        token=nextcloud_token,
        calendar_name="Taskinator"
    )
    
    # Load tasks to get external IDs
    tasks_file = "tasks/tasks.json"
    print(f"Reading tasks from {tasks_file}...")
    data = read_json(tasks_file)
    tasks = data.get("tasks", [])
    
    # Initialize metadata store
    metadata_store = SyncMetadataStore(Path(tasks_file).parent)
    
    # Find tasks with NextCloud metadata
    nextcloud_tasks = []
    for task in tasks:
        task_id = task.get("id")
        metadata = metadata_store.get_metadata(task_id, "nextcloud")
        
        if metadata and metadata.get("external_id"):
            nextcloud_tasks.append({
                "task_id": task_id,
                "title": task.get("title", ""),
                "external_id": metadata["external_id"],
                "last_sync": metadata.get("last_sync", 0)
            })
    
    if not nextcloud_tasks:
        print("No tasks with NextCloud metadata found.")
        return
    
    print(f"Found {len(nextcloud_tasks)} tasks with NextCloud metadata.")
    
    # Get all tasks from NextCloud
    print("Getting all tasks from NextCloud...")
    try:
        nc_tasks = await client.get_tasks()
        print(f"Retrieved {len(nc_tasks)} tasks from NextCloud.")
        
        # Display tasks
        for i, nc_task in enumerate(nc_tasks):
            print(f"\n--- NextCloud Task {i+1} ---")
            print(f"ID: {nc_task.id}")
            print(f"Title: {nc_task.title}")
            
            # Display raw JSON
            print("\nRaw Task Data:")
            task_dict = nc_task.model_dump()
            print(json.dumps(task_dict, indent=2, default=str))
            
            # Check if this task matches one of our local tasks
            matched = False
            for local_task in nextcloud_tasks:
                if str(local_task["external_id"]) == str(nc_task.id):
                    print(f"Matches local task ID: {local_task['task_id']} - {local_task['title']}")
                    matched = True
                    break
            
            if not matched:
                print("No matching local task found.")
            
            # Get detailed task info
            try:
                print("\nGetting detailed task info...")
                task_detail = await client.get_task(nc_task.id)
                
                # Display raw JSON for detailed task
                print("\nRaw Detailed Task Data:")
                detail_dict = task_detail.model_dump()
                print(json.dumps(detail_dict, indent=2, default=str))
                
                # Get raw iCalendar data
                print("\nRaw iCalendar Data:")
                try:
                    # This is a bit of a hack to get the raw iCalendar data
                    # We're using a private method, but it's the most direct way
                    calendar = client._get_calendar()
                    todos = calendar.todos()
                    for todo in todos:
                        if str(todo.icalendar_component.get("uid", "")) == nc_task.id:
                            print(todo.data)
                            break
                except Exception as e:
                    print(f"Error getting raw iCalendar data: {e}")
                
            except Exception as e:
                print(f"Error getting task details: {e}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())

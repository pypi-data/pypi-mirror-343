"""Migration script to add external integration fields to existing tasks."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

from ..utils import read_json, write_json, log
from ..external_integration import ExternalSyncMetadata, SyncStatus, ExternalSystem

def migrate_tasks(tasks_file: Path) -> None:
    """Add external integration fields to all tasks in the tasks.json file.
    
    Args:
        tasks_file: Path to the tasks.json file
    """
    logger.info(f"Migrating tasks in {tasks_file} to add external integration fields")
    
    try:
        # Read the current tasks file
        data = read_json(tasks_file)
        
        if not data or 'tasks' not in data:
            logger.warning(f"No tasks found in {tasks_file}")
            return
            
        # Track if any changes were made
        changes_made = False
        
        # Update each task with external integration fields
        for task in data['tasks']:
            # Handle migration from old nextcloud field to new external_sync field
            if 'nextcloud' in task and 'external_sync' not in task:
                # Convert old nextcloud metadata to new format
                nextcloud_data = task['nextcloud']
                
                # Create external sync metadata for NextCloud
                external_metadata = ExternalSyncMetadata(
                    system=ExternalSystem.NEXTCLOUD,
                    external_id=nextcloud_data.get('fileid', ''),
                    etag=nextcloud_data.get('etag', ''),
                    last_sync=nextcloud_data.get('last_sync'),
                    sync_status=nextcloud_data.get('sync_status', SyncStatus.PENDING),
                    version_history=nextcloud_data.get('version_history', [])
                )
                
                # Add to task
                task['external_sync'] = [external_metadata.to_dict()]
                
                # Keep the old nextcloud field for backward compatibility
                # but mark it as deprecated
                if 'additional_data' not in task['external_sync'][0]:
                    task['external_sync'][0]['additional_data'] = {}
                task['external_sync'][0]['additional_data']['migrated_from_legacy'] = True
                
                changes_made = True
                logger.debug(f"Migrated NextCloud metadata for task {task.get('id')}")
            elif 'external_sync' not in task:
                # Add empty external_sync array if it doesn't exist
                task['external_sync'] = []
                changes_made = True
                logger.debug(f"Added empty external_sync array for task {task.get('id')}")
        
        # Save the updated tasks file if changes were made
        if changes_made:
            logger.info(f"Saving updated tasks with external integration fields to {tasks_file}")
            write_json(tasks_file, data)
            logger.info("Migration completed successfully")
        else:
            logger.info("No changes needed, all tasks already have external integration fields")
            
    except Exception as e:
        logger.error(f"Error migrating tasks: {e}")
        raise

def run_migration(tasks_file: Path) -> None:
    """Run the migration to add external integration fields.
    
    Args:
        tasks_file: Path to the tasks.json file
    """
    logger.info("Starting external integration fields migration")
    migrate_tasks(tasks_file)
    logger.info("External integration fields migration completed")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        tasks_path = Path(sys.argv[1])
    else:
        from ..config import config
        tasks_path = config.tasks_dir / "tasks.json"
        
    run_migration(tasks_path)

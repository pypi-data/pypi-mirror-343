"""Migration script to add NextCloud-specific fields to existing tasks."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

from ..utils import read_json, write_json, log

def migrate_tasks(tasks_file: Path) -> None:
    """Add NextCloud-specific fields to all tasks in the tasks.json file.
    
    Args:
        tasks_file: Path to the tasks.json file
    """
    logger.info(f"Migrating tasks in {tasks_file} to add NextCloud fields")
    
    try:
        # Read the current tasks file
        data = read_json(tasks_file)
        
        if not data or 'tasks' not in data:
            logger.warning(f"No tasks found in {tasks_file}")
            return
            
        # Track if any changes were made
        changes_made = False
        
        # Update each task with NextCloud fields
        for task in data['tasks']:
            if 'nextcloud' not in task:
                # Add NextCloud metadata if it doesn't exist
                task['nextcloud'] = {
                    'etag': '',
                    'fileid': '',
                    'last_sync': None,
                    'sync_status': 'pending',
                    'version_history': []
                }
                changes_made = True
            else:
                # Ensure all required fields exist in the nextcloud metadata
                nextcloud = task['nextcloud']
                if 'etag' not in nextcloud:
                    nextcloud['etag'] = ''
                    changes_made = True
                if 'fileid' not in nextcloud:
                    nextcloud['fileid'] = ''
                    changes_made = True
                if 'last_sync' not in nextcloud:
                    nextcloud['last_sync'] = None
                    changes_made = True
                if 'sync_status' not in nextcloud:
                    nextcloud['sync_status'] = 'pending'
                    changes_made = True
                if 'version_history' not in nextcloud:
                    nextcloud['version_history'] = []
                    changes_made = True
        
        # Save the updated tasks file if changes were made
        if changes_made:
            logger.info(f"Saving updated tasks with NextCloud fields to {tasks_file}")
            write_json(tasks_file, data)
            logger.info("Migration completed successfully")
        else:
            logger.info("No changes needed, all tasks already have NextCloud fields")
            
    except Exception as e:
        logger.error(f"Error migrating tasks: {e}")
        raise

def run_migration(tasks_file: Path) -> None:
    """Run the migration to add NextCloud fields.
    
    Args:
        tasks_file: Path to the tasks.json file
    """
    logger.info("Starting NextCloud fields migration")
    migrate_tasks(tasks_file)
    logger.info("NextCloud fields migration completed")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        tasks_path = Path(sys.argv[1])
    else:
        from ..config import config
        tasks_path = config.tasks_dir / "tasks.json"
        
    run_migration(tasks_path)

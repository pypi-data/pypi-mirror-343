"""NextCloud tasks tools."""
from typing import List, Optional
from datetime import datetime
from agno.tools import Toolkit
from agno.utils.log import logger
import caldav

from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class NextCloudTask(BaseModel):
    """NextCloud task data."""
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        ser_json_timedelta='iso8601',
        ser_json_bytes='base64',
        json_schema_serialization_defaults_required=True
    )

    id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    due_date: Optional[datetime] = None
    created: Optional[datetime] = None
    modified: Optional[datetime] = None
    priority: Optional[int] = None
    calendar_id: Optional[str] = None
    categories: List[str] = []

    def model_dump_json(self, **kwargs) -> str:
        """Custom JSON serialization."""
        def serialize_datetime(dt: datetime) -> str:
            return dt.isoformat() if dt else None
            
        data = self.model_dump()
        if self.due_date:
            data['due_date'] = serialize_datetime(self.due_date)
        if self.created:
            data['created'] = serialize_datetime(self.created)
        if self.modified:
            data['modified'] = serialize_datetime(self.modified)
            
        import json
        return json.dumps(data, **kwargs)

    @classmethod
    def from_json(cls, json_str: str) -> List["NextCloudTask"]:
        """Deserialize a JSON string containing a list of tasks.
        
        Args:
            json_str: JSON string containing an array of tasks
            
        Returns:
            List of NextCloudTask instances
        """
        import json
        data = json.loads(json_str)
        return [cls.model_validate(item) for item in data]

class NextCloudTasksTools(Toolkit):
    def __init__(
        self,
        url: str,
        username: str,
        password: str,
        calendar_name: str = "Tasks",
    ):
        """Initialize NextCloud Tasks toolkit."""
        super().__init__(name="nextcloud_tasks")
        self.url = f"{url}/remote.php/dav"  # CalDAV endpoint
        self.username = username
        self.password = password
        self.calendar_name = calendar_name
        self._client = None
        self._calendar = None
        
        # Register methods
        self.register(self.create_task)
        self.register(self.list_tasks)
        self.register(self.get_task)
        self.register(self.update_task)
        self.register(self.complete_task)
        self.register(self.delete_task)
        self.register(self.clear_all_tasks)
        self._client = self._get_client()
        self._calendar = self._get_calendar()

    def _get_client(self) -> caldav.DAVClient:
        """Get or create CalDAV client."""
        if not self._client:
            try:
                self._client = caldav.DAVClient(
                    url=self.url,
                    username=self.username,
                    password=self.password
                )
                logger.info("Connected to NextCloud CalDAV server")
            except Exception as e:
                logger.error(f"Failed to connect to NextCloud: {e}")
                raise
        return self._client

    def _get_principal(self):
        """Get principal."""
        client = self._get_client()
        return client.principal()

    def _get_calendar(self) -> caldav.Calendar:
        """Get or create Tasks calendar."""
        if not self._calendar:
            principal = self._get_principal()
            
            # Try to find existing calendar
            calendars = principal.calendars()
            logger.info(f"Found {len(calendars)} calendars:")
            for cal in calendars:
                logger.info(f"  - Calendar: {cal.name}")
                if cal.name == self.calendar_name:
                    self._calendar = cal
                    break
                    
            # Create calendar if calendar not found
            if not self._calendar:
                self._calendar = principal.make_calendar(self.calendar_name)
                
        return self._calendar

    def _to_task(self, todo) -> NextCloudTask:
        """Convert CalDAV todo to NextCloudTask."""
        data = todo.icalendar_component
        uid = str(data.get("uid", todo.id))
        
        # Extract fields from the component
        summary = str(data.get("summary", ""))
        description = str(data.get("description", ""))
        status = str(data.get("status", ""))
        priority = data.get("priority")
        
        # Get due date
        due_date = None
        if "due" in data:
            try:
                due_date = data["due"].dt
            except (AttributeError, ValueError):
                pass
                
        # Get created/modified dates
        created = None
        if "created" in data:
            try:
                created = data["created"].dt
            except (AttributeError, ValueError):
                pass
                
        modified = None
        if "last-modified" in data:
            try:
                modified = data["last-modified"].dt
            except (AttributeError, ValueError):
                pass
                
        # Get categories
        categories = []
        if data.get("categories"):
            categories = [str(cat) for cat in data.get("categories")]
        
        return NextCloudTask(
            id=uid,
            title=summary,
            description=description,
            completed=status == "COMPLETED",
            due_date=due_date,
            created=created,
            modified=modified,
            priority=priority,
            calendar_id=self._calendar.id,
            categories=categories
        )

    def create_task(
        self,
        summary: str,
        due_date: Optional[datetime] = None,
        description: Optional[str] = None,
        priority: Optional[int] = None,
        categories: Optional[List[str]] = None,
    ) -> str:
        """Create a new task.
        
        Args:
            summary: Task title/summary
            due_date: Optional due date
            description: Optional detailed description
            priority: Optional priority (1-9, will be clamped)
            categories: Optional list of categories/tags
            
        Returns:
            JSON string representation of created task
        """
        try:
            calendar = self._get_calendar()

            # Build task data
            task_data = {
                "summary": summary,
                "status": "NEEDS-ACTION"
            }
            
            if description:
                task_data["description"] = description
            if due_date:
                task_data["due"] = due_date
            if priority is not None:
                # Clamp priority between 1-9
                task_data["priority"] = max(1, min(9, priority))
            if categories:
                task_data["categories"] = categories

            logger.info(f"Creating task with data: {task_data}")
            task = calendar.save_todo(**task_data)
            logger.info(f"Created task with ID: {task.id}")

            # Return task object as JSON
            return self._to_task(task).model_dump_json(indent=2)

        except Exception as e:
            logger.error(f"Failed to create task: {e}")
            raise

    def get_task(self, uid: str) -> str:
        """Get task by UID.
        
        Args:
            uid: Task UID to retrieve
            
        Returns:
            JSON string representation of the task
        """
        try:
            calendar = self._get_calendar()
            
            # Get task and update fields
            task = None
            for todo in calendar.todos():
                if str(todo.icalendar_component.get("uid", todo.id)) == uid:
                    task = todo
                    break
                    
            if not task:
                raise ValueError(f"Task {uid} not found")
                
            # Return task as JSON
            if task:
                return self._to_task(task).model_dump_json(indent=2)
            else:
                return "{}"  # Return empty JSON object if not found
            
        except Exception as e:
            logger.error(f"Failed to get task {uid}: {e}")
            raise

    def list_tasks(self, include_completed: bool = False) -> str:
        """List all tasks.
        
        Args:
            include_completed: Whether to include completed tasks
            
        Returns:
            JSON string containing array of tasks
        """
        try:
            calendar = self._get_calendar()
            tasks = []
            
            # Convert todos to NextCloudTask objects and filter by completion status
            for todo in calendar.todos():
                task = self._to_task(todo)
                if include_completed or not task.completed:
                    tasks.append(task)
                
            # Return tasks as JSON array
            return f"[{','.join(t.model_dump_json(indent=2) for t in tasks)}]"
            
        except Exception as e:
            logger.error(f"Failed to list tasks: {e}")
            raise

    def update_task(
        self,
        uid: str,
        summary: Optional[str] = None,
        due_date: Optional[datetime] = None,
        description: Optional[str] = None,
        priority: Optional[int] = None,
        categories: Optional[List[str]] = None,
        completed: Optional[bool] = None,
    ) -> str:
        """Update an existing task."""
        try:
            calendar = self._get_calendar()
            
            # Get task and update fields
            task = None
            for todo in calendar.todos():
                if str(todo.icalendar_component.get("uid", todo.id)) == uid:
                    task = todo
                    break
                  
            if task is None:
                raise ValueError(f"Task not found: {uid}")
                    
            data = task.icalendar_component
                    
            # Update fields if provided
            if summary is not None:
                data["summary"] = summary
            if description is not None:
                data["description"] = description
            if due_date is not None:
                # Create a new vDDDTypes instance for the due date
                from icalendar import vDDDTypes
                data["due"] = vDDDTypes(due_date.replace(microsecond=0))
            if priority is not None:
                data["priority"] = max(1, min(9, priority))  # Clamp between 1-9
            if categories is not None:
                data["categories"] = categories
            if completed is not None:
                data["status"] = "COMPLETED" if completed else "NEEDS-ACTION"
                        
            # Save updated task
            task.save()
            
            # Return updated task details
            return self.get_task(uid)
            
        except Exception as e:
            logger.error(f"Failed to update task {uid}: {e}")
            raise

    def complete_task(self, uid: str) -> str:
        """Mark a task as completed."""
        try:
            calendar = self._get_calendar()
            
            # Find task by UID
            todos = calendar.todos(include_completed=True)  # Include completed tasks
            logger.info(f"Looking for task {uid} to complete in {len(todos)} todos")
            
            for todo in todos:
                data = todo.icalendar_component
                task_uid = str(data.get("uid", todo.id))
                logger.info(f"Checking task {task_uid} with status {data.get('status')}")
                if task_uid == uid:
                    logger.info(f"Found task {uid}, marking as completed. Current data: {data}")
                    # Set task status to COMPLETED
                    data["status"] = "COMPLETED"
                    todo.save()
                    logger.info(f"Saved task {uid} with completed status")
                    return self.get_task(uid)
                    
            logger.error(f"Task {uid} not found to complete. Available tasks: {[str(t.icalendar_component.get('uid', t.id)) for t in todos]}")
            raise ValueError(f"Task not found: {uid}")
                
        except Exception as e:
            logger.error(f"Failed to complete task {uid}: {e}")
            raise

    def delete_task(self, uid: str) -> bool:
        """Delete a task."""
        try:
            calendar = self._get_calendar()
            
            # Find task by UID
            for task in calendar.todos():
                if str(task.icalendar_component.get("uid", task.id)) == uid:
                    task.delete()
                    return True
            
            raise ValueError(f"Task not found: {uid}")
            
        except Exception as e:
            logger.error(f"Failed to delete task {uid}: {e}")
            raise

    def clear_all_tasks(self) -> None:
        """Delete all tasks from the calendar."""
        try:
            calendar = self._get_calendar()
            for task in calendar.todos():
                task.delete()
        except Exception as e:
            logger.error(f"Failed to clear tasks: {e}")
            raise

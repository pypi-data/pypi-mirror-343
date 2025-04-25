"""Constants for Taskinator."""

from enum import Enum, auto

class SyncStatus:
    """Synchronization status constants."""
    SYNCED = "synced"
    ERROR = "error"
    CONFLICT = "conflict"
    SKIPPED = "skipped"
    PENDING = "pending"
    LINKED = "linked"

class ExternalSystem(str, Enum):
    """External system constants."""
    NEXTCLOUD = "nextcloud"

class SyncDirection(str, Enum):
    """Synchronization direction constants."""
    BIDIRECTIONAL = "bidirectional"
    PUSH = "push"
    PULL = "pull"

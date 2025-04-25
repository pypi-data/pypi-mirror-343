from typing import Optional, List, ForwardRef, Union, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime




class OutcomeSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    name: str = Field(default=None, max_length=30)
    description: str = Field(default=None)
    success_criteria: str = Field(default=None, max_length=2048)
    target_date: Optional[datetime] = Field(default=None)
    priority: float = Field(default=None)
    status: Optional[str] = Field(default=None, max_length=255)
    value_proposition: Optional[str] = Field(default=None, max_length=1024)
    progress_percentage: float = Field(default=None)
    last_updated: datetime = Field(default=None)
    created: datetime = Field(default=None)

    # Relationships
    epoch: Optional["EpochSchema"] = Field(default=None)
    owner: Optional["ActorSchema"] = Field(default=None)
    contributors: List["ActorSchema"] = Field(default_factory=list)
    parent_outcome: Optional["OutcomeSchema"] = Field(default=None)
    dependent_outcomes: List["OutcomeSchema"] = Field(default_factory=list)
    memory_bank: Optional["MemoryBankSchema"] = Field(default=None)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class MemoryBankSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    name: str = Field(default=None, max_length=30)
    created: datetime = Field(default=None)
    last_updated: datetime = Field(default=None)

    # Relationships
    objective_brief: Optional["MemoryBankFileSchema"] = Field(default=None)
    purpose_context: Optional["MemoryBankFileSchema"] = Field(default=None)
    active_context: Optional["MemoryBankFileSchema"] = Field(default=None)
    structural_patterns: Optional["MemoryBankFileSchema"] = Field(default=None)
    resource_context: Optional["MemoryBankFileSchema"] = Field(default=None)
    progress: Optional["MemoryBankFileSchema"] = Field(default=None)
    objective_intelligence: Optional["MemoryBankFileSchema"] = Field(default=None)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class FileSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    url: Optional[str] = Field(default=None, max_length=2048)
    filepath: Optional[str] = Field(default=None, max_length=2048)
    content: Optional[str] = Field(default=None)
    mime_type: Optional[str] = Field(default=None, max_length=100)
    created_at: datetime = Field(default=None)
    last_updated: datetime = Field(default=None)

    # Relationships
    created_by: Optional["ActorSchema"] = Field(default=None)
    related_outcome: Optional["OutcomeSchema"] = Field(default=None)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class ReportSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    title: Optional[str] = Field(default=None, max_length=255)
    summary: str = Field(default=None, max_length=2048)
    content: Optional[str] = Field(default=None)
    format: Optional[str] = Field(default=None, max_length=50)
    status: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default=None)
    last_updated: datetime = Field(default=None)

    # Relationships
    author: Optional["ActorSchema"] = Field(default=None)
    primary_outcome: Optional["OutcomeSchema"] = Field(default=None)
    related_outcomes: List["OutcomeSchema"] = Field(default_factory=list)
    images: List["ImageSchema"] = Field(default_factory=list)
    files: List["FileSchema"] = Field(default_factory=list)
    generated_from: Optional["RunResponseSchema"] = Field(default=None)
    follow_up_meeting: Optional["MeetingSchema"] = Field(default=None)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class ReasoningStepSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    title: Optional[str] = Field(default=None, max_length=255)
    action: Optional[str] = Field(default=None)
    result: Optional[str] = Field(default=None)
    reasoning: Optional[str] = Field(default=None)
    next_action: Optional[str] = Field(default=None, max_length=30)
    confidence: Optional[float] = Field(default=None)
    step_number: int = Field(default=None)
    created_at: datetime = Field(default=None)

    # Relationships
    run_response: Optional["RunResponseSchema"] = Field(default=None)
    outcome: Optional["OutcomeSchema"] = Field(default=None)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class MemoryBankFileSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    name: str = Field(default=None, max_length=30)
    content: Optional[str] = Field(default=None)
    file_type: str = Field(default=None, max_length=30)
    created: datetime = Field(default=None)
    last_updated: datetime = Field(default=None)

    # Relationships
    memory_bank: Optional["MemoryBankSchema"] = Field(default=None)
    created_by: Optional["ActorSchema"] = Field(default=None)
    last_updated_by: Optional["ActorSchema"] = Field(default=None)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class MemoryBankFileVersionSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    content: Optional[str] = Field(default=None)
    version_number: int = Field(default=None)
    change_summary: Optional[str] = Field(default=None, max_length=1024)
    created: datetime = Field(default=None)

    # Relationships
    file: Optional["MemoryBankFileSchema"] = Field(default=None)
    created_by: Optional["ActorSchema"] = Field(default=None)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class RunResponseSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    content: Optional[str] = Field(default=None)
    content_type: str = Field(default=None, max_length=50)
    thinking: Optional[str] = Field(default=None)
    event: str = Field(default=None, max_length=50)
    metrics: Optional[str] = Field(default=None)
    model: Optional[str] = Field(default=None, max_length=100)
    run_id: Optional[str] = Field(default=None, max_length=100)
    agent_identifier: Optional[str] = Field(default=None, max_length=100)
    session_id: Optional[str] = Field(default=None, max_length=100)
    workflow_id: Optional[str] = Field(default=None, max_length=100)
    tools: Optional[str] = Field(default=None)
    formatted_tool_calls: Optional[str] = Field(default=None)
    citations: Optional[str] = Field(default=None)
    extra_data: Optional[str] = Field(default=None)
    created_at: datetime = Field(default=None)
    last_updated: datetime = Field(default=None)

    # Relationships
    outcome: Optional["OutcomeSchema"] = Field(default=None)
    agent: Optional["LLMAgentSchema"] = Field(default=None)
    messages: List["MessageSchema"] = Field(default_factory=list)
    images: List["ImageSchema"] = Field(default_factory=list)
    videos: List["VideoSchema"] = Field(default_factory=list)
    audio: List["AudioSchema"] = Field(default_factory=list)
    response_audio: Optional["AudioResponseSchema"] = Field(default=None)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class MessageSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    role: str = Field(default=None, max_length=50)
    content: Optional[str] = Field(default=None)
    name: str = Field(default=None, max_length=30)
    tool_call_id: Optional[str] = Field(default=None, max_length=100)
    tool_calls: Optional[str] = Field(default=None)
    thinking: Optional[str] = Field(default=None)
    redacted_thinking: Optional[str] = Field(default=None)
    provider_data: Optional[str] = Field(default=None)
    citations: Optional[str] = Field(default=None)
    reasoning_content: Optional[str] = Field(default=None)
    tool_name: Optional[str] = Field(default=None, max_length=100)
    tool_args: Optional[str] = Field(default=None)
    tool_call_error: Optional[bool] = Field(default=None)
    stop_after_tool_call: bool = Field(default=None)
    add_to_agent_memory: bool = Field(default=None)
    from_history: bool = Field(default=None)
    metrics: Optional[str] = Field(default=None)
    references: Optional[str] = Field(default=None)
    created_at: datetime = Field(default=None)
    last_updated: datetime = Field(default=None)

    # Relationships
    audio: List["AudioSchema"] = Field(default_factory=list)
    images: List["ImageSchema"] = Field(default_factory=list)
    videos: List["VideoSchema"] = Field(default_factory=list)
    files: List["FileSchema"] = Field(default_factory=list)
    audio_output: Optional["AudioResponseSchema"] = Field(default=None)
    image_output: Optional["ImageArtifactSchema"] = Field(default=None)
    from_actor: Optional["ActorSchema"] = Field(default=None)
    related_outcome: Optional["OutcomeSchema"] = Field(default=None)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class MediaSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    media_id: str = Field(default=None, max_length=100)
    original_prompt: Optional[str] = Field(default=None)
    revised_prompt: Optional[str] = Field(default=None)
    created_at: datetime = Field(default=None)
    last_updated: datetime = Field(default=None)

    # Relationships
    created_by: Optional["ActorSchema"] = Field(default=None)
    related_outcome: Optional["OutcomeSchema"] = Field(default=None)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class VideoArtifactSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    url: Optional[str] = Field(default=None, max_length=2048)
    eta: Optional[str] = Field(default=None, max_length=100)
    length: Optional[str] = Field(default=None, max_length=100)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class ImageArtifactSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    url: Optional[str] = Field(default=None, max_length=2048)
    content: Optional[str] = Field(default=None)
    mime_type: Optional[str] = Field(default=None, max_length=100)
    alt_text: Optional[str] = Field(default=None, max_length=255)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class AudioArtifactSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    url: Optional[str] = Field(default=None, max_length=2048)
    base64_audio: Optional[str] = Field(default=None)
    length: Optional[str] = Field(default=None, max_length=100)
    mime_type: Optional[str] = Field(default=None, max_length=100)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class AudioResponseSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    id: str = Field(default=None, max_length=100)
    content: Optional[str] = Field(default=None)
    expires_at: Optional[int] = Field(default=None)
    transcript: Optional[str] = Field(default=None)
    mime_type: Optional[str] = Field(default=None, max_length=100)
    sample_rate: int = Field(default=None)
    channels: int = Field(default=None)
    created_at: datetime = Field(default=None)
    last_updated: datetime = Field(default=None)

    # Relationships
    created_by: Optional["ActorSchema"] = Field(default=None)
    related_outcome: Optional["OutcomeSchema"] = Field(default=None)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class VideoSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    filepath: Optional[str] = Field(default=None, max_length=2048)
    content: Optional[str] = Field(default=None)
    format: Optional[str] = Field(default=None, max_length=50)
    created_at: datetime = Field(default=None)
    last_updated: datetime = Field(default=None)

    # Relationships
    created_by: Optional["ActorSchema"] = Field(default=None)
    related_outcome: Optional["OutcomeSchema"] = Field(default=None)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class AudioSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    content: Optional[str] = Field(default=None)
    filepath: Optional[str] = Field(default=None, max_length=2048)
    url: Optional[str] = Field(default=None, max_length=2048)
    format: Optional[str] = Field(default=None, max_length=50)
    created_at: datetime = Field(default=None)
    last_updated: datetime = Field(default=None)

    # Relationships
    created_by: Optional["ActorSchema"] = Field(default=None)
    related_outcome: Optional["OutcomeSchema"] = Field(default=None)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class ImageSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    url: Optional[str] = Field(default=None, max_length=2048)
    filepath: Optional[str] = Field(default=None, max_length=2048)
    content: Optional[str] = Field(default=None)
    format: Optional[str] = Field(default=None, max_length=50)
    detail: Optional[str] = Field(default=None, max_length=50)
    id: str = Field(default=None, max_length=100)
    created_at: datetime = Field(default=None)
    last_updated: datetime = Field(default=None)

    # Relationships
    created_by: Optional["ActorSchema"] = Field(default=None)
    related_outcome: Optional["OutcomeSchema"] = Field(default=None)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class ActorSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    name: str = Field(default=None, max_length=30)
    nextcloud_username: Optional[str] = Field(default=None, max_length=512)
    nextcloud_password: Optional[str] = Field(default=None, max_length=512)
    last_updated: datetime = Field(default=None)
    created: datetime = Field(default=None)

    # Relationships
    meetings: List["MeetingSchema"] = Field(default_factory=list)
    owned_outcomes: List["OutcomeSchema"] = Field(default_factory=list)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class EpochSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    name: str = Field(default=None, max_length=30)
    start_date: Optional[datetime] = Field(default=None)
    end_date: Optional[datetime] = Field(default=None)
    description: str = Field(default=None)
    created: datetime = Field(default=None)
    last_updated: datetime = Field(default=None)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class MeetingSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    name: str = Field(default=None, max_length=30)
    meeting_type: str = Field(default=None, max_length=30)
    purpose: Optional[str] = Field(default=None, max_length=1024)
    location: Optional[str] = Field(default=None, max_length=255)
    scheduled_start: Optional[datetime] = Field(default=None)
    state: str = Field(default=None, max_length=30)
    last_updated: datetime = Field(default=None)
    created: datetime = Field(default=None)

    # Relationships
    host: Optional["ActorSchema"] = Field(default=None)
    attendees: List["ActorSchema"] = Field(default_factory=list)
    expected_attendees: List["ActorSchema"] = Field(default_factory=list)
    required_attendees: List["ActorSchema"] = Field(default_factory=list)
    outcomes: List["OutcomeSchema"] = Field(default_factory=list)
    primary_outcome: Optional["OutcomeSchema"] = Field(default=None)
    expected_outcomes: List["OutcomeSchema"] = Field(default_factory=list)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class LLMAgentSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    description: str = Field(default=None)
    system_prompt: Optional[str] = Field(default=None, max_length=4096)
    api_key: Optional[str] = Field(default=None, max_length=255)
    model_name: Optional[str] = Field(default=None, max_length=255)

    # Relationships
    llm: Optional["LLMSchema"] = Field(default=None)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class HumanSchema(BaseModel):
    id: Optional[int] = Field(default=None)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class InteractionSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    history: str = Field(default=None)
    description: str = Field(default=None)
    mode: str = Field(default=None, max_length=20)
    outcome_contribution: Optional[str] = Field(default=None, max_length=2048)
    last_updated: datetime = Field(default=None)
    created: datetime = Field(default=None)

    # Relationships
    meeting: Optional["MeetingSchema"] = Field(default=None)
    outcomes: List["OutcomeSchema"] = Field(default_factory=list)
    primary_outcome: Optional["OutcomeSchema"] = Field(default=None)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class StatementSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    hash: str = Field(default=None, max_length=2048)
    text: str = Field(default=None, max_length=256)
    full_context: Optional[str] = Field(default=None)
    outcome_relevance: Optional[str] = Field(default=None)
    created: datetime = Field(default=None)
    last_updated: datetime = Field(default=None)

    # Relationships
    said_by: Optional["ActorSchema"] = Field(default=None)
    said_to: Optional["ActorSchema"] = Field(default=None)
    in_reply_to: Optional["StatementSchema"] = Field(default=None)
    conversation: Optional["ConversationSchema"] = Field(default=None)
    related_outcomes: List["OutcomeSchema"] = Field(default_factory=list)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class ConversationSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    outcome_focus: bool = Field(default=None)

    # Relationships
    interaction: Optional["InteractionSchema"] = Field(default=None)
    primary_outcome: Optional["OutcomeSchema"] = Field(default=None)
    outcomes: List["OutcomeSchema"] = Field(default_factory=list)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class OrganizationSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    name: str = Field(default=None, max_length=30)
    created: datetime = Field(default=None)
    last_updated: datetime = Field(default=None)

    # Relationships
    actors: List["ActorSchema"] = Field(default_factory=list)
    outcomes: List["OutcomeSchema"] = Field(default_factory=list)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class JobSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    name: str = Field(default=None, max_length=30)
    status: Optional[str] = Field(default=None, max_length=255)
    celery_id: Optional[str] = Field(default=None, max_length=255)
    priority: float = Field(default=None)
    initial_priority: float = Field(default=None)
    max_wait_cycles: int = Field(default=None)
    created: datetime = Field(default=None)
    last_updated: datetime = Field(default=None)
    completed: Optional[datetime] = Field(default=None)

    # Relationships
    related_outcome: Optional["OutcomeSchema"] = Field(default=None)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class DeliverableSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    name: str = Field(default=None, max_length=30)
    text: str = Field(default=None, max_length=256)
    created: datetime = Field(default=None)
    last_updated: datetime = Field(default=None)

    # Relationships
    for_interaction: Optional["InteractionSchema"] = Field(default=None)
    for_epoch: Optional["EpochSchema"] = Field(default=None)
    for_meeting: Optional["MeetingSchema"] = Field(default=None)
    for_outcome: Optional["OutcomeSchema"] = Field(default=None)
    contributing_outcomes: List["OutcomeSchema"] = Field(default_factory=list)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class TranscriptionSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    content: Optional[str] = Field(default=None)
    created: datetime = Field(default=None)
    last_updated: datetime = Field(default=None)

    # Relationships
    for_interaction: Optional["InteractionSchema"] = Field(default=None)
    for_meeting: Optional["MeetingSchema"] = Field(default=None)
    related_outcome: Optional["OutcomeSchema"] = Field(default=None)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class LLMSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    name: str = Field(default=None, max_length=30)
    created: datetime = Field(default=None)
    last_updated: datetime = Field(default=None)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class LLMHostSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    name: str = Field(default=None, max_length=30)
    uri: str = Field(default=None, max_length=1024)
    created: datetime = Field(default=None)
    last_updated: datetime = Field(default=None)

    # Relationships
    llm: Optional["LLMSchema"] = Field(default=None)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

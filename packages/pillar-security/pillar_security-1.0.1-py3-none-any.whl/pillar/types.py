"""
Core types for the Pillar SDK.

This module contains the core types used across the Pillar SDK,
independent of any specific integration.
"""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Role(Enum):
    """Possible roles for a message."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    FUNCTION = "function"
    TOOL = "tool"


# === Message Types ===


class PillarMessage(BaseModel):
    """A message in the Pillar system."""

    role: str
    content: str
    tool_calls: list[dict[str, Any]] | None = None


# === Pillar Response Types ===


class FindingMetadata(BaseModel):
    """Metadata for a finding from Pillar analysis."""

    start_idx: int | None = Field(
        default=None, description="Start index of the evidence in the text"
    )
    end_idx: int | None = Field(default=None, description="End index of the evidence in the text")


class Finding(BaseModel):
    """Detailed finding from Pillar analysis."""

    category: str = Field(description="Category of the finding (e.g., 'pii', 'prompt_injection')")
    type: str = Field(description="Type of the finding within the category")
    metadata: FindingMetadata | None = Field(default=None, description="Metadata for the finding")


class AnalysisResponse(BaseModel):
    """Response from the Pillar API content analysis endpoint (synchronous mode)."""

    flagged: bool = Field(description="Whether the content was flagged")
    session_id: str = Field(description="Session identifier")
    scanners: dict[str, bool] | None = Field(
        default=None, description="Scanners that were triggered and their results"
    )
    evidence: list[Finding] | None = Field(
        default=None, description="Detailed findings from analysis"
    )
    masked_messages: list[str] | None = Field(
        default=None, description="All messages without sensitive content"
    )


class AsyncAnalysisResponse(BaseModel):
    """Response from the Pillar API content analysis endpoint (asynchronous mode)."""

    status: str = Field(description="Status of the analysis request (e.g., 'queued')")
    session_id: str = Field(description="Session identifier")
    position: int | None = Field(
        default=None, description="Position of the analysis request in the queue"
    )


class PillarMetadata(BaseModel):
    """Metadata for the Pillar API request."""

    source: str
    version: str


class ApiRequest(BaseModel):
    """Request for the Pillar API."""

    messages: list[PillarMessage]
    metadata: PillarMetadata
    tools: list[dict[str, Any]] | None = None
    session_id: str | None = None
    user_id: str | None = None
    service: str | None = Field(default=None, description="Service provider")
    model: str | None = Field(default=None, description="Model identifier")


# API request/response types
API_REQUEST = ApiRequest
"""
Request data for the Pillar API.
An ApiRequest dataclass that can be converted to a dictionary using to_dict().
"""

API_RESPONSE = AnalysisResponse | AsyncAnalysisResponse
"""
Response from the Pillar API.
Either a list of AnalysisResponse or AsyncAnalysisResponse objects.
"""

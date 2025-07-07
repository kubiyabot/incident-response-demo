"""
Configuration management for incident response workflows.
"""

import os
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator


class IncidentSeverity(str, Enum):
    """Incident severity levels."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class IncidentPriority(str, Enum):
    """Incident priority levels."""

    URGENT = "urgent"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class IncidentConfig(BaseModel):
    """Configuration model for incident response workflows."""

    # Required incident fields
    incident_id: str = Field(..., description="Unique incident identifier")
    incident_title: str = Field(..., description="Incident title/summary")
    incident_severity: IncidentSeverity = Field(..., description="Incident severity level")
    incident_body: str = Field(..., description="Detailed incident description")
    incident_url: str = Field(..., description="Link to incident dashboard/monitoring")

    # Optional incident fields
    incident_priority: IncidentPriority = Field(
        IncidentPriority.MEDIUM, description="Incident priority"
    )
    incident_source: str = Field("automated-detection", description="Source of incident detection")
    incident_owner: Optional[str] = Field(None, description="Incident owner email")
    customer_impact: str = Field("unknown", description="Customer impact assessment")

    # Service validation
    affected_services: Optional[str] = Field(
        None, description="Comma-separated list of affected services"
    )

    # Communication channels
    slack_channel_id: str = Field(
        "#incidents", description="Primary Slack channel for notifications"
    )
    notification_channels: str = Field("#alerts", description="Additional notification channels")
    escalation_channel: str = Field("#incident-escalation", description="Escalation channel")

    # Workflow settings
    investigation_timeout: int = Field(600, description="AI investigation timeout in seconds")
    max_retries: int = Field(3, description="Maximum retry attempts")
    investigation_agent: str = Field("test-workflow", description="AI agent name for investigation")

    # Environment configuration
    kubiya_api_key: Optional[str] = Field(None, description="Kubiya API key")
    kubiya_user_email: Optional[str] = Field(None, description="Kubiya user email")
    kubiya_user_org: Optional[str] = Field(None, description="Kubiya user organization")
    runner: str = Field("gke-integration", description="Workflow runner")

    class Config:
        """Pydantic configuration."""

        use_enum_values = True
        extra = "allow"  # Allow additional fields

    @validator("incident_owner", pre=True, always=True)
    def set_incident_owner(cls, v, values):
        """Set incident owner from environment if not provided."""
        if v is None:
            return os.getenv("KUBIYA_USER_EMAIL", "unknown@company.com")
        return v

    @validator("kubiya_api_key", pre=True, always=True)
    def set_api_key(cls, v):
        """Set API key from environment if not provided."""
        if v is None:
            return os.getenv("KUBIYA_API_KEY")
        return v

    @validator("kubiya_user_email", pre=True, always=True)
    def set_user_email(cls, v):
        """Set user email from environment if not provided."""
        if v is None:
            return os.getenv("KUBIYA_USER_EMAIL")
        return v

    @validator("kubiya_user_org", pre=True, always=True)
    def set_user_org(cls, v):
        """Set user org from environment if not provided."""
        if v is None:
            return os.getenv("KUBIYA_USER_ORG", "default")
        return v

    def to_workflow_params(self) -> Dict[str, Any]:
        """Convert config to workflow parameters."""
        return {
            "incident_id": self.incident_id,
            "incident_title": self.incident_title,
            "incident_severity": self.incident_severity,
            "incident_priority": self.incident_priority,
            "incident_body": self.incident_body,
            "incident_url": self.incident_url,
            "incident_source": self.incident_source,
            "incident_owner": self.incident_owner,
            "slack_channel_id": self.slack_channel_id,
            "notification_channels": self.notification_channels,
            "escalation_channel": self.escalation_channel,
            "investigation_timeout": str(self.investigation_timeout),
            "max_retries": str(self.max_retries),
            "investigation_agent": self.investigation_agent,
            "customer_impact": self.customer_impact,
            "affected_services": self.affected_services or "",
        }

    def to_workflow_env(self) -> Dict[str, str]:
        """Convert config to workflow environment variables."""
        return {
            "KUBIYA_API_KEY": self.kubiya_api_key or "${KUBIYA_API_KEY}",
            "KUBIYA_USER_EMAIL": self.kubiya_user_email or "${KUBIYA_USER_EMAIL}",
            "KUBIYA_USER_ORG": self.kubiya_user_org or "${KUBIYA_USER_ORG}",
            "INCIDENT_SEVERITY": self.incident_severity,
            "INCIDENT_PRIORITY": self.incident_priority,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "IncidentConfig":
        """Create config from dictionary."""
        return cls(**data)

    @classmethod
    def from_env(cls, **overrides) -> "IncidentConfig":
        """Create config from environment variables with optional overrides."""
        env_data = {
            "incident_id": os.getenv("INCIDENT_ID", "INC-DEFAULT"),
            "incident_title": os.getenv("INCIDENT_TITLE", "System Issue"),
            "incident_severity": os.getenv("INCIDENT_SEVERITY", "medium"),
            "incident_body": os.getenv("INCIDENT_BODY", "System issue detected"),
            "incident_url": os.getenv("INCIDENT_URL", "https://monitoring.company.com"),
            "slack_channel_id": os.getenv("SLACK_CHANNEL_ID", "#incidents"),
            "affected_services": os.getenv("AFFECTED_SERVICES"),
        }
        env_data.update(overrides)
        return cls(**env_data)

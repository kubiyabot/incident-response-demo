"""
Kubiya Incident Response Workflow Module

A production-grade incident response workflow system that provides:
- Intelligent service validation with AI agents
- Automated Kubernetes cluster investigation
- Slack integration for real-time notifications
- Workflow re-triggering capabilities
- Comprehensive incident lifecycle management

Example usage:
    from kubiya_incident import IncidentWorkflow

    workflow = IncidentWorkflow()
    result = workflow.create_incident_response(
        incident_id="INC-123",
        incident_title="Database Connection Issues",
        incident_severity="high"
    )
"""

__version__ = "1.0.0"
__author__ = "Kubiya"
__email__ = "support@kubiya.ai"

from .agents.service_validator import ServiceValidationAgent
from .core.config import IncidentConfig
from .core.workflow import IncidentWorkflow
from .workflows.incident_response import IncidentResponseWorkflow

__all__ = [
    "IncidentWorkflow",
    "IncidentConfig",
    "ServiceValidationAgent",
    "IncidentResponseWorkflow",
]

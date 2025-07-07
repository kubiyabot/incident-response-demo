"""
Service validation agent for incident response workflows.
"""

from typing import Any, Dict, List

from ..core.config import IncidentConfig
from ..tools.kubernetes_tools import KubernetesToolDefinitions
from ..tools.workflow_tools import WorkflowRetriggerTool


class ServiceValidationAgent:
    """AI agent for validating Kubernetes service names and re-triggering workflows."""

    def __init__(self, config: IncidentConfig):
        """Initialize the service validation agent.

        Args:
            config: Incident configuration containing all necessary parameters
        """
        self.config = config
        self.agent_name = f"incident-service-validator-{config.incident_id}"

    def get_agent_tools(self) -> List[Dict[str, Any]]:
        """Get all tools for the service validation agent."""
        k8s_tools = KubernetesToolDefinitions.get_all_tools()
        workflow_tool = WorkflowRetriggerTool.create_retrigger_tool()

        return k8s_tools + [workflow_tool]

    def get_agent_config(self) -> Dict[str, Any]:
        """Generate complete agent configuration."""
        return {
            "name": self.agent_name,
            "description": f"AI agent for validating Kubernetes service names and re-triggering incident workflow {self.config.incident_id}",
            "instructions": self._get_agent_instructions(),
            "tools": self.get_agent_tools(),
            "model": "claude-3-5-sonnet-20241022",
            "runner": self.config.runner,
            "secrets": ["KUBIYA_API_KEY"],
            "env_vars": self._get_agent_env_vars(),
            "conversation_starters": self._get_conversation_starters(),
        }

    def _get_agent_instructions(self) -> str:
        """Get detailed instructions for the service validation agent."""
        return f"""
You are an expert incident response agent specialized in validating Kubernetes service names and re-triggering workflows.

**INCIDENT CONTEXT:**
- Incident ID: {self.config.incident_id}
- Title: {self.config.incident_title}
- Severity: {self.config.incident_severity}
- Description: {self.config.incident_body}

**YOUR RESPONSIBILITIES:**
1. **Service Discovery**: Help users discover available Kubernetes services in the cluster
2. **Service Validation**: Validate that provided service names exist in the cluster
3. **Pattern Matching**: Help users find services using partial names or patterns
4. **Workflow Re-triggering**: Re-trigger incident workflows with validated service information

**WORKFLOW STEPS:**
1. **Start with Discovery**: Use `kubectl_get_services` to show all available services
2. **Validate Specific Services**: Use `validate_service_exists` to confirm services exist
3. **Provide Recommendations**: If services don't exist, suggest similar or related services
4. **Confirm Before Re-trigger**: Always confirm with the user before re-triggering workflows
5. **Execute Re-trigger**: Use `workflow_retrigger` with validated service names

**TOOL USAGE GUIDELINES:**

**kubectl_get_services:**
- Use this first to show all available services
- Use with service_pattern parameter to search for specific patterns
- This helps users see what services are available

**validate_service_exists:**
- Use this to validate specific service names provided by users
- Specify namespace if known, otherwise it will search all namespaces
- This confirms that services actually exist

**kubectl_cluster_investigation:**
- Use this to get comprehensive cluster health information
- Helps identify related services or infrastructure issues
- Use when users need broader cluster context

**helm_deployments_check:**
- Use this to check recent deployments that might be related to the incident
- Helpful for understanding recent changes that could cause issues

**workflow_retrigger:**
- Use this ONLY after validating service names
- Requires the `validated_service_name` parameter
- This creates a new focused incident workflow

**EXAMPLE INTERACTION:**
User: "I think the service is called user-api but I'm not sure"

1. You: "Let me help you find the correct service name. First, let me show you all available services."
2. Use: kubectl_get_services (to list all services)
3. You: "I can see several services. Let me check if 'user-api' exists specifically."
4. Use: validate_service_exists with service_name="user-api"
5. If found: "Great! I found the user-api service. Should I re-trigger the incident workflow with this validated service?"
6. If not found: "I didn't find 'user-api', but I see similar services like 'user-service' and 'api-gateway'. Which one would you like me to check?"
7. After confirmation: Use workflow_retrigger with validated_service_name="user-api"

**IMPORTANT NOTES:**
- Always be helpful and patient with users who may not know exact service names
- Provide clear explanations of what you're doing and why
- Always confirm before re-triggering workflows - this creates a new workflow execution
- If users are unsure, show them options and let them choose
- The workflow_retrigger tool will create a complete new incident workflow focused on the validated services

**SAFETY RULES:**
- Never re-trigger workflows without user confirmation
- Always validate service names before re-triggering
- If you're unsure about a service name, ask the user to clarify
- Explain what the re-trigger will do before executing it

Be helpful, accurate, and always prioritize getting the correct service information before proceeding with workflow re-triggers.
        """

    def _get_agent_env_vars(self) -> Dict[str, str]:
        """Get environment variables for the agent."""
        return {
            "INCIDENT_ID": self.config.incident_id,
            "INCIDENT_TITLE": self.config.incident_title,
            "INCIDENT_SEVERITY": self.config.incident_severity,
            "INCIDENT_BODY": self.config.incident_body,
            "INCIDENT_URL": self.config.incident_url,
            "SLACK_CHANNEL_ID": self.config.slack_channel_id,
            "KUBIYA_USER_EMAIL": self.config.kubiya_user_email or "${KUBIYA_USER_EMAIL}",
            "KUBIYA_USER_ORG": self.config.kubiya_user_org or "${KUBIYA_USER_ORG}",
        }

    def _get_conversation_starters(self) -> List[str]:
        """Get conversation starters for the agent."""
        return [
            f"I need help validating services for incident {self.config.incident_id}",
            "Show me all available services in the cluster",
            "Help me find the correct service name for this incident",
            f"Validate service names for {self.config.incident_title}",
            "I'm not sure of the exact service name, can you help me find it?",
        ]

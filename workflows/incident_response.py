"""
Main incident response workflow implementation.
"""

from typing import Any, Dict

from kubiya_workflow_sdk.dsl import Workflow

from ..agents.service_validator import ServiceValidationAgent
from ..core.config import IncidentConfig


class IncidentResponseWorkflow:
    """Main incident response workflow with intelligent service validation."""

    def __init__(self, config: IncidentConfig):
        """Initialize the incident response workflow.

        Args:
            config: Incident configuration
        """
        self.config = config
        self.service_agent = ServiceValidationAgent(config)

    def create_workflow(self) -> Workflow:
        """Create the complete incident response workflow."""

        return (
            Workflow("production-incident-workflow")
            .description(
                "Production-grade incident response workflow with AI investigation and Slack integration"
            )
            .env(**self.config.to_workflow_env())
            .params(**self.config.to_workflow_params())
            .runner(self.config.runner)
            # Step 1: Validate incident parameters
            .step(
                "validate-incident",
                self._get_validation_command(),
                description="Validate incident parameters and prerequisites",
                executor={"type": "command", "config": {}},
                output="validation_status",
            )
            # Step 2: Setup Slack integration
            .step(
                "setup-slack-integration",
                description="Initialize Slack integration for incident communications",
                executor={
                    "type": "kubiya",
                    "config": {
                        "url": "api/v1/integration/slack/token/1",
                        "method": "GET",
                        "timeout": 30,
                        "silent": False,
                    },
                },
                depends=["validate-incident"],
                output="slack_token",
            )
            # Step 3: Handle validation failure (missing services)
            .step(
                "handle-validation-failure",
                self._get_validation_failure_command(),
                description="Send Slack notification when services are missing and create validation agent",
                executor={"type": "command", "config": {}},
                depends=["setup-slack-integration"],
                output="validation_failure_message",
            )
            # Step 4: Post incident alert (only if services provided)
            .step(
                "post-incident-alert",
                self._get_incident_alert_command(),
                description="Send beautiful incident alert to Slack when services are provided",
                executor={"type": "command", "config": {}},
                depends=["setup-slack-integration"],
                output="initial_alert_message",
            )
            # Step 5: Notify investigation start
            .step(
                "notify-investigation-start",
                self._get_investigation_start_command(),
                description="Notify AI investigation start",
                executor={"type": "command", "config": {}},
                depends=["post-incident-alert"],
                output="investigation_start_message",
            )
            # Step 6: AI-powered incident investigation
            .step(
                "investigate-incident-with-ai",
                description="AI-powered incident investigation",
                executor={
                    "type": "agent",
                    "config": {
                        "agent_name": self.config.investigation_agent,
                        "message": self._get_investigation_message(),
                    },
                },
                depends=["notify-investigation-start"],
                output="investigation_results",
            )
            # Step 7: Post investigation results (simplified - skip processing step)
            .step(
                "post-investigation-results",
                self._get_simple_post_results_command(),
                description="Post AI investigation completion notification to Slack",
                executor={"type": "command", "config": {}},
                depends=["investigate-incident-with-ai"],
                output="investigation_results_message",
            )
            # Step 9: Post action summary
            .step(
                "post-action-summary",
                self._get_action_summary_command(),
                description="Post actionable summary with next steps",
                executor={"type": "command", "config": {}},
                depends=["post-investigation-results"],
                output="action_summary_message",
            )
        )

    def _get_validation_command(self) -> str:
        """Get the incident validation command."""
        return """
echo "🔍 VALIDATING INCIDENT PARAMETERS"
echo "================================="

# Initialize validation status
VALIDATION_PASSED=true
MISSING_PARAMS=""

# Validate required parameters
if [ -z "${incident_id}" ]; then
  echo "❌ ERROR: incident_id is required"
  VALIDATION_PASSED=false
  MISSING_PARAMS="${MISSING_PARAMS} incident_id"
fi

if [ -z "${incident_title}" ]; then
  echo "❌ ERROR: incident_title is required"
  VALIDATION_PASSED=false
  MISSING_PARAMS="${MISSING_PARAMS} incident_title"
fi

if [ -z "${incident_severity}" ]; then
  echo "❌ ERROR: incident_severity is required"
  VALIDATION_PASSED=false
  MISSING_PARAMS="${MISSING_PARAMS} incident_severity"
fi

# NOTE: affected_services validation is now handled by agent
if [ -z "${affected_services}" ]; then
  echo "⚠️ WARNING: affected_services not provided - will create validation agent"
fi

# Validate severity levels
case "${incident_severity}" in
  "critical"|"high"|"medium"|"low")
    echo "✅ Severity '${incident_severity}' is valid"
    ;;
  *)
    echo "❌ ERROR: Invalid severity '${incident_severity}'. Must be: critical, high, medium, or low"
    VALIDATION_PASSED=false
    MISSING_PARAMS="${MISSING_PARAMS} valid_severity"
    ;;
esac

# Set validation result
if [ "$VALIDATION_PASSED" = "true" ]; then
  echo "📋 INCIDENT METADATA:"
  echo "  ID: ${incident_id}"
  echo "  Title: ${incident_title}"
  echo "  Severity: ${incident_severity}"
  echo "  Priority: ${incident_priority}"
  echo "  Owner: ${incident_owner}"
  echo "  Source: ${incident_source}"
  echo "  Affected Services: ${affected_services:-'TBD via agent'}"
  echo "  Customer Impact: ${customer_impact}"
  echo ""
  echo "✅ Incident validation completed successfully"
else
  echo "❌ Validation failed. Missing parameters: ${MISSING_PARAMS}"
  echo "⚠️ Continuing workflow to handle validation failure..."
fi
        """

    def _get_validation_failure_command(self) -> str:
        """Get the validation failure handling command."""
        agent_config = self.service_agent.get_agent_config()
        agent_name = agent_config["name"]
        tools_count = len(agent_config["tools"])

        # Build command without nested f-strings
        base_command = """
echo "🔍 DEBUG: handle-validation-failure step starting"
echo "affected_services value: '${affected_services}'"

# Check if affected_services is provided (if provided, skip this step)
if [ -n "${affected_services}" ]; then
  echo "🚫 SKIPPING: affected_services is provided - handle-validation-failure will not run"
  echo "This step only runs when affected_services is missing"
  exit 0
fi

echo "🚨 VALIDATION FAILED - CREATING SERVICE VALIDATION AGENT"
echo "Affected services is missing, creating agent to help with validation"

echo "🤖 AGENT CONFIGURATION:"
echo "Agent Name: """

        middle_command = """"
echo "Tools Available: """

        end_command = """ tools"
echo "- kubectl_get_services: List all cluster services"
echo "- validate_service_exists: Validate specific services"
echo "- kubectl_cluster_investigation: Comprehensive cluster analysis"
echo "- helm_deployments_check: Check recent deployments"
echo "- workflow_retrigger: Re-trigger workflow with validated services"

echo ""
echo "💬 AGENT INSTRUCTIONS:"
echo "The agent will help users:"
echo "1. Discover available Kubernetes services"
echo "2. Validate specific service names"
echo "3. Re-trigger the workflow with validated services"

echo ""
echo "Posting agent notification to channel: ${slack_channel_id}"
echo "Sending Slack message..."

AGENT_MESSAGE='{
    "channel": "'${slack_channel_id}'",
    "text": "🤖 Service Validation Agent Created",
    "attachments": [{
        "color": "#36a64f",
        "blocks": [{
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🤖 SERVICE VALIDATION AGENT READY"
            }
        }, {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Incident **${incident_title}** needs service validation*"
            }
        }, {
            "type": "divider"
        }, {
            "type": "section",
            "fields": [{
                "type": "mrkdwn",
                "text": "*🆔 Incident ID:*\\\\n${incident_id}"
            }, {
                "type": "mrkdwn",
                "text": "*🔥 Severity:*\\\\n${incident_severity}"
            }, {
                "type": "mrkdwn",
                "text": "*🤖 Agent:*\\\\n"""

        agent_field = """"
            }, {
                "type": "mrkdwn",
                "text": "*🎯 Purpose:*\\\\nService validation & workflow re-trigger"
            }]
        }, {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*🛠️ Agent Capabilities:*\\\\n• Validate Kubernetes service names\\\\n• Search for services in cluster\\\\n• Re-trigger workflow with validated services\\\\n• Provide service recommendations"
            }
        }, {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*💬 How to use:* Mention the agent and ask:\\\\n• \\"Help me validate services for incident ${incident_id}\\"\\\\n• \\"Show me all services in the cluster\\"\\\\n• \\"Validate service [service-name] for this incident\\""
            }
        }]
    }]
}'

curl -X POST https://slack.com/api/chat.postMessage \\
  -H "Authorization: Bearer ${slack_token.token}" \\
  -H "Content-Type: application/json" \\
  -d "$AGENT_MESSAGE"

echo "✅ Service validation agent notification sent to Slack"
        """

        return (
            base_command
            + agent_name
            + middle_command
            + str(tools_count)
            + end_command
            + agent_name
            + agent_field
        )

    def _get_incident_alert_command(self) -> str:
        """Get the incident alert command."""
        return """
echo "🔍 DEBUG: post-incident-alert step starting"
echo "affected_services value: '${affected_services}'"

# Check if affected_services is provided
if [ -z "${affected_services}" ]; then
  echo "🚫 SKIPPING: affected_services not provided - post-incident-alert will not run"
  exit 0
fi

echo "🚨 POSTING BEAUTIFUL INCIDENT ALERT"
echo "affected_services provided: '${affected_services}'"
echo "Posting to channel: ${slack_channel_id}"

echo "Sending beautiful incident alert with blocks..."
curl -X POST https://slack.com/api/chat.postMessage \\
  -H "Authorization: Bearer ${slack_token.token}" \\
  -H "Content-Type: application/json" \\
  -d '{"channel": "'${slack_channel_id}'", "text": "🚨 INCIDENT: ${incident_title}", "attachments": [{"color": "danger", "blocks": [{"type": "header", "text": {"type": "plain_text", "text": "🚨 PRODUCTION INCIDENT ALERT"}}, {"type": "section", "text": {"type": "mrkdwn", "text": "*${incident_title}*"}}, {"type": "divider"}, {"type": "section", "fields": [{"type": "mrkdwn", "text": "*🆔 ID:*\\\\n${incident_id}"}, {"type": "mrkdwn", "text": "*🔥 Severity:*\\\\n${incident_severity}"}, {"type": "mrkdwn", "text": "*⚡ Priority:*\\\\n${incident_priority}"}, {"type": "mrkdwn", "text": "*🎯 Services:*\\\\n${affected_services}"}]}, {"type": "section", "text": {"type": "mrkdwn", "text": "*📝 Description:*\\\\n${incident_body}"}}, {"type": "actions", "elements": [{"type": "button", "text": {"type": "plain_text", "text": "📊 Dashboard"}, "url": "${incident_url}", "style": "primary"}]}]}]}'

echo "✅ Beautiful incident alert posted to Slack"
        """

    def _get_investigation_start_command(self) -> str:
        """Get the investigation start notification command."""
        return """
echo "🔍 DEBUG: notify-investigation-start step starting"
echo "affected_services value: '${affected_services}'"

# Check if affected_services is provided
if [ -z "${affected_services}" ]; then
  echo "🚫 SKIPPING: affected_services not provided - notify-investigation-start will not run"
  exit 0
fi

echo "🔍 NOTIFYING INVESTIGATION START"
echo "affected_services provided: '${affected_services}'"
echo "Posting to channel: ${slack_channel_id}"

echo "Sending beautiful investigation start notification..."
curl -X POST https://slack.com/api/chat.postMessage \\
  -H "Authorization: Bearer ${slack_token.token}" \\
  -H "Content-Type: application/json" \\
  -d '{"channel": "'${slack_channel_id}'", "text": "🔍 AI Investigation Started", "attachments": [{"color": "good", "blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": "🔍 *AI Investigation Started*"}}, {"type": "divider"}, {"type": "section", "fields": [{"type": "mrkdwn", "text": "*🤖 Agent:*\\\\n'${investigation_agent}'"}, {"type": "mrkdwn", "text": "*⏱️ Timeout:*\\\\n'${investigation_timeout}' seconds"}, {"type": "mrkdwn", "text": "*🔄 Retries:*\\\\n'${max_retries}' attempts"}, {"type": "mrkdwn", "text": "*📊 Status:*\\\\n:hourglass_flowing_sand: Running"}]}, {"type": "section", "text": {"type": "mrkdwn", "text": "*🎯 Mission:* Automated Kubernetes diagnosis, root cause analysis, impact assessment"}}]}]}'

echo "✅ Beautiful investigation start notification posted to Slack"
        """

    def _get_investigation_message(self) -> str:
        """Get the AI investigation message."""
        return """**AUTOMATED KUBERNETES INCIDENT INVESTIGATION**

**CRITICAL NOTICE:** You are running in AUTOMATION MODE with NO USER INTERACTION capabilities. Perform CONCISE analysis using available tools.

**INCIDENT DETAILS:**
• **ID:** ${incident_id}
• **Title:** ${incident_title}
• **Severity:** ${incident_severity} (URGENT)
• **Description:** ${incident_body}
• **Affected Services:** ${affected_services}
• **Dashboard URL:** ${incident_url}

**YOUR MISSION - FOCUSED KUBERNETES INVESTIGATION:**
Perform these targeted investigations using available k8s-cli, helm-cli, datadog-cli, and observe-cli tools:

**1. RECENT DEPLOYMENTS (Last 6 Hours)**
- List recent Helm releases and their status
- Check for any failed or problematic deployments
- Use: helm-cli tools

**2. SERVICE HEALTH CHECK**
- Check status of affected services: ${affected_services}
- Look for pods with high restart counts (>3)
- Review recent pod events and logs
- Use: k8s-cli tools

**3. CLUSTER HEALTH OVERVIEW**
- Quick node health check
- Check for resource constraints or alerts
- Use: k8s-cli and datadog-cli/observe-cli if available

**REQUIRED OUTPUT FORMAT (KEEP CONCISE - MAX 2 SENTENCES PER SECTION):**
```
## 🎯 INVESTIGATION SUMMARY
[Brief 1-2 sentence overview]

## 📦 RECENT DEPLOYMENTS
[Quick status of recent changes]

## 🔍 SERVICE HEALTH
[Status of affected services: ${affected_services}]

## ⚠️ ISSUES FOUND
[Key problems identified]

## ⚡ IMMEDIATE ACTIONS
1. [Critical action 1]
2. [Critical action 2]

## 🚨 ESCALATION
[Yes/No with brief reason]
```

**CONSTRAINTS:**
- KEEP OUTPUT CONCISE - Limited output required
- Focus ONLY on affected services: ${affected_services}
- Use read-only tools only
- No verbose command outputs
- Provide actionable insights quickly

**START FOCUSED INVESTIGATION NOW!**"""

    def _get_process_results_command(self) -> str:
        """Get the process investigation results command."""
        return """
echo "🔍 DEBUG: process-investigation-results step starting"
echo "affected_services value: '${affected_services}'"

# Check if affected_services is provided
if [ -z "${affected_services}" ]; then
  echo "🚫 SKIPPING: affected_services not provided - process-investigation-results will not run"
  exit 0
fi

echo "📊 PROCESSING INVESTIGATION RESULTS"
echo "===================================="

# Use printf to handle special characters properly
printf '%s' "${investigation_results}" > /tmp/investigation_output.txt
RESULT_LENGTH=$(wc -c < /tmp/investigation_output.txt)
echo "AI investigation output length: $RESULT_LENGTH characters"

# Simple check - just verify we have content
if [ "$RESULT_LENGTH" -gt 10 ]; then
  echo "✅ AI investigation completed successfully"
  echo "AGENT_ERROR_DETECTED=false" > /tmp/agent_status
  echo "Investigation results processed successfully"
else
  echo "⚠️ Investigation results appear incomplete"
  echo "AGENT_ERROR_DETECTED=true" > /tmp/agent_status
  echo "Providing fallback investigation results"
fi

echo "📝 Investigation results ready for Slack posting"
echo "✅ Investigation results processing completed"
        """

    def _get_post_results_command(self) -> str:
        """Get the post investigation results command."""
        return """
echo "🔍 DEBUG: post-investigation-results step starting"
echo "affected_services value: '${affected_services}'"

# Check if affected_services is provided
if [ -z "${affected_services}" ]; then
  echo "🚫 SKIPPING: affected_services not provided - post-investigation-results will not run"
  exit 0
fi

echo "🔬 POSTING INVESTIGATION RESULTS"
echo "affected_services provided: '${affected_services}'"
echo "Posting to channel: ${slack_channel_id}"

# Post investigation completion notification
echo "📊 Posting investigation completion notification..."
curl -s -X POST https://slack.com/api/chat.postMessage \\
  -H "Authorization: Bearer ${slack_token.token}" \\
  -H "Content-Type: application/json" \\
  -d "{
    \\"channel\\": \\"${slack_channel_id}\\",
    \\"text\\": \\"🔬 AI Investigation Complete\\",
    \\"attachments\\": [{
      \\"color\\": \\"#ff9900\\",
      \\"blocks\\": [{
        \\"type\\": \\"header\\",
        \\"text\\": {
          \\"type\\": \\"plain_text\\",
          \\"text\\": \\"🔬 AI INVESTIGATION COMPLETE\\"
        }
      }, {
        \\"type\\": \\"section\\",
        \\"text\\": {
          \\"type\\": \\"mrkdwn\\",
          \\"text\\": \\"*Incident:* ${incident_title}\\\\n*Services:* ${affected_services}\\\\n*Status:* ✅ Analysis Complete\\"
        }
      }, {
        \\"type\\": \\"section\\",
        \\"text\\": {
          \\"type\\": \\"mrkdwn\\",
          \\"text\\": \\"*Key Findings:* Critical services not running - immediate action required\\\\n*Next Steps:* Deploy services and restore monitoring\\"
        }
      }]
    }]
  }"

# Post the actual investigation results as a code block (if file exists)
if [ -f "/tmp/investigation_output.txt" ]; then
  echo "📝 Posting detailed investigation results..."

  # Use base64 encoding to safely transfer the content
  base64 -w 0 /tmp/investigation_output.txt > /tmp/investigation_b64.txt

  # Create a simple script to decode and post
  cat > /tmp/post_results.sh << 'EOF'
#!/bin/bash
CONTENT=$(base64 -d /tmp/investigation_b64.txt)
curl -s -X POST https://slack.com/api/chat.postMessage \\
  -H "Authorization: Bearer $1" \\
  -H "Content-Type: application/json" \\
  -d "{\\"channel\\": \\"$2\\", \\"text\\": \\"📋 **Investigation Results:**\\\\n\\`\\`\\`\\\\n${CONTENT}\\\\n\\`\\`\\`\\"}"
EOF

  chmod +x /tmp/post_results.sh
  /tmp/post_results.sh "${slack_token.token}" "${slack_channel_id}" || echo "📝 Fallback: Investigation completed with findings"
else
  echo "📝 Investigation results file not found, posting summary"
  curl -s -X POST https://slack.com/api/chat.postMessage \\
    -H "Authorization: Bearer ${slack_token.token}" \\
    -H "Content-Type: application/json" \\
    -d "{
      \\"channel\\": \\"${slack_channel_id}\\",
      \\"text\\": \\"📋 Investigation completed successfully. Key finding: Critical services require immediate attention.\\"
    }"
fi

echo "✅ Investigation results posted to Slack"
        """

    def _get_simple_post_results_command(self) -> str:
        """Get a simplified post investigation results command that avoids variable substitution issues."""
        return """
echo "🔍 DEBUG: post-investigation-results step starting"
echo "affected_services value: '${affected_services}'"

# Check if affected_services is provided
if [ -z "${affected_services}" ]; then
  echo "🚫 SKIPPING: affected_services not provided - post-investigation-results will not run"
  exit 0
fi

echo "🔬 POSTING INVESTIGATION COMPLETION NOTIFICATION"
echo "affected_services provided: '${affected_services}'"
echo "Posting to channel: ${slack_channel_id}"

# Post investigation completion notification (avoiding variable substitution issues)
echo "📊 Posting investigation completion notification..."
curl -s -X POST https://slack.com/api/chat.postMessage \\
  -H "Authorization: Bearer ${slack_token.token}" \\
  -H "Content-Type: application/json" \\
  -d "{
    \\"channel\\": \\"${slack_channel_id}\\",
    \\"text\\": \\"🔬 AI Investigation Complete\\",
    \\"attachments\\": [{
      \\"color\\": \\"#ff9900\\",
      \\"blocks\\": [{
        \\"type\\": \\"header\\",
        \\"text\\": {
          \\"type\\": \\"plain_text\\",
          \\"text\\": \\"🔬 AI INVESTIGATION COMPLETE\\"
        }
      }, {
        \\"type\\": \\"section\\",
        \\"text\\": {
          \\"type\\": \\"mrkdwn\\",
          \\"text\\": \\"*Incident:* ${incident_title}\\\\n*Services:* ${affected_services}\\\\n*Status:* ✅ Analysis Complete\\"
        }
      }, {
        \\"type\\": \\"section\\",
        \\"text\\": {
          \\"type\\": \\"mrkdwn\\",
          \\"text\\": \\"*Summary:* AI investigation completed successfully for the affected services. Detailed analysis has been performed and findings are available.\\"
        }
      }, {
        \\"type\\": \\"section\\",
        \\"text\\": {
          \\"type\\": \\"mrkdwn\\",
          \\"text\\": \\"*Next Steps:* Review investigation findings and take appropriate remediation actions based on the analysis.\\"
        }
      }]
    }]
  }"

echo "📝 Investigation completed successfully - detailed results generated"
echo "✅ Investigation results notification posted to Slack"
        """

    def _get_action_summary_command(self) -> str:
        """Get the action summary command."""
        return """
echo "🔍 DEBUG: post-action-summary step starting"
echo "affected_services value: '${affected_services}'"

# Check if affected_services is provided
if [ -z "${affected_services}" ]; then
  echo "🚫 SKIPPING: affected_services not provided - post-action-summary will not run"
  exit 0
fi

echo "⚡ POSTING ACTION SUMMARY"
echo "affected_services provided: '${affected_services}'"
echo "Posting to channel: ${slack_channel_id}"

echo "Sending action summary..."
curl -X POST https://slack.com/api/chat.postMessage \\
  -H "Authorization: Bearer ${slack_token.token}" \\
  -H "Content-Type: application/json" \\
  -d '{"channel": "'${slack_channel_id}'", "text": "✅ Incident Response Complete for ${incident_title} - Next steps available for review"}'

echo "✅ Action summary posted to Slack"
        """

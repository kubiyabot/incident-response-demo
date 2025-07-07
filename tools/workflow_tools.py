"""
Workflow re-triggering tools for incident response.
"""

from typing import Dict, Any


class WorkflowRetriggerTool:
    """Tool for re-triggering incident workflows with validated services."""
    
    @staticmethod
    def create_retrigger_tool() -> Dict[str, Any]:
        """Create workflow re-trigger tool definition."""
        return {
            "name": "workflow_retrigger",
            "description": "Re-trigger the incident workflow with validated service information using the Kubiya Workflow API",
            "type": "http",
            "url": "https://api.kubiya.ai/api/v1/workflow?runner=gke-integration&operation=execute_workflow",
            "method": "POST",
            "headers": {
                "Content-Type": "application/json",
                "Authorization": "UserKey {{KUBIYA_API_KEY}}",
                "Accept": "text/event-stream"
            },
            "body": {
                "command": "execute_workflow",
                "name": "incident-response-retrigger-{{INCIDENT_ID}}",
                "description": "Re-triggered incident response with validated service: {{validated_service_name}}",
                "env": {
                    "KUBIYA_API_KEY": "{{KUBIYA_API_KEY}}",
                    "KUBIYA_USER_EMAIL": "{{KUBIYA_USER_EMAIL}}",
                    "KUBIYA_USER_ORG": "{{KUBIYA_USER_ORG}}"
                },
                "params": {
                    "incident_id": "{{INCIDENT_ID}}",
                    "incident_title": "{{INCIDENT_TITLE}}",
                    "incident_severity": "{{INCIDENT_SEVERITY}}",
                    "incident_body": "{{INCIDENT_BODY}}",
                    "incident_url": "{{INCIDENT_URL}}",
                    "slack_channel_id": "{{SLACK_CHANNEL_ID}}",
                    "affected_services": "{{validated_service_name}}",
                    "incident_priority": "medium",
                    "incident_source": "agent-validated",
                    "incident_owner": "{{KUBIYA_USER_EMAIL}}",
                    "customer_impact": "partial"
                },
                "steps": [
                    {
                        "name": "validated-incident-alert",
                        "description": "Send validated incident alert to Slack",
                        "executor": {
                            "type": "kubiya",
                            "config": {
                                "url": "api/v1/integration/slack/token/1",
                                "method": "GET",
                                "timeout": 30
                            }
                        },
                        "output": "slack_token"
                    },
                    {
                        "name": "post-validated-alert",
                        "description": "Post alert with validated service information",
                        "executor": {
                            "type": "command",
                            "config": {}
                        },
                        "command": "echo '✅ INCIDENT WORKFLOW RE-TRIGGERED' && echo 'Incident ID: {{INCIDENT_ID}}' && echo 'Validated Services: {{validated_service_name}}' && echo 'Starting targeted investigation...' && curl -X POST https://slack.com/api/chat.postMessage -H \"Authorization: Bearer ${slack_token.token}\" -H \"Content-Type: application/json\" -d '{\"channel\": \"{{SLACK_CHANNEL_ID}}\", \"text\": \"✅ INCIDENT RE-TRIGGERED\", \"attachments\": [{\"color\": \"good\", \"blocks\": [{\"type\": \"header\", \"text\": {\"type\": \"plain_text\", \"text\": \"✅ INCIDENT VALIDATED & RE-TRIGGERED\"}}, {\"type\": \"section\", \"text\": {\"type\": \"mrkdwn\", \"text\": \"*{{INCIDENT_TITLE}}*\"}}, {\"type\": \"section\", \"fields\": [{\"type\": \"mrkdwn\", \"text\": \"*🆔 ID:*\\n{{INCIDENT_ID}}\"}, {\"type\": \"mrkdwn\", \"text\": \"*🔥 Severity:*\\n{{INCIDENT_SEVERITY}}\"}, {\"type\": \"mrkdwn\", \"text\": \"*🎯 Validated Services:*\\n{{validated_service_name}}\"}, {\"type\": \"mrkdwn\", \"text\": \"*🤖 Source:*\\nAgent Validated\"}]}, {\"type\": \"section\", \"text\": {\"type\": \"mrkdwn\", \"text\": \"*📝 Description:*\\n{{INCIDENT_BODY}}\"}}]}]}'",
                        "depends": ["validated-incident-alert"],
                        "output": "validated_alert"
                    },
                    {
                        "name": "investigate-validated-services",
                        "description": "AI investigation focused on validated services",
                        "executor": {
                            "type": "agent",
                            "config": {
                                "agent_name": "incident-responder",
                                "message": "**VALIDATED KUBERNETES INCIDENT INVESTIGATION**\\n\\n**INCIDENT DETAILS:**\\n• **ID:** {{INCIDENT_ID}}\\n• **Title:** {{INCIDENT_TITLE}}\\n• **Severity:** {{INCIDENT_SEVERITY}} (URGENT)\\n• **Description:** {{INCIDENT_BODY}}\\n• **Validated Services:** {{validated_service_name}}\\n• **Dashboard URL:** {{INCIDENT_URL}}\\n\\n**YOUR MISSION - FOCUS ON VALIDATED SERVICES:**\\nPerform targeted investigation for the validated services: {{validated_service_name}}\\n\\n**1. SERVICE-SPECIFIC INVESTIGATION**\\n- Check the health and status of {{validated_service_name}}\\n- Analyze recent deployments affecting these services\\n- Review logs and metrics for these specific services\\n\\n**2. KUBERNETES CLUSTER ANALYSIS**\\n- Check pods, deployments, and services related to {{validated_service_name}}\\n- Verify resource utilization for these services\\n- Look for networking issues affecting these services\\n\\n**3. ROOT CAUSE ANALYSIS**\\n- Focus investigation on {{validated_service_name}}\\n- Identify specific issues with these validated services\\n- Provide targeted remediation steps\\n\\n**REQUIRED OUTPUT FORMAT:**\\n```\\n## 🎯 VALIDATED SERVICE INVESTIGATION\\n[Focus on {{validated_service_name}}]\\n\\n## 🔍 SERVICE STATUS\\n[Current status of {{validated_service_name}}]\\n\\n## 🚨 ROOT CAUSE\\n[Primary cause affecting {{validated_service_name}}]\\n\\n## ⚡ IMMEDIATE ACTIONS\\n1. [Specific action for {{validated_service_name}} - ETA]\\n2. [Additional remediation - ETA]\\n\\n## 📊 IMPACT ASSESSMENT\\n[Business impact of {{validated_service_name}} issues]\\n```\\n\\n**START TARGETED INVESTIGATION NOW!**"
                            }
                        },
                        "depends": ["post-validated-alert"],
                        "output": "investigation_results",
                        "timeout": 600,
                        "retries": 3
                    }
                ]
            }
        }
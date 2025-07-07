#!/usr/bin/env python3
"""
Command-line interface for Kubiya Incident Response Workflow.
"""

import argparse
import json
import sys

from core.config import IncidentConfig
from core.workflow import IncidentWorkflow


def create_parser() -> argparse.ArgumentParser:
    """Create the command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Kubiya Incident Response Workflow CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Execute workflow with basic parameters
  kubiya-incident execute --incident-id INC-123 --title "Database Issues" --severity high

  # Execute workflow with services
  kubiya-incident execute --incident-id INC-123 --title "API Down" --severity critical --services "user-api,payment-service"

  # Export workflow to JSON
  kubiya-incident export --format json --output workflow.json

  # Create service validation agent only
  kubiya-incident create-agent --incident-id INC-123 --title "Service Issues"

  # Test workflow configuration
  kubiya-incident validate --incident-id INC-123 --title "Test" --severity medium
""",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Execute command
    execute_parser = subparsers.add_parser("execute", help="Execute incident response workflow")
    execute_parser.add_argument("--incident-id", required=True, help="Incident ID")
    execute_parser.add_argument("--title", required=True, help="Incident title")
    execute_parser.add_argument(
        "--severity",
        required=True,
        choices=["critical", "high", "medium", "low"],
        help="Incident severity",
    )
    execute_parser.add_argument("--services", help="Comma-separated list of affected services")
    execute_parser.add_argument(
        "--priority",
        choices=["urgent", "high", "medium", "low"],
        default="medium",
        help="Incident priority",
    )
    execute_parser.add_argument("--owner", help="Incident owner")
    execute_parser.add_argument("--source", default="cli", help="Incident source")
    execute_parser.add_argument("--body", help="Incident description")
    execute_parser.add_argument("--url", help="Incident dashboard URL")
    execute_parser.add_argument("--channel", help="Slack channel ID")
    execute_parser.add_argument("--stream", action="store_true", help="Stream execution output")

    # Export command
    export_parser = subparsers.add_parser("export", help="Export workflow configuration")
    export_parser.add_argument(
        "--format", choices=["json", "yaml", "dict"], default="json", help="Export format"
    )
    export_parser.add_argument("--output", help="Output file path (default: stdout)")
    export_parser.add_argument("--incident-id", default="TEMPLATE", help="Template incident ID")
    export_parser.add_argument(
        "--title", default="Template Incident", help="Template incident title"
    )
    export_parser.add_argument(
        "--severity",
        default="medium",
        choices=["critical", "high", "medium", "low"],
        help="Template severity",
    )

    # Create agent command
    agent_parser = subparsers.add_parser("create-agent", help="Create service validation agent")
    agent_parser.add_argument("--incident-id", required=True, help="Incident ID")
    agent_parser.add_argument("--title", required=True, help="Incident title")
    agent_parser.add_argument(
        "--severity",
        required=True,
        choices=["critical", "high", "medium", "low"],
        help="Incident severity",
    )
    agent_parser.add_argument("--body", help="Incident description")
    agent_parser.add_argument("--output", help="Output file for agent config")

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate workflow configuration")
    validate_parser.add_argument("--incident-id", required=True, help="Incident ID")
    validate_parser.add_argument("--title", required=True, help="Incident title")
    validate_parser.add_argument(
        "--severity",
        required=True,
        choices=["critical", "high", "medium", "low"],
        help="Incident severity",
    )
    validate_parser.add_argument("--services", help="Comma-separated list of affected services")

    return parser


def execute_workflow(args) -> int:
    """Execute the incident response workflow."""
    try:
        # Create configuration
        config_dict = {
            "incident_id": args.incident_id,
            "incident_title": args.title,
            "incident_severity": args.severity,
            "incident_priority": args.priority,
            "incident_owner": args.owner or "${KUBIYA_USER_EMAIL}",
            "incident_source": args.source,
            "incident_body": args.body or f"Incident: {args.title}",
            "incident_url": args.url or "#",
            "slack_channel_id": args.channel or "${SLACK_CHANNEL_ID}",
        }

        if args.services:
            config_dict["affected_services"] = args.services

        config = IncidentConfig(**config_dict)
        incident = IncidentWorkflow(config)

        print(f"🚀 Executing incident workflow: {args.incident_id}")
        print(f"📋 Title: {args.title}")
        print(f"🔥 Severity: {args.severity}")
        if args.services:
            print(f"🎯 Services: {args.services}")
        print("")

        workflow = incident.create_incident_response()

        if args.stream:
            print("📡 Streaming execution results...")
            print("" + "=" * 50)
            for line in incident.execute_workflow_stream(workflow):
                print(line)
        else:
            result = incident.execute_workflow(workflow)
            if result["success"]:
                print("✅ Workflow executed successfully!")
                print(result["response"])
            else:
                print(f"❌ Workflow execution failed: {result['error']}")
                return 1

        return 0

    except Exception as e:
        print(f"❌ Error executing workflow: {str(e)}")
        return 1


def export_workflow(args) -> int:
    """Export workflow configuration."""
    try:
        # Create template configuration with defaults
        config_dict = {
            "incident_id": args.incident_id,
            "incident_title": args.title,
            "incident_severity": args.severity,
            "incident_body": f"Template incident: {args.title}",
            "incident_url": "https://example.com/incidents/template",
        }

        config = IncidentConfig(**config_dict)
        incident = IncidentWorkflow(config)

        # Export in requested format
        if args.format == "json":
            output = incident.to_json()
        elif args.format == "yaml":
            output = incident.to_yaml()
        else:  # dict
            output = json.dumps(incident.to_dict(), indent=2)

        # Write to file or stdout
        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
            print(f"✅ Workflow exported to {args.output}")
        else:
            print(output)

        return 0

    except Exception as e:
        print(f"❌ Error exporting workflow: {str(e)}")
        return 1


def create_agent(args) -> int:
    """Create service validation agent configuration."""
    try:
        # Create configuration with defaults
        config_dict = {
            "incident_id": args.incident_id,
            "incident_title": args.title,
            "incident_severity": args.severity,
            "incident_body": args.body or f"Incident: {args.title}",
            "incident_url": "https://example.com/incidents/agent-test",
        }

        config = IncidentConfig(**config_dict)
        incident = IncidentWorkflow(config)

        agent_config = incident.create_service_validation_agent()
        output = json.dumps(agent_config, indent=2)

        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
            print(f"✅ Agent configuration exported to {args.output}")
        else:
            print(output)

        return 0

    except Exception as e:
        print(f"❌ Error creating agent: {str(e)}")
        return 1


def validate_config(args) -> int:
    """Validate workflow configuration."""
    try:
        # Create configuration with defaults
        config_dict = {
            "incident_id": args.incident_id,
            "incident_title": args.title,
            "incident_severity": args.severity,
            "incident_body": f"Test incident: {args.title}",
            "incident_url": "https://example.com/incidents/test",
        }

        if args.services:
            config_dict["affected_services"] = args.services

        config = IncidentConfig(**config_dict)
        incident = IncidentWorkflow(config)

        # Try to create workflow to validate
        workflow = incident.create_incident_response()

        print("✅ Configuration validation passed!")
        print(f"📋 Incident ID: {config.incident_id}")
        print(f"📝 Title: {config.incident_title}")
        print(f"🔥 Severity: {config.incident_severity}")
        print(f"🏃 Runner: {config.runner}")
        print(f"📊 Steps: {len(workflow.to_dict()['steps'])}")

        if hasattr(config, "affected_services") and config.affected_services:
            print(f"🎯 Services: {config.affected_services}")

        return 0

    except Exception as e:
        print(f"❌ Configuration validation failed: {str(e)}")
        return 1


def main() -> int:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Execute command
    if args.command == "execute":
        return execute_workflow(args)
    elif args.command == "export":
        return export_workflow(args)
    elif args.command == "create-agent":
        return create_agent(args)
    elif args.command == "validate":
        return validate_config(args)
    else:
        print(f"❌ Unknown command: {args.command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

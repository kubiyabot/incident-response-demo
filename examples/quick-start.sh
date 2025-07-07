#!/bin/bash
# Quick start script for Kubiya Incident Response Workflow
set -e

echo "🚀 Kubiya Incident Response Workflow - Quick Start"
echo "================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "../cli.py" ]; then
    echo -e "${RED}❌ Please run this script from the examples directory${NC}"
    echo "Expected location: kubiya_incident/examples/"
    exit 1
fi

# Get the project root
PROJECT_ROOT="$(cd .. && pwd)"
echo -e "${BLUE}📁 Project root: $PROJECT_ROOT${NC}"

# Check if virtual environment exists
if [ ! -d "$PROJECT_ROOT/venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Running setup first...${NC}"
    cd "$PROJECT_ROOT"
    ./kubiya_incident/setup.sh
    cd - > /dev/null
fi

# Activate virtual environment
echo -e "${YELLOW}🔧 Activating virtual environment...${NC}"
source "$PROJECT_ROOT/venv/bin/activate"

# Set PYTHONPATH for development
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

echo ""
echo -e "${GREEN}✅ Environment ready! Here are some examples:${NC}"
echo ""

# Example 1: Basic workflow export
echo -e "${BLUE}📋 Example 1: Export basic workflow to JSON${NC}"
echo "Command: python3 -m kubiya_incident.cli export --format json"
echo "Output:"
python3 -m kubiya_incident.cli export --format json | head -10
echo "... (truncated)"
echo ""

# Example 2: Export with custom parameters
echo -e "${BLUE}📋 Example 2: Export critical incident workflow${NC}"
echo "Command: python3 -m kubiya_incident.cli export --format json --incident-id 'CRITICAL-001' --title 'Database Outage' --severity critical"
echo "Result: See workflow-critical.json"
echo ""

# Example 3: Validate configuration
echo -e "${BLUE}📋 Example 3: Validate workflow configuration${NC}"
echo "Command: python3 -m kubiya_incident.cli validate --incident-id 'TEST-123' --title 'Test Incident' --severity medium"
echo "Output:"
python3 -m kubiya_incident.cli validate --incident-id 'TEST-123' --title 'Test Incident' --severity medium
echo ""

# Example 4: Create service validation agent
echo -e "${BLUE}📋 Example 4: Create service validation agent${NC}"
echo "Command: python3 -m kubiya_incident.cli create-agent --incident-id 'SERVICE-001' --title 'Service Check' --severity high"
echo "Result: See service-validation-agent.json"
echo ""

# Example 5: Execute workflow (dry run)
echo -e "${BLUE}📋 Example 5: Execute workflow (requires API key)${NC}"
echo "Command: KUBIYA_API_KEY=your-key python3 -m kubiya_incident.cli execute --incident-id 'PROD-001' --title 'Production Issue' --severity high --services 'user-api,payment-service'"
echo "Note: This requires a valid KUBIYA_API_KEY environment variable"
echo ""

# Show generated files
echo -e "${GREEN}📁 Generated example files:${NC}"
ls -la *.json *.yaml 2>/dev/null || echo "No example files found. Run export commands to generate them."
echo ""

# Interactive mode
echo -e "${YELLOW}🎯 Want to try it yourself?${NC}"
echo "Choose an option:"
echo "1. Export workflow to JSON"
echo "2. Export workflow to YAML"
echo "3. Validate configuration"
echo "4. Create service agent"
echo "5. Show CLI help"
echo "6. Exit"

read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo -e "${BLUE}🔧 Exporting workflow to JSON...${NC}"
        python3 -m kubiya_incident.cli export --format json --output interactive-workflow.json
        echo "✅ Exported to interactive-workflow.json"
        ;;
    2)
        echo -e "${BLUE}🔧 Exporting workflow to YAML...${NC}"
        python3 -m kubiya_incident.cli export --format yaml --output interactive-workflow.yaml
        echo "✅ Exported to interactive-workflow.yaml"
        ;;
    3)
        echo -e "${BLUE}🔧 Validating configuration...${NC}"
        python3 -m kubiya_incident.cli validate --incident-id "INTERACTIVE-001" --title "Interactive Test" --severity medium
        ;;
    4)
        echo -e "${BLUE}🔧 Creating service validation agent...${NC}"
        python3 -m kubiya_incident.cli create-agent --incident-id "AGENT-001" --title "Agent Test" --severity high --output interactive-agent.json
        echo "✅ Agent created: interactive-agent.json"
        ;;
    5)
        echo -e "${BLUE}🔧 Showing CLI help...${NC}"
        python3 -m kubiya_incident.cli --help
        ;;
    6)
        echo -e "${GREEN}👋 Goodbye!${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}❌ Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}🎉 Quick start complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Set up your KUBIYA_API_KEY environment variable"
echo "2. Try executing a workflow with real incident data"
echo "3. Integrate with your monitoring and alerting systems"
echo "4. Customize the workflow steps for your environment"
echo ""
echo "For more information, see the README.md file"
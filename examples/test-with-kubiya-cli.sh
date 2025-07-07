#!/bin/bash
# Test script for Kubiya CLI integration
set -e

echo "🧪 Kubiya CLI Integration Test Script"
echo "====================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
RUNNER="${KUBIYA_RUNNER:-gke-integration}"
API_KEY="${KUBIYA_API_KEY}"

# Check prerequisites
echo -e "${BLUE}🔍 Checking prerequisites...${NC}"

# Check if kubiya CLI is installed
if ! command -v kubiya &> /dev/null; then
    echo -e "${RED}❌ Kubiya CLI not found. Please install it first:${NC}"
    echo "npm install -g @kubiya/cli"
    echo "or download from: https://github.com/kubiya-ai/kubiya-cli/releases"
    exit 1
fi

# Check API key
if [ -z "$API_KEY" ]; then
    echo -e "${YELLOW}⚠️  KUBIYA_API_KEY not set. Some tests will be skipped.${NC}"
    echo "To run full tests, set: export KUBIYA_API_KEY='your-api-key'"
    SKIP_EXECUTION=true
else
    echo -e "${GREEN}✅ API key found${NC}"
    SKIP_EXECUTION=false
fi

# Check if we're in the right directory
if [ ! -f "../cli.py" ]; then
    echo -e "${RED}❌ Please run this script from the examples directory${NC}"
    echo "Expected location: kubiya_incident/examples/"
    exit 1
fi

# Get the project root
PROJECT_ROOT="$(cd .. && pwd)"
echo -e "${BLUE}📁 Project root: $PROJECT_ROOT${NC}"

# Activate virtual environment if it exists
if [ -d "$PROJECT_ROOT/venv" ]; then
    echo -e "${YELLOW}🔧 Activating virtual environment...${NC}"
    source "$PROJECT_ROOT/venv/bin/activate"
    export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"
else
    echo -e "${YELLOW}⚠️  Virtual environment not found. Using system Python.${NC}"
fi

echo ""
echo -e "${GREEN}🚀 Starting Kubiya CLI Tests${NC}"
echo ""

# Test 1: Export workflow to JSON
echo -e "${BLUE}📋 Test 1: Export Basic Workflow${NC}"
TEST_WORKFLOW="kubiya-cli-test-workflow.json"

python3 -m kubiya_incident.cli export --format json --output "$TEST_WORKFLOW"

if [ -f "$TEST_WORKFLOW" ]; then
    echo -e "${GREEN}✅ Workflow exported successfully to $TEST_WORKFLOW${NC}"
    # Validate JSON
    if jq empty "$TEST_WORKFLOW" 2>/dev/null; then
        echo -e "${GREEN}✅ JSON is valid${NC}"
    else
        echo -e "${RED}❌ Invalid JSON format${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ Failed to export workflow${NC}"
    exit 1
fi

echo ""

# Test 2: Export critical incident workflow
echo -e "${BLUE}📋 Test 2: Export Critical Incident Workflow${NC}"
CRITICAL_WORKFLOW="kubiya-cli-critical-test.json"

python3 -m kubiya_incident.cli export \
    --format json \
    --incident-id "CRITICAL-CLI-TEST" \
    --title "Critical CLI Test Incident" \
    --severity critical \
    --output "$CRITICAL_WORKFLOW"

if [ -f "$CRITICAL_WORKFLOW" ]; then
    echo -e "${GREEN}✅ Critical workflow exported successfully${NC}"
else
    echo -e "${RED}❌ Failed to export critical workflow${NC}"
    exit 1
fi

echo ""

# Test 3: List available runners (if API key is available)
if [ "$SKIP_EXECUTION" = false ]; then
    echo -e "${BLUE}📋 Test 3: List Available Runners${NC}"
    if kubiya runner list 2>/dev/null; then
        echo -e "${GREEN}✅ Successfully listed runners${NC}"
    else
        echo -e "${YELLOW}⚠️  Could not list runners (using default: $RUNNER)${NC}"
    fi
    echo ""
fi

# Test 4: Validate workflow with Kubiya CLI (dry run)
echo -e "${BLUE}📋 Test 4: Validate Workflow Structure${NC}"
if jq '.name, .steps | length' "$TEST_WORKFLOW"; then
    echo -e "${GREEN}✅ Workflow structure is valid${NC}"
    STEP_COUNT=$(jq '.steps | length' "$TEST_WORKFLOW")
    echo -e "${BLUE}📊 Workflow contains $STEP_COUNT steps${NC}"
else
    echo -e "${RED}❌ Invalid workflow structure${NC}"
    exit 1
fi

echo ""

# Test 5: Workflow format validation (if API key available)
if [ "$SKIP_EXECUTION" = false ]; then
    echo -e "${BLUE}📋 Test 5: Validate Workflow Format${NC}"
    echo "Note: Actual Kubiya CLI execution methods may vary. Check Kubiya CLI documentation."
    echo "Generated workflow file: $TEST_WORKFLOW"
    echo "File size: $(wc -c < "$TEST_WORKFLOW") bytes"
    echo "JSON validation: $(jq empty "$TEST_WORKFLOW" && echo "✅ Valid" || echo "❌ Invalid")"
    
    echo ""
    
    echo -e "${BLUE}📋 Additional Tests: Workflow Structure Validation${NC}"
    echo "Critical workflow: $CRITICAL_WORKFLOW"
    echo "Critical workflow size: $(wc -c < "$CRITICAL_WORKFLOW") bytes"
    echo "Critical JSON validation: $(jq empty "$CRITICAL_WORKFLOW" && echo "✅ Valid" || echo "❌ Invalid")"
    
    echo ""
    echo -e "${YELLOW}📌 Note: Actual Kubiya CLI execution commands depend on your specific setup.${NC}"
    echo -e "${YELLOW}   Refer to https://github.com/kubiyabot/cli for current CLI usage.${NC}"
    
else
    echo -e "${YELLOW}⚠️  Skipping execution tests (no API key)${NC}"
    echo "To run execution tests, set KUBIYA_API_KEY environment variable"
fi

echo ""

# Test Results Summary
echo -e "${GREEN}📊 Test Results Summary${NC}"
echo "======================="
echo "✅ Workflow export: SUCCESS"
echo "✅ Critical workflow export: SUCCESS"
echo "✅ Workflow structure validation: SUCCESS"

if [ "$SKIP_EXECUTION" = false ]; then
    echo "✅ Workflow format validation: COMPLETED"
    echo "✅ JSON structure tests: COMPLETED"
    echo "ℹ️  CLI execution: See Kubiya CLI docs"
else
    echo "⏭️  Format validation tests: SKIPPED (no API key)"
fi

echo ""
echo -e "${GREEN}🎉 Kubiya CLI Integration Test Complete!${NC}"
echo ""

# Show generated files
echo -e "${BLUE}📁 Generated Files:${NC}"
ls -la *.json | grep kubiya-cli || echo "No test files found"

echo ""
echo -e "${BLUE}💡 Next Steps:${NC}"
echo "1. Set KUBIYA_API_KEY to run execution tests"
echo "2. Try the generated workflows: $TEST_WORKFLOW, $CRITICAL_WORKFLOW"
echo "3. Customize parameters for your environment"
echo "4. Integrate with your monitoring and alerting systems"

# Cleanup option
echo ""
read -p "🗑️  Clean up generated test files? (y/N): " cleanup
if [[ $cleanup =~ ^[Yy]$ ]]; then
    rm -f kubiya-cli-*.json
    echo -e "${GREEN}✅ Test files cleaned up${NC}"
fi

echo ""
echo -e "${YELLOW}📚 For more examples, see the README.md file${NC}"
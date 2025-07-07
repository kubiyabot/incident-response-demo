# Kubiya Incident Response Workflow

🚀 **Production-grade incident response workflow with intelligent service validation**

A comprehensive, automated incident response system built on the Kubiya Workflow SDK that provides intelligent service validation, Slack integration, and seamless workflow execution.

## 🌟 Features

- **🔄 Automated Incident Response**: End-to-end incident management workflow
- **🤖 Intelligent Service Validation**: AI-powered service validation and discovery
- **💬 Slack Integration**: Rich notifications and real-time updates
- **🎯 Multiple Export Formats**: JSON, YAML, and dictionary formats
- **🐳 Docker Support**: Containerized deployment and execution
- **🔧 Developer-Friendly**: Easy setup with comprehensive tooling
- **📊 Comprehensive Logging**: Full audit trail and debugging support

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ 
- pip or pipenv
- Docker (optional, for containerized deployment)
- Kubiya API key (for workflow execution)

### 1. Setup

```bash
# Clone and navigate to the project
cd kubiya_incident

# Run the setup script
./setup.sh

# Or for development setup with testing tools
./dev-setup.sh
```

### 2. Basic Usage

```bash
# Activate virtual environment
source venv/bin/activate

# Export workflow to JSON
kubiya-incident export --format json --output my-workflow.json

# Export workflow to YAML
kubiya-incident export --format yaml --output my-workflow.yaml

# Validate configuration
kubiya-incident validate --incident-id "TEST-123" --title "Test Incident" --severity medium

# Create service validation agent
kubiya-incident create-agent --incident-id "SERVICE-001" --title "Service Check" --severity high
```

### 3. Execute Workflow

```bash
# Set your API key
export KUBIYA_API_KEY="your-api-key-here"

# Execute workflow with basic parameters
kubiya-incident execute \
  --incident-id "PROD-001" \
  --title "Database Connection Issues" \
  --severity high \
  --services "user-api,payment-service,notification-service"

# Execute with streaming output
kubiya-incident execute \
  --incident-id "CRITICAL-001" \
  --title "Payment System Down" \
  --severity critical \
  --services "payment-gateway,billing-api" \
  --stream
```

## 📋 CLI Reference

### Commands

#### `export` - Export Workflow Configuration

Export workflow configuration to various formats for use with Kubiya CLI or visual editor.

```bash
kubiya-incident export [OPTIONS]
```

**Options:**
- `--format` - Export format: `json`, `yaml`, or `dict` (default: json)
- `--output` - Output file path (default: stdout)
- `--incident-id` - Template incident ID (default: TEMPLATE)
- `--title` - Template incident title (default: Template Incident)
- `--severity` - Template severity: `critical`, `high`, `medium`, `low` (default: medium)

**Examples:**
```bash
# Export to JSON file
kubiya-incident export --format json --output workflow.json

# Export to YAML with custom parameters
kubiya-incident export \
  --format yaml \
  --incident-id "TEMPLATE-CRITICAL" \
  --title "Critical Production Issue" \
  --severity critical \
  --output critical-workflow.yaml

# Export to stdout (pipe to other tools)
kubiya-incident export --format json | jq '.steps[0].name'
```

#### `execute` - Execute Incident Response Workflow

Execute the incident response workflow with real parameters.

```bash
kubiya-incident execute [OPTIONS]
```

**Required Options:**
- `--incident-id` - Unique incident identifier
- `--title` - Incident title/description
- `--severity` - Incident severity: `critical`, `high`, `medium`, `low`

**Optional Options:**
- `--services` - Comma-separated list of affected services
- `--priority` - Incident priority: `urgent`, `high`, `medium`, `low` (default: medium)
- `--owner` - Incident owner (default: ${KUBIYA_USER_EMAIL})
- `--source` - Incident source (default: cli)
- `--body` - Detailed incident description
- `--url` - Incident dashboard URL
- `--channel` - Slack channel ID
- `--stream` - Stream execution output

**Examples:**
```bash
# Basic execution
kubiya-incident execute \
  --incident-id "INC-2024-001" \
  --title "API Response Time Degradation" \
  --severity high

# Full execution with all parameters
kubiya-incident execute \
  --incident-id "INC-2024-002" \
  --title "Database Connection Pool Exhaustion" \
  --severity critical \
  --services "user-service,auth-service,notification-service" \
  --priority urgent \
  --owner "sre-team@company.com" \
  --body "Database connection pool exhausted, causing 500 errors" \
  --url "https://monitoring.company.com/incident/2024-002" \
  --channel "C1234567890" \
  --stream
```

#### `create-agent` - Create Service Validation Agent

Create a service validation agent configuration for discovering and validating services.

```bash
kubiya-incident create-agent [OPTIONS]
```

**Required Options:**
- `--incident-id` - Incident identifier
- `--title` - Incident title
- `--severity` - Incident severity

**Optional Options:**
- `--body` - Incident description
- `--output` - Output file for agent config

**Examples:**
```bash
# Create agent and output to file
kubiya-incident create-agent \
  --incident-id "SERVICE-VAL-001" \
  --title "Service Discovery for Payment Issues" \
  --severity high \
  --output service-agent.json

# Create agent and output to stdout
kubiya-incident create-agent \
  --incident-id "DISC-001" \
  --title "Microservice Discovery" \
  --severity medium
```

#### `validate` - Validate Workflow Configuration

Validate workflow configuration without executing.

```bash
kubiya-incident validate [OPTIONS]
```

**Required Options:**
- `--incident-id` - Incident identifier
- `--title` - Incident title
- `--severity` - Incident severity

**Optional Options:**
- `--services` - Comma-separated list of affected services

**Examples:**
```bash
# Basic validation
kubiya-incident validate \
  --incident-id "VAL-001" \
  --title "Configuration Test" \
  --severity medium

# Validation with services
kubiya-incident validate \
  --incident-id "VAL-002" \
  --title "Full Configuration Test" \
  --severity high \
  --services "api-gateway,user-service"
```

## 🐳 Docker Usage

### Build Docker Image

```bash
# Build with default settings
./docker-build.sh

# Build with custom tag
./docker-build.sh --tag v1.0.0

# Build and push to registry
./docker-build.sh --tag latest --push
```

### Run in Container

```bash
# Run CLI help
docker run --rm kubiya-incident-response:latest

# Export workflow
docker run --rm kubiya-incident-response:latest \
  kubiya-incident export --format json

# Execute workflow (requires API key)
docker run --rm \
  -e KUBIYA_API_KEY="your-api-key" \
  kubiya-incident-response:latest \
  kubiya-incident execute \
  --incident-id "DOCKER-001" \
  --title "Containerized Execution" \
  --severity medium
```

## 🔧 Development

### Setup Development Environment

```bash
# Run development setup
./dev-setup.sh

# This installs:
# - pytest, pytest-cov (testing)
# - black, flake8, mypy (code quality)
# - Development utility scripts
```

### Development Commands

```bash
# Format code
./format.sh

# Lint code
./lint.sh

# Type checking
./typecheck.sh

# Run tests with coverage
./test.sh

# Clean temporary files
./clean.sh
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=kubiya_incident --cov-report=html

# Run specific test file
pytest tests/test_workflow.py -v
```

## 📊 Workflow Export Examples

### JSON Format

The exported JSON workflow can be used directly with the Kubiya CLI:

```bash
# Export workflow
kubiya-incident export --format json --output workflow.json

# Execute with Kubiya CLI
kubiya workflow execute --file workflow.json --param incident_id="REAL-001" --param incident_title="Real Incident"
```

## 🧪 Testing with Kubiya CLI

### Prerequisites for CLI Testing

1. **Install Kubiya CLI**:
   ```bash
   # Install via npm
   npm install -g @kubiya/cli
   
   # Or download from releases
   # https://github.com/kubiya-ai/kubiya-cli/releases
   ```

2. **Set up authentication**:
   ```bash
   # Set your API key
   export KUBIYA_API_KEY="your-api-key-here"
   
   # Or configure via CLI
   kubiya auth login
   ```

### Basic CLI Testing

```bash
# 1. Export workflow to JSON
kubiya-incident export --format json --output test-workflow.json

# 2. Execute with Kubiya CLI
kubiya workflow execute test-workflow.json \
  --var incident_id="INC-99999" \
  --var incident_title="Database Connection Failure" \
  --var incident_severity="high" \
  --var incident_body="Primary database is not responding to queries" \
  --var incident_url="https://monitoring.example.com/INC-99999" \
  --var slack_channel_id="#kubi-incident-testing" \
  --runner gke-integration
```

### Advanced CLI Testing Examples

#### 1. Critical Incident Test

```bash
# Export critical incident workflow
kubiya-incident export \
  --format json \
  --incident-id "CRITICAL-TEMPLATE" \
  --title "Critical System Failure" \
  --severity critical \
  --output critical-test.json

# Execute with Kubiya CLI
kubiya workflow execute critical-test.json \
  --var incident_id="INC-CRITICAL-001" \
  --var incident_title="Payment System Complete Outage" \
  --var incident_severity="critical" \
  --var incident_priority="urgent" \
  --var incident_owner="sre-team@company.com" \
  --var incident_body="Payment processing system is completely down, affecting all transactions" \
  --var incident_url="https://status.company.com/incidents/critical-001" \
  --var affected_services="payment-gateway,billing-api,notification-service" \
  --var slack_channel_id="#incident-critical" \
  --var customer_impact="All payment processing is down" \
  --runner gke-integration
```

#### 2. Service Discovery Test (No Services Provided)

```bash
# Export basic workflow
kubiya-incident export --format json --output service-discovery-test.json

# Execute without affected_services to trigger agent creation
kubiya workflow execute service-discovery-test.json \
  --var incident_id="INC-DISCOVERY-001" \
  --var incident_title="Unknown Service Impact" \
  --var incident_severity="medium" \
  --var incident_body="Alert triggered but affected services unknown" \
  --var incident_url="https://monitoring.company.com/alerts/unknown-impact" \
  --var slack_channel_id="#incident-investigation" \
  --runner gke-integration
```

#### 3. High-Volume Testing

```bash
# Test multiple incidents with different parameters
for i in {1..5}; do
  kubiya workflow execute test-workflow.json \
    --var incident_id="INC-LOAD-$(printf '%03d' $i)" \
    --var incident_title="Load Test Incident $i" \
    --var incident_severity="medium" \
    --var incident_body="Load testing incident number $i" \
    --var incident_url="https://monitoring.example.com/INC-LOAD-$(printf '%03d' $i)" \
    --var slack_channel_id="#load-testing" \
    --runner gke-integration &
done
wait
```

### CLI Testing with Different Runners

```bash
# Test with different runners
RUNNERS=("gke-integration" "local-runner" "cloud-runner")

for runner in "${RUNNERS[@]}"; do
  echo "Testing with runner: $runner"
  kubiya workflow execute test-workflow.json \
    --var incident_id="INC-RUNNER-TEST-$(date +%s)" \
    --var incident_title="Runner Test: $runner" \
    --var incident_severity="low" \
    --var incident_body="Testing workflow execution with $runner" \
    --var slack_channel_id="#runner-testing" \
    --runner "$runner"
done
```

### CLI Testing Best Practices

#### 1. Parameter Validation Testing

```bash
# Test with missing required parameters
kubiya workflow execute test-workflow.json \
  --var incident_id="INC-MISSING-PARAMS" \
  --runner gke-integration
# Expected: Validation failure

# Test with invalid severity
kubiya workflow execute test-workflow.json \
  --var incident_id="INC-INVALID-SEVERITY" \
  --var incident_title="Invalid Severity Test" \
  --var incident_severity="invalid" \
  --runner gke-integration
# Expected: Validation failure
```

#### 2. Environment-Specific Testing

```bash
# Development environment
kubiya workflow execute test-workflow.json \
  --var incident_id="INC-DEV-001" \
  --var incident_title="Development Test" \
  --var incident_severity="low" \
  --var incident_body="Development environment test" \
  --var incident_url="https://dev-monitoring.company.com/INC-DEV-001" \
  --var slack_channel_id="#dev-incidents" \
  --runner gke-integration

# Staging environment  
kubiya workflow execute test-workflow.json \
  --var incident_id="INC-STAGING-001" \
  --var incident_title="Staging Test" \
  --var incident_severity="medium" \
  --var incident_body="Staging environment test" \
  --var incident_url="https://staging-monitoring.company.com/INC-STAGING-001" \
  --var slack_channel_id="#staging-incidents" \
  --runner gke-integration

# Production environment (use with caution)
kubiya workflow execute test-workflow.json \
  --var incident_id="INC-PROD-001" \
  --var incident_title="Production Test" \
  --var incident_severity="high" \
  --var incident_body="Production environment test - use with caution" \
  --var incident_url="https://monitoring.company.com/INC-PROD-001" \
  --var slack_channel_id="#production-incidents" \
  --runner gke-integration
```

#### 3. Automated Testing Scripts

Create a test suite script:

```bash
#!/bin/bash
# test-suite.sh - Comprehensive testing script

set -e

echo "🧪 Starting Kubiya CLI Test Suite"
echo "================================="

# Test 1: Basic validation
echo "Test 1: Basic Parameter Validation"
kubiya workflow execute test-workflow.json \
  --var incident_id="INC-TEST-001" \
  --var incident_title="Basic Validation Test" \
  --var incident_severity="medium" \
  --runner gke-integration

# Test 2: Service validation
echo "Test 2: Service Validation"
kubiya workflow execute test-workflow.json \
  --var incident_id="INC-TEST-002" \
  --var incident_title="Service Validation Test" \
  --var incident_severity="high" \
  --var affected_services="user-api,payment-service" \
  --runner gke-integration

# Test 3: Agent creation
echo "Test 3: Agent Creation (no services)"
kubiya workflow execute test-workflow.json \
  --var incident_id="INC-TEST-003" \
  --var incident_title="Agent Creation Test" \
  --var incident_severity="medium" \
  --runner gke-integration

# Test 4: Critical incident
echo "Test 4: Critical Incident"
kubiya workflow execute test-workflow.json \
  --var incident_id="INC-TEST-004" \
  --var incident_title="Critical Test" \
  --var incident_severity="critical" \
  --var incident_priority="urgent" \
  --var affected_services="core-api,database,cache" \
  --runner gke-integration

echo "✅ All tests completed successfully!"
```

### CLI Testing Output Analysis

#### 1. Successful Execution
```bash
# Look for these success indicators
kubiya workflow execute test-workflow.json \
  --var incident_id="INC-SUCCESS-001" \
  --var incident_title="Success Test" \
  --var incident_severity="medium" \
  --runner gke-integration

# Expected output:
# ✅ Workflow executed successfully
# 📋 Incident ID: INC-SUCCESS-001
# 🔥 Severity: medium
# 📊 Steps completed: 8/8
```

#### 2. Validation Failures
```bash
# Test validation failure
kubiya workflow execute test-workflow.json \
  --var incident_id="INC-FAIL-001" \
  --runner gke-integration

# Expected output:
# ❌ Validation failed. Missing parameters: incident_title incident_severity
```

#### 3. Agent Creation
```bash
# Test agent creation
kubiya workflow execute test-workflow.json \
  --var incident_id="INC-AGENT-001" \
  --var incident_title="Agent Test" \
  --var incident_severity="medium" \
  --runner gke-integration

# Expected output:
# 🤖 Service validation agent created
# 📧 Slack notification sent
# 🔄 Workflow can be re-triggered with validated services
```

### Troubleshooting CLI Testing

#### Common Issues and Solutions

1. **Authentication Errors**
   ```bash
   # Error: Unauthorized
   # Solution: Check API key
   export KUBIYA_API_KEY="your-correct-api-key"
   ```

2. **Runner Not Found**
   ```bash
   # Error: Runner 'invalid-runner' not found
   # Solution: Use valid runner name
   kubiya runner list  # List available runners
   ```

3. **Parameter Validation Errors**
   ```bash
   # Error: Required parameter missing
   # Solution: Check all required variables are provided
   kubiya workflow execute test-workflow.json \
     --var incident_id="INC-001" \
     --var incident_title="Test" \
     --var incident_severity="medium" \
     --runner gke-integration
   ```

4. **Workflow File Not Found**
   ```bash
   # Error: File not found
   # Solution: Use absolute path or verify file location
   kubiya workflow execute "$(pwd)/test-workflow.json" \
     --var incident_id="INC-001" \
     --runner gke-integration
   ```

### YAML Format

Perfect for version control and visual editing:

```bash
# Export workflow
kubiya-incident export --format yaml --output workflow.yaml

# View in editor or version control
git add workflow.yaml
git commit -m "Add incident response workflow"
```

### Integration Examples

#### CI/CD Pipeline

```yaml
# .github/workflows/deploy-workflow.yml
name: Deploy Incident Response Workflow

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
          
      - name: Install dependencies
        run: |
          cd kubiya_incident
          ./setup.sh
          
      - name: Export workflow
        run: |
          source venv/bin/activate
          kubiya-incident export --format json --output production-workflow.json
          
      - name: Deploy to Kubiya
        run: |
          kubiya workflow deploy --file production-workflow.json
        env:
          KUBIYA_API_KEY: ${{ secrets.KUBIYA_API_KEY }}
```

#### Kubernetes Deployment

```yaml
# kubernetes/incident-response-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: incident-response-workflow
spec:
  replicas: 2
  selector:
    matchLabels:
      app: incident-response
  template:
    metadata:
      labels:
        app: incident-response
    spec:
      containers:
      - name: incident-response
        image: kubiya-incident-response:latest
        env:
        - name: KUBIYA_API_KEY
          valueFrom:
            secretKeyRef:
              name: kubiya-secrets
              key: api-key
        command: ["kubiya-incident"]
        args: ["execute", "--incident-id", "$(INCIDENT_ID)", "--title", "$(INCIDENT_TITLE)", "--severity", "$(INCIDENT_SEVERITY)"]
```

## 🎯 Use Cases

### 1. Automated Incident Response

```bash
# Monitor triggers this when alert fires
kubiya-incident execute \
  --incident-id "$(date +%Y%m%d-%H%M%S)" \
  --title "High CPU Usage on Production" \
  --severity high \
  --services "web-api,background-workers" \
  --owner "sre-team@company.com"
```

### 2. Service Discovery and Validation

```bash
# Create agent for unknown service issues
kubiya-incident create-agent \
  --incident-id "UNKNOWN-SERVICES-001" \
  --title "Service Discovery Required" \
  --severity medium \
  --output discovery-agent.json

# Agent helps discover and validate services
# Then re-trigger workflow with validated services
```

### 3. Workflow Template Generation

```bash
# Generate templates for different severity levels
kubiya-incident export --severity critical --output critical-template.json
kubiya-incident export --severity high --output high-template.json
kubiya-incident export --severity medium --output medium-template.json
kubiya-incident export --severity low --output low-template.json
```

### 4. Integration Testing

```bash
# Validate configuration before deployment
kubiya-incident validate \
  --incident-id "TEST-$(date +%s)" \
  --title "Pre-deployment Configuration Test" \
  --severity medium \
  --services "api-gateway,user-service,payment-service"
```

## 🔐 Environment Variables

### Required for Execution

- `KUBIYA_API_KEY` - Your Kubiya API key for workflow execution

### Optional Configuration

- `KUBIYA_USER_EMAIL` - Default incident owner (used if --owner not specified)
- `SLACK_CHANNEL_ID` - Default Slack channel for notifications
- `INCIDENT_DASHBOARD_URL` - Base URL for incident dashboard links

### Example Environment Setup

```bash
# .env file
KUBIYA_API_KEY=your-api-key-here
KUBIYA_USER_EMAIL=sre-team@company.com
SLACK_CHANNEL_ID=C1234567890
INCIDENT_DASHBOARD_URL=https://monitoring.company.com/incidents
```

## 📝 Configuration

### Incident Configuration

The workflow accepts these configuration parameters:

```python
{
    "incident_id": "REQUIRED - Unique incident identifier",
    "incident_title": "REQUIRED - Incident title",
    "incident_severity": "REQUIRED - critical|high|medium|low",
    "incident_priority": "OPTIONAL - urgent|high|medium|low",
    "incident_owner": "OPTIONAL - Incident owner email",
    "incident_source": "OPTIONAL - Source of incident (cli, monitoring, etc.)",
    "incident_body": "OPTIONAL - Detailed description", 
    "incident_url": "OPTIONAL - Dashboard URL",
    "affected_services": "OPTIONAL - Comma-separated service list",
    "slack_channel_id": "OPTIONAL - Slack channel for notifications"
}
```

### Service Validation Agent

When `affected_services` is not provided, the workflow automatically creates a service validation agent with these capabilities:

- **Service Discovery**: List all Kubernetes services
- **Service Validation**: Validate specific service names
- **Cluster Investigation**: Comprehensive cluster analysis
- **Deployment Checks**: Recent Helm deployments
- **Workflow Re-trigger**: Re-run workflow with validated services

## 🚨 Error Handling

The workflow includes comprehensive error handling:

### Validation Errors

```bash
# Missing required parameters
kubiya-incident validate --incident-id "TEST"
# Output: ❌ ERROR: incident_title is required

# Invalid severity
kubiya-incident validate --incident-id "TEST" --title "Test" --severity "invalid"
# Output: ❌ ERROR: Invalid severity 'invalid'. Must be: critical, high, medium, or low
```

### Execution Errors

```bash
# Missing API key
kubiya-incident execute --incident-id "TEST" --title "Test" --severity medium
# Output: ❌ Error executing workflow: KUBIYA_API_KEY is required for workflow execution
```

### Agent Creation Errors

```bash
# Invalid parameters
kubiya-incident create-agent --incident-id "TEST"
# Output: ❌ Error creating agent: incident_title is required
```

## 📈 Monitoring and Logging

### Execution Logging

```bash
# Stream execution with detailed logging
kubiya-incident execute \
  --incident-id "MONITOR-001" \
  --title "Monitoring Test" \
  --severity medium \
  --stream
```

### Health Checks

```bash
# Validate system health
kubiya-incident validate \
  --incident-id "HEALTH-CHECK" \
  --title "System Health" \
  --severity low
```

### Docker Health Check

The Docker image includes a built-in health check:

```bash
# Check container health
docker ps --filter "name=incident-response" --format "table {{.Names}}\\t{{.Status}}"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Run the development setup: `./dev-setup.sh`
4. Make your changes
5. Run tests and linting: `./test.sh && ./lint.sh`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation**: This README and inline code documentation
- **Issues**: GitHub Issues for bug reports and feature requests
- **Community**: Kubiya Community Discord
- **Enterprise**: Contact support@kubiya.ai for enterprise support

---

Made with ❤️ by the Kubiya team

## 🚀 Quick Reference - Copy & Paste Commands

### Setup and Export
```bash
# 1. Setup environment
./setup.sh && source venv/bin/activate

# 2. Export workflow
kubiya-incident export --format json --output my-workflow.json

# 3. Test with Kubiya CLI
./examples/test-with-kubiya-cli.sh
```

### Ready-to-Use Kubiya CLI Commands

```bash
# Basic incident (copy and modify as needed)
kubiya workflow execute my-workflow.json \
  --var incident_id="INC-$(date +%Y%m%d-%H%M%S)" \
  --var incident_title="Your Incident Title Here" \
  --var incident_severity="high" \
  --var incident_body="Detailed description of the incident" \
  --var incident_url="https://your-monitoring.com/incident-url" \
  --var slack_channel_id="#your-incident-channel" \
  --runner gke-integration

# With affected services
kubiya workflow execute my-workflow.json \
  --var incident_id="INC-$(date +%Y%m%d-%H%M%S)" \
  --var incident_title="Service Outage" \
  --var incident_severity="critical" \
  --var affected_services="api-gateway,user-service,payment-service" \
  --var incident_body="Multiple services experiencing issues" \
  --var slack_channel_id="#critical-incidents" \
  --runner gke-integration

# Service discovery (no services specified)
kubiya workflow execute my-workflow.json \
  --var incident_id="INC-DISCOVERY-$(date +%Y%m%d-%H%M%S)" \
  --var incident_title="Unknown Service Impact" \
  --var incident_severity="medium" \
  --var incident_body="Alert triggered, investigating affected services" \
  --var slack_channel_id="#incident-investigation" \
  --runner gke-integration
```

### Environment Variables
```bash
# Required for execution
export KUBIYA_API_KEY="your-api-key-here"

# Optional defaults
export KUBIYA_USER_EMAIL="your-email@company.com"
export SLACK_CHANNEL_ID="#incidents"
export KUBIYA_RUNNER="gke-integration"
```

## 📚 Additional Resources

- [Kubiya Workflow SDK Documentation](https://docs.kubiya.ai/workflow-sdk)
- [Kubiya CLI Documentation](https://docs.kubiya.ai/cli)
- [Incident Response Best Practices](https://docs.kubiya.ai/best-practices/incident-response)
- [Service Validation Guide](https://docs.kubiya.ai/guides/service-validation)
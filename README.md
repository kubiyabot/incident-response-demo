# Kubiya Incident Response Workflow

Production-grade incident response workflow with intelligent service validation for Kubernetes environments.

## 🚀 Quick Start

### 1. Setup

```bash
# Setup environment
./setup.sh

# Or for development
./dev-setup.sh
```

### 2. Export Workflow

```bash
# Activate environment
source venv/bin/activate

# Export to JSON for Kubiya CLI
python -m kubiya_incident.cli export --format json --output incident-workflow.json

# Export with custom parameters
python -m kubiya_incident.cli export \
  --format json \
  --incident-id "PROD-TEMPLATE" \
  --title "Production Incident" \
  --severity critical \
  --output prod-incident.json
```

### 3. Use with Kubiya CLI

#### Install Kubiya CLI

**Debian/Ubuntu:**
```bash
curl -fsSL https://cli.kubiya.ai/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/kubiya-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/kubiya-archive-keyring.gpg] https://cli.kubiya.ai/apt stable main" | sudo tee /etc/apt/sources.list.d/kubiya.list
sudo apt update
sudo apt install kubiya-cli
```

**From Source:**
```bash
git clone https://github.com/kubiyabot/cli.git
cd cli
make build
make install
```

#### Execute Workflow

```bash
# Set API key
export KUBIYA_API_KEY="your-api-key"

# Execute workflow (replace with actual execution method)
kubiya tool execute incident-response \
  --incident-id "INC-$(date +%Y%m%d-%H%M%S)" \
  --title "Database Connection Failure" \
  --severity "high" \
  --services "user-api,payment-service"
```

## 📋 CLI Commands

### Export Commands
```bash
# Basic export
python -m kubiya_incident.cli export --format json

# Export to file
python -m kubiya_incident.cli export --format yaml --output workflow.yaml

# Custom parameters
python -m kubiya_incident.cli export \
  --incident-id "INC-123" \
  --title "Custom Incident" \
  --severity high \
  --format json
```

### Validation
```bash
# Validate configuration
python -m kubiya_incident.cli validate \
  --incident-id "TEST-123" \
  --title "Test Incident" \
  --severity medium
```

### Service Agent Creation
```bash
# Create service validation agent
python -m kubiya_incident.cli create-agent \
  --incident-id "SERVICE-001" \
  --title "Service Discovery" \
  --severity high \
  --output agent.json
```

## 🏗️ Workflow Features

- **🔄 Automated Incident Response**: Complete incident management workflow
- **🤖 Service Validation**: AI agent for Kubernetes service discovery
- **💬 Slack Integration**: Real-time notifications and updates
- **📊 Multiple Formats**: Export to JSON/YAML
- **🎯 Conditional Logic**: Smart service validation vs. agent creation

## 🐳 Docker

```bash
# Build container
./docker-build.sh

# Run with Docker
docker run --rm \
  -e KUBIYA_API_KEY="your-key" \
  kubiya-incident-response:latest \
  python -m kubiya_incident.cli export --format json
```

## 🔧 Development

```bash
# Setup dev environment with testing tools
./dev-setup.sh

# Format code
./format.sh

# Run lints
./lint.sh

# Run tests
./test.sh
```

## 📁 Generated Files

- `examples/workflow-basic.json` - Basic incident workflow
- `examples/workflow-critical.json` - Critical incident template
- `examples/service-validation-agent.json` - Service validation agent config

## 🎯 Integration

This workflow is designed to be triggered by monitoring systems and integrates with:
- Kubernetes clusters for service validation
- Slack for real-time communication
- Kubiya platform for workflow execution

## 📝 Configuration

Required environment variables:
- `KUBIYA_API_KEY` - For workflow execution (optional for export)

Optional:
- `KUBIYA_USER_EMAIL` - Default incident owner
- `SLACK_CHANNEL_ID` - Default notification channel

## 🔗 Links

- [Kubiya CLI Repository](https://github.com/kubiyabot/cli)
- [Kubiya Workflow SDK](https://github.com/kubiyabot/workflow-sdk)
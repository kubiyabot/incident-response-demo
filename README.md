# Kubiya Incident Response Workflow

Production-grade incident response workflow with intelligent service validation for Kubernetes environments.

## 🔄 End-to-End Workflow Architecture

```mermaid
flowchart TD
    %% Development Phase
    A[Python DSL Code] --> B[IncidentWorkflow Class]
    B --> C[Configuration Schema]
    C --> D[Workflow Steps Definition]
    
    %% Compilation Phase
    D --> E[CLI Export Command]
    E --> F{Export Format}
    F -->|JSON| G[workflow.json]
    F -->|YAML| H[workflow.yaml]
    
    %% Kubiya Platform Integration
    G --> I[compose.kubiya.ai/workflow/designer]
    H --> I
    I --> J[Visual Workflow Editor]
    J --> K[Modified Workflow]
    K --> L[Platform Deployment]
    
    %% MCP Server Integration
    L --> M[Kubiya MCP Server]
    M --> N[Agent Access Layer]
    N --> O[AI Agents Can Call Workflow]
    
    %% Runtime Execution
    O --> P{Trigger Source}
    P -->|Agent Call| Q[Agent-Triggered Execution]
    P -->|Direct API| R[Direct API Execution]
    P -->|Monitoring Alert| S[Alert-Triggered Execution]
    
    Q --> T[Workflow Engine]
    R --> T
    S --> T
    
    T --> U[Step Execution]
    U --> V[Kubernetes Validation]
    U --> W[Slack Notifications]
    U --> X[Service Discovery]
    
    %% Conditional Logic
    V --> Y{Services Provided?}
    Y -->|Yes| Z[Execute Incident Steps]
    Y -->|No| AA[Create Service Agent]
    AA --> BB[Agent Helps Discover Services]
    BB --> CC[Re-trigger with Services]
    CC --> Z
    
    %% Output
    Z --> DD[Slack Updates]
    Z --> EE[Incident Dashboard]
    Z --> FF[Kubernetes Actions]
```

## 🏗️ Workflow Steps Flow

```mermaid
flowchart LR
    A[1. Validate Incident] --> B[2. Setup Slack]
    B --> C{Services Known?}
    C -->|No| D[3. Create Agent]
    C -->|Yes| E[4. Post Alert]
    D --> F[5. Agent Notification]
    E --> G[6. Execute Response]
    F --> H[7. Wait for Discovery]
    G --> I[8. Monitor & Update]
```

## 📊 MCP Server Integration

```mermaid
sequenceDiagram
    participant A as AI Agent
    participant M as Kubiya MCP Server
    participant W as Incident Workflow
    participant K as Kubernetes
    participant S as Slack API

    A->>M: Call incident-response tool
    M->>W: Trigger workflow execution
    W->>W: Validate parameters
    
    alt Services provided
        W->>S: Post incident alert
        W->>K: Validate services
        W->>S: Update with status
    else Services unknown
        W->>M: Create service validation agent
        M->>A: New agent available
        A->>K: Discover services
        A->>M: Re-trigger with services
        M->>W: Execute with validated services
    end
    
    W->>A: Return execution results
```

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

### 3. Kubiya Platform Integration

#### Visual Workflow Designer

1. **Export your workflow:**
   ```bash
   python -m kubiya_incident.cli export --format json --output incident-workflow.json
   ```

2. **Import to Workflow Designer:**
   - Navigate to [compose.kubiya.ai/workflow/designer](https://compose.kubiya.ai/workflow/designer)
   - Click "Import" or "Load JSON"
   - Upload your `incident-workflow.json` file
   - Modify steps visually using the drag-and-drop interface
   - Add/remove steps, modify parameters, change conditions
   - Export modified workflow back to JSON/YAML

3. **Deploy to Platform:**
   - Use the platform's deployment features
   - Configure triggers (webhooks, schedules, agent calls)
   - Set up environment variables and secrets
   - Enable MCP server integration for agent access

### 4. Use with Kubiya CLI

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

## 🔧 Workflow Customization

### JSON Structure for Workflow Designer

The exported JSON follows the Kubiya Workflow SDK format:

```json
{
  "name": "production-incident-workflow",
  "description": "Automated incident response with service validation",
  "params": {
    "incident_id": "INC-123",
    "incident_title": "Incident Title",
    "incident_severity": "high",
    "affected_services": "service1,service2"
  },
  "steps": [
    {
      "name": "validate-incident",
      "description": "Validate incident parameters",
      "executor": {"type": "command", "config": {}},
      "command": "# Validation logic here",
      "output": "validation_status"
    }
  ]
}
```

**Key Components for Designer:**
- `name`: Workflow identifier
- `description`: Human-readable description
- `params`: Input parameters with default values
- `steps`: Array of executable steps with dependencies
- `executor`: Execution environment configuration

### Example: Adding Custom Step

```python
# In workflows/incident_response.py
def _create_custom_monitoring_step(self) -> Dict[str, Any]:
    return {
        "name": "setup-monitoring-alerts",
        "description": "Configure monitoring for incident tracking",
        "command": """
            # Custom monitoring setup
            echo "Setting up monitoring for incident ${incident_id}"
            # Add your monitoring logic here
        """,
        "executor": {"type": "command", "config": {}},
        "depends": ["validate-incident"],
        "output": "monitoring_status"
    }
```

## 🏗️ Workflow Features

- **🔄 Automated Incident Response**: Complete incident management workflow
- **🤖 Service Validation**: AI agent for Kubernetes service discovery
- **💬 Slack Integration**: Real-time notifications and updates
- **📊 Multiple Formats**: Export to JSON/YAML
- **🎯 Conditional Logic**: Smart service validation vs. agent creation
- **🔧 Highly Customizable**: Modify steps, add custom logic, change integrations

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
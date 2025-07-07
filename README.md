# Kubiya Incident Response Workflow

Production-grade incident response workflow with intelligent service validation for Kubernetes environments.

## 🔄 End-to-End Workflow Architecture

```mermaid
graph TB
    subgraph "Development Phase"
        A[Python DSL Code] --> B[IncidentWorkflow Class]
        B --> C[Configuration Schema]
        C --> D[Workflow Steps Definition]
    end
    
    subgraph "Compilation Phase"
        D --> E[CLI Export Command]
        E --> F{Export Format}
        F -->|JSON| G[workflow.json]
        F -->|YAML| H[workflow.yaml]
    end
    
    subgraph "Kubiya Platform Integration"
        G --> I[compose.kubiya.ai/workflow/designer]
        H --> I
        I --> J[Visual Workflow Editor]
        J --> K[Modified Workflow]
        K --> L[Platform Deployment]
    end
    
    subgraph "MCP Server Integration"
        L --> M[Kubiya MCP Server]
        M --> N[Agent Access Layer]
        N --> O[AI Agents Can Call Workflow]
    end
    
    subgraph "Runtime Execution"
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
    end
    
    subgraph "Conditional Logic"
        V --> Y{Services Provided?}
        Y -->|Yes| Z[Execute Incident Steps]
        Y -->|No| AA[Create Service Agent]
        AA --> BB[Agent Helps Discover Services]
        BB --> CC[Re-trigger with Services]
        CC --> Z
    end
    
    subgraph "Output & Integration"
        Z --> DD[Slack Updates]
        Z --> EE[Incident Dashboard]
        Z --> FF[Kubernetes Actions]
        DD --> GG[Team Notification]
        EE --> HH[Status Tracking]
        FF --> II[Service Recovery]
    end

    classDef development fill:#e1f5fe
    classDef compilation fill:#f3e5f5
    classDef platform fill:#e8f5e8
    classDef runtime fill:#fff3e0
    classDef conditional fill:#fce4ec
    classDef output fill:#f1f8e9
    
    class A,B,C,D development
    class E,F,G,H compilation
    class I,J,K,L,M,N,O platform
    class P,Q,R,S,T,U,V,W runtime
    class Y,Z,AA,BB,CC conditional
    class DD,EE,FF,GG,HH,II output
```

## 🏗️ Workflow Components Architecture

```mermaid
graph LR
    subgraph "DSL Components"
        A[IncidentConfig] --> B[Validation Rules]
        A --> C[Environment Variables]
        A --> D[Service Parameters]
    end
    
    subgraph "Workflow Steps"
        E[1. Validate Incident] --> F[2. Setup Slack]
        F --> G[3. Service Check]
        G --> H{Services Known?}
        H -->|No| I[4a. Create Agent]
        H -->|Yes| J[4b. Post Alert]
        I --> K[5a. Agent Notification]
        J --> L[5b. Execute Response]
        K --> M[6. Wait for Discovery]
        L --> N[6. Monitor & Update]
    end
    
    subgraph "Integration Points"
        O[Kubernetes API] --> P[Service Discovery]
        Q[Slack API] --> R[Real-time Updates]
        S[Kubiya MCP] --> T[Agent Integration]
    end
    
    B --> E
    P --> G
    R --> F
    T --> I
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

#### MCP Server Integration

```mermaid
sequenceDiagram
    participant Agent as AI Agent
    participant MCP as Kubiya MCP Server
    participant Workflow as Incident Workflow
    participant K8s as Kubernetes
    participant Slack as Slack API

    Agent->>MCP: Call incident-response tool
    MCP->>Workflow: Trigger workflow execution
    Workflow->>Workflow: Validate parameters
    alt Services provided
        Workflow->>Slack: Post incident alert
        Workflow->>K8s: Validate services
        Workflow->>Slack: Update with status
    else Services unknown
        Workflow->>MCP: Create service validation agent
        MCP->>Agent: New agent available
        Agent->>K8s: Discover services
        Agent->>MCP: Re-trigger with services
        MCP->>Workflow: Execute with validated services
    end
    Workflow->>Agent: Return execution results
```

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

### Modifying Workflow Steps

The workflow consists of 8 main steps that can be customized:

```mermaid
flowchart TD
    A[1. validate-incident] --> B[2. setup-slack-integration]
    B --> C[3. handle-validation-failure]
    B --> D[4. post-incident-alert]
    C --> E[5. service-discovery-loop]
    D --> F[6. kubernetes-investigation]
    F --> G[7. notify-resolution-team]
    G --> H[8. update-incident-status]
    
    style A fill:#ffeb3b
    style B fill:#2196f3
    style C fill:#ff9800
    style D fill:#4caf50
    style E fill:#9c27b0
    style F fill:#f44336
    style G fill:#607d8b
    style H fill:#795548
```

### Customization Points

1. **Parameter Validation** (`validate-incident`):
   - Modify required fields in `core/config.py`
   - Add custom validation rules
   - Change severity levels

2. **Slack Integration** (`setup-slack-integration`):
   - Customize notification templates
   - Add different channels for different severities
   - Modify message formatting

3. **Service Discovery Logic** (`handle-validation-failure`):
   - Customize agent creation parameters
   - Modify service discovery tools
   - Add custom Kubernetes queries

4. **Alert Formatting** (`post-incident-alert`):
   - Design custom Slack block layouts
   - Add rich notifications
   - Include dashboard links

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
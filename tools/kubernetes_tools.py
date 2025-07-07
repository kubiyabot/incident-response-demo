"""
Kubernetes tools for service validation and cluster investigation.
"""

from typing import Any, Dict, List


class KubernetesToolDefinitions:
    """Kubernetes tool definitions for incident response agents."""

    @staticmethod
    def kubectl_get_services() -> Dict[str, Any]:
        """Tool to get all services in the Kubernetes cluster."""
        return {
            "name": "kubectl_get_services",
            "description": "Get all services in the Kubernetes cluster to validate service names and discover available services",
            "type": "docker",
            "image": "bitnami/kubectl:latest",
            "content": """#!/bin/bash
set -e

echo "🔍 KUBERNETES SERVICES DISCOVERY"
echo "================================="

# Get all services with detailed information
echo "📋 All services across all namespaces:"
kubectl get services --all-namespaces -o wide --show-labels

echo ""
echo "📊 Service summary by namespace:"
kubectl get services --all-namespaces --no-headers | awk '{print $1}' | sort | uniq -c | sort -nr

# Search for specific pattern if provided
if [ -n "$SERVICE_PATTERN" ]; then
    echo ""
    echo "🔍 Searching for services matching pattern: '$SERVICE_PATTERN'"
    kubectl get services --all-namespaces | grep -i "$SERVICE_PATTERN" || echo "❌ No services found matching pattern: $SERVICE_PATTERN"

    echo ""
    echo "🔍 Similar service names (fuzzy search):"
    kubectl get services --all-namespaces --no-headers | awk '{print $2}' | grep -i "$(echo $SERVICE_PATTERN | cut -c1-3)" || echo "No similar services found"
fi

echo ""
echo "✅ Services discovery completed"
            """,
            "args": {"SERVICE_PATTERN": "{{service_pattern}}"},
        }

    @staticmethod
    def validate_service_exists() -> Dict[str, Any]:
        """Tool to validate if a specific service exists."""
        return {
            "name": "validate_service_exists",
            "description": "Validate if a specific service exists in the Kubernetes cluster",
            "type": "docker",
            "image": "bitnami/kubectl:latest",
            "content": """#!/bin/bash
set -e

echo "🔍 VALIDATING SERVICE: $SERVICE_NAME"
echo "===================================="

NAMESPACE=${NAMESPACE:-default}
FOUND=false

# Check in specified namespace first
echo "🔍 Checking namespace: $NAMESPACE"
if kubectl get service "$SERVICE_NAME" -n "$NAMESPACE" 2>/dev/null; then
    echo "✅ Service '$SERVICE_NAME' found in namespace '$NAMESPACE'"
    FOUND=true

    # Get detailed service information
    echo ""
    echo "📋 Service details:"
    kubectl describe service "$SERVICE_NAME" -n "$NAMESPACE"

    echo ""
    echo "🔗 Service endpoints:"
    kubectl get endpoints "$SERVICE_NAME" -n "$NAMESPACE" 2>/dev/null || echo "No endpoints found"
else
    echo "❌ Service '$SERVICE_NAME' not found in namespace '$NAMESPACE'"
fi

# If not found in specified namespace, search all namespaces
if [ "$FOUND" = "false" ]; then
    echo ""
    echo "🔍 Searching across all namespaces..."
    ALL_MATCHES=$(kubectl get services --all-namespaces --no-headers | grep "$SERVICE_NAME" || true)

    if [ -n "$ALL_MATCHES" ]; then
        echo "✅ Found matching services:"
        echo "$ALL_MATCHES"
        FOUND=true
    else
        echo "❌ Service '$SERVICE_NAME' not found in any namespace"

        # Suggest similar services
        echo ""
        echo "💡 Similar service names found:"
        kubectl get services --all-namespaces --no-headers | awk '{print $1 ":" $2}' | grep -i "$(echo $SERVICE_NAME | cut -c1-3)" | head -5 || echo "No similar services found"
    fi
fi

if [ "$FOUND" = "true" ]; then
    echo ""
    echo "✅ Service validation successful"
    exit 0
else
    echo ""
    echo "❌ Service validation failed"
    exit 1
fi
            """,
            "args": {"SERVICE_NAME": "{{service_name}}", "NAMESPACE": "{{namespace:default}}"},
        }

    @staticmethod
    def kubectl_cluster_investigation() -> Dict[str, Any]:
        """Comprehensive Kubernetes cluster investigation tool."""
        return {
            "name": "kubectl_cluster_investigation",
            "description": "Perform comprehensive Kubernetes cluster investigation for incident analysis",
            "type": "docker",
            "image": "bitnami/kubectl:latest",
            "content": """#!/bin/bash
set -e

echo "🔍 KUBERNETES CLUSTER INVESTIGATION"
echo "===================================="

SERVICES=${AFFECTED_SERVICES:-"all"}
echo "🎯 Investigating services: $SERVICES"

echo ""
echo "1️⃣ CLUSTER OVERVIEW"
echo "==================="
echo "📊 Node status:"
kubectl get nodes -o wide

echo ""
echo "📊 Namespace overview:"
kubectl get namespaces

echo ""
echo "2️⃣ POD HEALTH ANALYSIS"
echo "======================="
echo "🔍 Pods with high restart counts (>5):"
kubectl get pods --all-namespaces --field-selector=status.phase=Running | awk 'NR>1 && $5>5 {print $0}' || echo "No pods with high restart counts found"

echo ""
echo "🔍 Failed/Pending pods:"
kubectl get pods --all-namespaces --field-selector=status.phase!=Running,status.phase!=Succeeded | head -20

echo ""
echo "3️⃣ SERVICE-SPECIFIC INVESTIGATION"
echo "=================================="
if [ "$SERVICES" != "all" ]; then
    IFS=',' read -ra SERVICE_ARRAY <<< "$SERVICES"
    for service in "${SERVICE_ARRAY[@]}"; do
        service=$(echo "$service" | xargs)  # trim whitespace
        echo ""
        echo "🔍 Investigating service: $service"

        # Find pods for this service
        kubectl get pods --all-namespaces -l app=$service -o wide 2>/dev/null || echo "No pods found with label app=$service"

        # Check service endpoints
        kubectl get services --all-namespaces | grep "$service" || echo "Service $service not found"
    done
fi

echo ""
echo "4️⃣ RECENT EVENTS"
echo "================="
echo "🔍 Recent cluster events (last 1 hour):"
kubectl get events --all-namespaces --sort-by='.lastTimestamp' | tail -20

echo ""
echo "5️⃣ RESOURCE UTILIZATION"
echo "========================"
echo "📊 Node resource usage:"
kubectl top nodes 2>/dev/null || echo "Metrics server not available"

echo ""
echo "📊 Top resource-consuming pods:"
kubectl top pods --all-namespaces --sort-by=memory 2>/dev/null | head -10 || echo "Metrics server not available"

echo ""
echo "✅ Cluster investigation completed"
            """,
            "args": {"AFFECTED_SERVICES": "{{affected_services}}"},
        }

    @staticmethod
    def helm_deployments_check() -> Dict[str, Any]:
        """Check recent Helm deployments."""
        return {
            "name": "helm_deployments_check",
            "description": "Check recent Helm deployments that might be related to the incident",
            "type": "docker",
            "image": "alpine/helm:latest",
            "content": """#!/bin/bash
set -e

echo "🔍 HELM DEPLOYMENTS ANALYSIS"
echo "============================="

# Install kubectl in helm image
apk add --no-cache curl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
mv kubectl /usr/local/bin/

echo "📋 All Helm releases:"
helm list --all-namespaces

echo ""
echo "🔍 Recent Helm deployments (last 6 hours):"
helm list --all-namespaces --date --output json | jq -r '.[] | select(.updated | strptime("%Y-%m-%d %H:%M:%S.%f %z") > (now - 6*3600)) | "\\(.name) (\\(.namespace)) - \\(.updated) - \\(.status)"' 2>/dev/null || echo "No recent deployments found or jq not available"

echo ""
echo "🔍 Failed Helm releases:"
helm list --all-namespaces --failed

echo ""
echo "📊 Helm release status summary:"
helm list --all-namespaces --output json | jq -r 'group_by(.status) | .[] | "\\(.[0].status): \\(length) releases"' 2>/dev/null || echo "Status summary not available"

echo ""
echo "✅ Helm analysis completed"
            """,
            "args": {},
        }

    @classmethod
    def get_all_tools(cls) -> List[Dict[str, Any]]:
        """Get all Kubernetes tools for agent configuration."""
        return [
            cls.kubectl_get_services(),
            cls.validate_service_exists(),
            cls.kubectl_cluster_investigation(),
            cls.helm_deployments_check(),
        ]

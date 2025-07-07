#!/bin/bash
# Development setup script for Kubiya Incident Response Workflow
set -e

echo "🔧 Setting up development environment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the project root directory (parent of kubiya_incident)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${BLUE}📁 Project root: $PROJECT_ROOT${NC}"

# Run basic setup first
echo -e "${YELLOW}🚀 Running basic setup...${NC}"
./kubiya_incident/setup.sh

# Activate virtual environment
source venv/bin/activate

# Install development dependencies
echo -e "${YELLOW}📦 Installing development dependencies...${NC}"
pip install pytest pytest-cov black flake8 mypy

# Create development directories
echo -e "${YELLOW}📁 Creating development directories...${NC}"
mkdir -p tests
mkdir -p docs
mkdir -p examples

# Create test configuration
if [ ! -f "pytest.ini" ]; then
    echo -e "${YELLOW}📝 Creating pytest configuration...${NC}"
    cat > pytest.ini << EOF
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --verbose --tb=short
EOF
fi

# Create a basic test file if it doesn't exist
if [ ! -f "tests/test_workflow.py" ]; then
    echo -e "${YELLOW}📝 Creating basic test file...${NC}"
    cat > tests/test_workflow.py << 'EOF'
"""
Basic tests for the incident response workflow.
"""
import pytest
from kubiya_incident.core.config import IncidentConfig
from kubiya_incident.core.workflow import IncidentWorkflow


def test_incident_config_creation():
    """Test creating an incident configuration."""
    config = IncidentConfig(
        incident_id="TEST-123",
        incident_title="Test Incident",
        incident_severity="medium"
    )
    assert config.incident_id == "TEST-123"
    assert config.incident_title == "Test Incident"
    assert config.incident_severity == "medium"


def test_workflow_creation():
    """Test creating a workflow from configuration."""
    config = IncidentConfig(
        incident_id="TEST-456",
        incident_title="Test Workflow",
        incident_severity="high"
    )
    workflow = IncidentWorkflow(config)
    assert workflow.config.incident_id == "TEST-456"


def test_workflow_export():
    """Test exporting workflow to various formats."""
    config = IncidentConfig(
        incident_id="TEST-789",
        incident_title="Export Test",
        incident_severity="low"
    )
    workflow = IncidentWorkflow(config)
    
    # Test JSON export
    json_output = workflow.to_json()
    assert "TEST-789" in json_output
    
    # Test YAML export
    yaml_output = workflow.to_yaml()
    assert "TEST-789" in yaml_output
    
    # Test dict export
    dict_output = workflow.to_dict()
    assert isinstance(dict_output, dict)
    assert "name" in dict_output
EOF
fi

# Create __init__.py for tests
if [ ! -f "tests/__init__.py" ]; then
    touch tests/__init__.py
fi

# Run tests to verify setup
echo -e "${YELLOW}🧪 Running tests to verify setup...${NC}"
python -m pytest tests/ -v

# Create development utility scripts
echo -e "${YELLOW}📝 Creating development utility scripts...${NC}"

# Format script
cat > format.sh << 'EOF'
#!/bin/bash
echo "🎨 Formatting code with black..."
black kubiya_incident/ tests/ --line-length 100
echo "✅ Code formatting complete!"
EOF
chmod +x format.sh

# Lint script
cat > lint.sh << 'EOF'
#!/bin/bash
echo "🔍 Linting code with flake8..."
flake8 kubiya_incident/ tests/ --max-line-length=100 --ignore=E203,W503
echo "✅ Linting complete!"
EOF
chmod +x lint.sh

# Type check script
cat > typecheck.sh << 'EOF'
#!/bin/bash
echo "🔎 Type checking with mypy..."
mypy kubiya_incident/ --ignore-missing-imports
echo "✅ Type checking complete!"
EOF
chmod +x typecheck.sh

# Test script
cat > test.sh << 'EOF'
#!/bin/bash
echo "🧪 Running tests..."
python -m pytest tests/ -v --cov=kubiya_incident --cov-report=html
echo "✅ Tests complete! Coverage report available in htmlcov/"
EOF
chmod +x test.sh

# Clean script
cat > clean.sh << 'EOF'
#!/bin/bash
echo "🧹 Cleaning up temporary files..."
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
rm -rf build/ dist/ htmlcov/ .coverage .pytest_cache/
echo "✅ Cleanup complete!"
EOF
chmod +x clean.sh

echo ""
echo -e "${GREEN}🎉 Development environment setup complete!${NC}"
echo ""
echo "Available development commands:"
echo -e "${YELLOW}./format.sh${NC}    - Format code with black"
echo -e "${YELLOW}./lint.sh${NC}      - Lint code with flake8"
echo -e "${YELLOW}./typecheck.sh${NC} - Type check with mypy"
echo -e "${YELLOW}./test.sh${NC}      - Run tests with coverage"
echo -e "${YELLOW}./clean.sh${NC}     - Clean temporary files"
echo ""
echo "To activate the virtual environment:"
echo -e "${YELLOW}source venv/bin/activate${NC}"
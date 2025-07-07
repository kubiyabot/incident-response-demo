#!/bin/bash
# Setup script for Kubiya Incident Response Workflow
set -e

echo "🚀 Setting up Kubiya Incident Response Workflow..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed${NC}"
    exit 1
fi

# Get the project root directory (parent of kubiya_incident)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${YELLOW}📁 Project root: $PROJECT_ROOT${NC}"

# Remove existing virtual environment if it exists
if [ -d "venv" ]; then
    echo -e "${YELLOW}🗑️  Removing existing virtual environment...${NC}"
    rm -rf venv
fi

# Create virtual environment
echo -e "${YELLOW}🔧 Creating virtual environment...${NC}"
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo -e "${YELLOW}⬆️  Upgrading pip...${NC}"
pip install --upgrade pip

# Install requirements
echo -e "${YELLOW}📦 Installing requirements...${NC}"
pip install -r requirements.txt

# Install package in development mode
echo -e "${YELLOW}🔧 Installing package in development mode...${NC}"
pip install -e .

# Verify installation
echo -e "${YELLOW}✅ Verifying installation...${NC}"
if command -v kubiya-incident &> /dev/null; then
    echo -e "${GREEN}✅ CLI installed successfully!${NC}"
    kubiya-incident --help
else
    echo -e "${RED}❌ CLI installation failed${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 Setup complete!${NC}"
echo ""
echo "To activate the virtual environment:"
echo -e "${YELLOW}source venv/bin/activate${NC}"
echo ""
echo "To run the CLI:"
echo -e "${YELLOW}kubiya-incident --help${NC}"
echo ""
echo "To deactivate the virtual environment:"
echo -e "${YELLOW}deactivate${NC}"
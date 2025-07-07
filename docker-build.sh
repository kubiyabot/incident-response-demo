#!/bin/bash
# Docker build script for Kubiya Incident Response Workflow
set -e

echo "🐳 Building Docker image for Kubiya Incident Response Workflow..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="kubiya-incident-response"
IMAGE_TAG="latest"
DOCKERFILE_PATH="./Dockerfile"

# Get the project root directory (parent of kubiya_incident)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${BLUE}📁 Project root: $PROJECT_ROOT${NC}"

# Parse command line arguments
BUILD_ARGS=""
PUSH_IMAGE=false
NO_CACHE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --tag|-t)
            IMAGE_TAG="$2"
            shift 2
            ;;
        --name|-n)
            IMAGE_NAME="$2"
            shift 2
            ;;
        --push|-p)
            PUSH_IMAGE=true
            shift
            ;;
        --no-cache)
            NO_CACHE=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --tag, -t TAG        Set image tag (default: latest)"
            echo "  --name, -n NAME      Set image name (default: kubiya-incident-response)"
            echo "  --push, -p           Push image to registry after build"
            echo "  --no-cache           Build without using cache"
            echo "  --help, -h           Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

FULL_IMAGE_NAME="$IMAGE_NAME:$IMAGE_TAG"

echo -e "${YELLOW}🏗️  Building image: $FULL_IMAGE_NAME${NC}"

# Build arguments
if [ "$NO_CACHE" = true ]; then
    BUILD_ARGS="--no-cache"
fi

# Build the Docker image
echo -e "${YELLOW}🔨 Running docker build...${NC}"
docker build $BUILD_ARGS -t "$FULL_IMAGE_NAME" -f kubiya_incident/Dockerfile .

# Verify the build
echo -e "${YELLOW}✅ Verifying image build...${NC}"
docker images | grep "$IMAGE_NAME"

# Test the image
echo -e "${YELLOW}🧪 Testing the image...${NC}"
docker run --rm "$FULL_IMAGE_NAME" kubiya-incident --help

# Push if requested
if [ "$PUSH_IMAGE" = true ]; then
    echo -e "${YELLOW}📤 Pushing image to registry...${NC}"
    docker push "$FULL_IMAGE_NAME"
    echo -e "${GREEN}✅ Image pushed successfully!${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Docker build complete!${NC}"
echo ""
echo "Image name: $FULL_IMAGE_NAME"
echo ""
echo "To run the container:"
echo -e "${YELLOW}docker run --rm $FULL_IMAGE_NAME kubiya-incident --help${NC}"
echo ""
echo "To run with environment variables:"
echo -e "${YELLOW}docker run --rm -e KUBIYA_API_KEY=your-key $FULL_IMAGE_NAME kubiya-incident execute --incident-id INC-123 --title 'Test' --severity medium${NC}"
echo ""
echo "To run interactively:"
echo -e "${YELLOW}docker run --rm -it $FULL_IMAGE_NAME /bin/bash${NC}"
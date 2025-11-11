#!/bin/bash

# =======================================================================
# 🚀 LOCAL DOCKER DEPLOYMENT - Insurance Bot
# =======================================================================
# Description: Chạy dự án local bằng Docker để test trước khi deploy server
# =======================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}=======================================================================${NC}"
    echo -e "${BLUE}🚀 INSURANCE BOT - LOCAL DOCKER DEPLOYMENT${NC}"
    echo -e "${BLUE}=======================================================================${NC}"
}

check_prerequisites() {
    echo -e "${YELLOW}🔍 Checking prerequisites...${NC}"

    # Check Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker is not installed${NC}"
        echo "Install Docker: https://docs.docker.com/get-docker/"
        exit 1
    fi

    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}❌ Docker Compose is not installed${NC}"
        echo "Install Docker Compose: https://docs.docker.com/compose/install/"
        exit 1
    fi

    # Check Docker daemon
    if ! docker info &> /dev/null; then
        echo -e "${RED}❌ Docker daemon is not running${NC}"
        echo "Start Docker service or Docker Desktop"
        exit 1
    fi

    echo -e "${GREEN}✅ All prerequisites met${NC}"
}

setup_config() {
    echo -e "${YELLOW}⚙️ Setting up configuration...${NC}"

    # Create .env if not exists
    if [ ! -f .env ]; then
        cp deploy.env .env
        echo -e "${GREEN}✅ Created .env from deploy.env${NC}"
    else
        echo -e "${GREEN}✅ .env already exists${NC}"
    fi

    # Update local settings
    sed -i 's|DOMAIN=.*|DOMAIN=localhost|' .env 2>/dev/null || true
    sed -i 's|API_HOST=.*|API_HOST=0.0.0.0|' .env 2>/dev/null || true

    echo -e "${GREEN}✅ Configuration ready${NC}"
}

deploy_local() {
    echo -e "${YELLOW}🐳 Starting local deployment...${NC}"

    # Stop existing containers
    docker-compose down 2>/dev/null || true

    # Build and start
    docker-compose -f docker-compose-simple.yml up -d --build

    echo -e "${GREEN}✅ Local deployment started${NC}"
}

wait_for_services() {
    echo -e "${YELLOW}⏳ Waiting for services to be ready...${NC}"

    # Wait for API to be healthy
    local max_attempts=30
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        if curl -f http://localhost:8001/health &> /dev/null; then
            echo -e "${GREEN}✅ API is healthy${NC}"
            return 0
        fi

        echo -e "${YELLOW}Waiting... (attempt $attempt/$max_attempts)${NC}"
        sleep 10
        ((attempt++))
    done

    echo -e "${RED}❌ API failed to become healthy${NC}"
    return 1
}

show_info() {
    echo -e "${BLUE}=======================================================================${NC}"
    echo -e "${GREEN}🎉 LOCAL DEPLOYMENT SUCCESSFUL!${NC}"
    echo -e "${BLUE}=======================================================================${NC}"
    echo ""
    echo -e "${GREEN}🌐 Local API Endpoints:${NC}"
    echo -e "   Health Check: http://localhost:8001/health"
    echo -e "   Swagger UI:   http://localhost:8001/api/docs"
    echo -e "   Chat API:     http://localhost:8001/chat"
    echo ""
    echo -e "${GREEN}🔐 Authentication:${NC}"
    echo -e "   API Key: fiss-c61197f847cc4682a91ada560bbd7119"
    echo -e "   Header: Authorization: Bearer <API_KEY>"
    echo ""
    echo -e "${GREEN}🛠️ Management Commands:${NC}"
    echo -e "   View logs:    docker-compose logs -f"
    echo -e "   Restart:      docker-compose restart"
    echo -e "   Stop:         docker-compose down"
    echo -e "   Rebuild:      docker-compose build --no-cache"
    echo ""
    echo -e "${BLUE}=======================================================================${NC}"
}

test_api() {
    echo -e "${YELLOW}🧪 Testing API...${NC}"

    # Test health endpoint
    if curl -f http://localhost:8001/health &> /dev/null; then
        echo -e "${GREEN}✅ Health check passed${NC}"
    else
        echo -e "${RED}❌ Health check failed${NC}"
        return 1
    fi

    # Test chat endpoint
    local response=$(curl -s -X POST http://localhost:8001/chat \
        -H "Authorization: Bearer fiss-c61197f847cc4682a91ada560bbd7119" \
        -H "Content-Type: application/json" \
        -d '{"message": "Hello, test local deployment"}')

    if [[ "$response" == *"error"* ]]; then
        echo -e "${RED}❌ Chat API test failed${NC}"
        echo "Response: $response"
        return 1
    else
        echo -e "${GREEN}✅ Chat API test passed${NC}"
    fi

    return 0
}

main() {
    print_header
    check_prerequisites
    setup_config
    deploy_local

    if wait_for_services; then
        if test_api; then
            show_info
            echo ""
            echo -e "${GREEN}🎉 READY TO DEPLOY TO SERVER!${NC}"
            echo -e "${YELLOW}Run: ./quick-deploy.sh your-domain.com admin@your-domain.com${NC}"
        else
            echo -e "${RED}❌ API tests failed. Check logs: docker-compose logs -f${NC}"
            exit 1
        fi
    else
        echo -e "${RED}❌ Services failed to start. Check logs: docker-compose logs -f${NC}"
        exit 1
    fi
}

# Run main function
main "$@"

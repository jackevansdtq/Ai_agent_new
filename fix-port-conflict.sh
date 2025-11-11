#!/bin/bash

# Fix Docker port conflict for Neo4J port 7474

echo "🔧 Fixing Docker port conflict..."

# Stop all running containers
echo "🛑 Stopping all containers..."
docker-compose down

# Remove orphaned containers
echo "🧹 Removing orphaned containers..."
docker container prune -f

# Change Neo4J port to avoid conflict
echo "🔄 Changing Neo4J port from 7474 to 7475..."
sed -i 's/NEO4J_PORT=.*/NEO4J_PORT=7475/' .env

# Update browser URL
echo "🔄 Updating Neo4J Browser URL..."
sed -i 's/NEO4J_BROWSER_URL=.*/NEO4J_BROWSER_URL=http:\/\/localhost:7475/' .env

echo "✅ Port conflict fixed!"
echo "📝 Neo4J Browser will be available at: http://localhost:7475"
echo ""
echo "🚀 Now run: docker-compose up -d"

#!/bin/bash

# Configure to use external Neo4J server instead of Docker container

echo "🔧 Configuring to use external Neo4J server..."

# Comment out neo4j service in docker-compose.yml
echo "📝 Commenting out Neo4J service in docker-compose.yml..."
sed -i 's/^  neo4j:/  # neo4j:/' docker-compose.yml
sed -i 's/^    image: neo4j:5.15/    # image: neo4j:5.15/' docker-compose.yml
sed -i 's/^    container_name: insurance-neo4j/    # container_name: insurance-neo4j/' docker-compose.yml
sed -i 's/^    environment:/    # environment:/' docker-compose.yml
sed -i 's/^      NEO4J_AUTH:.*/    #   NEO4J_AUTH: neo4j\/${NEO4J_PASSWORD:-password}/' docker-compose.yml
sed -i 's/^      NEO4J_PLUGINS:.*/    #   NEO4J_PLUGINS: '\''["graph-data-science"]'\''/' docker-compose.yml
sed -i 's/^      NEO4J_dbms_security_procedures_unrestricted:.*/    #   NEO4J_dbms_security_procedures_unrestricted: '\''gds.*'\''/' docker-compose.yml
sed -i 's/^      NEO4J_dbms_security_procedures_allowlist:.*/    #   NEO4J_dbms_security_procedures_allowlist: '\''gds.*,apoc.*'\''/' docker-compose.yml
sed -i 's/^    ports:/    # ports:/' docker-compose.yml
sed -i 's/^      - "\${NEO4J_PORT:-7474}:7474"/    #   - "\${NEO4J_PORT:-7474}:7474"/' docker-compose.yml
sed -i 's/^      - "\${NEO4J_BOLT_PORT:-7687}:7687"/    #   - "\${NEO4J_BOLT_PORT:-7687}:7687"/' docker-compose.yml
sed -i 's/^    volumes:/    # volumes:/' docker-compose.yml
sed -i 's/^      - neo4j_data:\/data/    #   - neo4j_data:\/data/' docker-compose.yml
sed -i 's/^      - neo4j_logs:\/logs/    #   - neo4j_logs:\/logs/' docker-compose.yml
sed -i 's/^      - \.\/neo4j-plugins:\/plugins/    #   - \.\/neo4j-plugins:\/plugins/' docker-compose.yml

# Remove neo4j dependency from insurance-bot service
echo "🔗 Removing Neo4J dependency from insurance-bot..."
sed -i '/neo4j:/d' docker-compose.yml
sed -i '/condition: service_healthy/d' docker-compose.yml

# Update .env with external Neo4J URI
echo "🌐 Updating Neo4J URI for external server..."
read -p "Enter your Neo4J server IP/hostname: " NEO4J_HOST
read -p "Enter Neo4J Bolt port (default 7687): " NEO4J_PORT_INPUT
NEO4J_PORT_INPUT=${NEO4J_PORT_INPUT:-7687}

sed -i "s|NEO4J_URI=.*|NEO4J_URI=neo4j://${NEO4J_HOST}:${NEO4J_PORT_INPUT}|" .env

echo "✅ Configuration updated!"
echo ""
echo "🔧 Please update these in .env with your server credentials:"
echo "   NEO4J_USERNAME=your_username"
echo "   NEO4J_PASSWORD=your_password"
echo ""
echo "🚀 Now run: docker-compose up -d"

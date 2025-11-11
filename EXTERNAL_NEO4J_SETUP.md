# 🔗 External Neo4J Setup Guide

## Cấu hình sử dụng Neo4J server riêng

### 1. Cập nhật .env với thông tin Neo4J server

```bash
# Edit file .env
nano .env

# Cập nhật các dòng sau với thông tin server của bạn:
NEO4J_URI=neo4j://your-neo4j-server-ip:7687
NEO4J_USERNAME=your_username
NEO4J_PASSWORD=your_password
```

### 2. Deploy với external Neo4J

```bash
# Quick deploy sẽ tự động sử dụng cấu hình external Neo4J
./quick-deploy.sh your-domain.com admin@your-domain.com

# Hoặc manual deploy
cp docker-compose-external.yml docker-compose.yml
docker-compose up -d
```

### 3. Kiểm tra kết nối

```bash
# Check API health
curl http://localhost:8001/health

# Check Neo4J connection trong logs
docker-compose logs -f insurance-bot
```

### 4. Test API

```bash
curl -X POST http://localhost:8001/chat \
  -H "Authorization: Bearer fiss-c61197f847cc4682a91ada560bbd7119" \
  -H "Content-Type: application/json" \
  -d '{"message": "Test external Neo4J connection"}'
```

## ⚠️ Lưu ý quan trọng

- **Port 7687** phải accessible từ Docker container
- **Username/Password** phải đúng với Neo4J server
- **Plugins** (graph-data-science, APOC) phải được cài trên Neo4J server của bạn
- **Database permissions** phải cho phép kết nối từ IP của server

## 🔧 Troubleshooting

### Connection failed
```bash
# Check Neo4J server is running
telnet your-neo4j-server 7687

# Check credentials
cypher-shell -a neo4j://your-neo4j-server:7687 -u your_username -p your_password
```

### Plugins missing
```bash
# Install plugins trên Neo4J server của bạn
# graph-data-science và APOC plugins required
```

### Permission denied
```bash
# Check firewall settings
# Allow port 7687 từ IP của server
```

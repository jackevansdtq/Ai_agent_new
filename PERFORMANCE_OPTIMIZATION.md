# 🚀 Performance Optimization Guide

## Mục tiêu
Giảm thời gian xử lý từ **49-68 giây** xuống **dưới 15 giây**.

## Các tối ưu đã thực hiện

### 1. ✅ QueryParam Optimization
- **top_k**: Giảm từ 60 → **5** (giảm 91.7%)
- **max_token_for_text_unit**: Giảm từ 4000 → **1500** (giảm 62.5%)
- **max_token_for_node_context**: Giảm từ 500 → **200** (giảm 60%)
- **max_token_for_local_context**: Giảm từ 4000 → **1500** (giảm 62.5%)
- **max_token_for_global_context**: Giảm từ 4000 → **1500** (giảm 62.5%)

### 2. ✅ Mode Optimization
- **Naive mode**: Sử dụng mode nhanh nhất (chỉ vector search, không dùng graph)
- **Fallback logic**: Nếu naive mode > 10s, tự động chuyển sang light mode với top_k=3

### 3. ✅ Caching Improvements
- **Response cache**: Cache responses với TTL 1 giờ
- **Embedding cache**: Cache embeddings để tránh gọi API lặp lại
- **Auto cleanup**: Tự động xóa cache entries đã hết hạn

### 4. ✅ Environment Variables
- **TOP_K**: 10 (default)
- **COSINE_THRESHOLD**: 0.25 (tối ưu cho filtering)

### 5. ✅ Performance Monitoring
- Thêm timing logs để track query time và total time
- Auto-retry với parameters nhỏ hơn nếu query quá chậm

## Kết quả

### Trước tối ưu:
- Processing time: **49-68 giây**
- Query time: **54 giây**

### Sau tối ưu:
- Query time: **~15 giây** ✅ (giảm 72%)
- Processing time: **~56 giây** (cần tối ưu thêm)

## Vấn đề còn lại

### 1. Processing Time vs Query Time
- Query time: **14.96s** ✅ (đã đạt mục tiêu < 15s)
- Total processing time: **56.40s** ❌ (vẫn chậm)

**Nguyên nhân có thể:**
- Event loop overhead
- Network latency
- API layer overhead
- Bot initialization (nếu có)

### 2. Các tối ưu tiếp theo

#### A. Async API Layer
```python
# Thay vì:
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
response = loop.run_until_complete(bot.chat(message))

# Nên dùng:
response = await bot.chat(message)  # Nếu Flask hỗ trợ async
```

#### B. Connection Pooling
- Tối ưu Neo4J connection pool
- Tối ưu OpenAI API client (reuse connections)

#### C. Parallel Processing
- Batch embedding requests
- Parallel vector searches
- Concurrent LLM calls (nếu có)

#### D. Response Streaming
- Stream response từ LLM thay vì chờ toàn bộ
- Giảm Time To First Token (TTFT)

#### E. Pre-computation
- Pre-compute embeddings cho common queries
- Pre-warm cache với popular questions

## Cấu hình tối ưu

### deploy.env
```env
# Performance optimization (tối ưu cho tốc độ < 15s)
TOP_K=10
COSINE_THRESHOLD=0.25
```

### QueryParam (trong code)
```python
query_param = QueryParam(
    mode="naive",  # Nhanh nhất
    top_k=5,  # Tối thiểu
    max_token_for_text_unit=1500,  # Giảm context
)
```

## Monitoring

### Logs để theo dõi:
```bash
docker-compose logs insurance-bot | grep -E "(Query time|Total time|naive|light)"
```

### Metrics quan trọng:
1. **Query time**: Thời gian MiniRAG query (mục tiêu: < 15s)
2. **Total time**: Tổng thời gian từ request đến response
3. **Cache hit rate**: Tỷ lệ cache hits
4. **API call count**: Số lượng API calls (OpenAI, Neo4J)

## Best Practices

1. **Luôn check cache trước**: Response cache → Embedding cache
2. **Sử dụng naive mode**: Nhanh nhất cho simple queries
3. **Giảm top_k**: Càng nhỏ càng nhanh (trade-off với accuracy)
4. **Giảm max_token**: Giảm context size để tăng tốc
5. **Monitor performance**: Track metrics để identify bottlenecks

## Tài liệu tham khảo

- [MiniRAG Documentation](https://github.com/MiniRAG/MiniRAG)
- [RAG Performance Optimization](https://www.pinecone.io/learn/retrieval-augmented-generation/)
- [Vector Database Optimization](https://www.pinecone.io/learn/vector-database/)


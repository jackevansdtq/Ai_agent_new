# 🚀 Advanced Performance Optimization Guide

## Mục tiêu
Giảm thời gian xử lý từ **30 giây** xuống **dưới 16 giây** bằng các kỹ thuật từ các công ty lớn.

## Các tối ưu đã implement

### 1. ✅ Singleton OpenAI Client (Connection Pooling)
- **Vấn đề**: Tạo client mới mỗi request → overhead connection setup
- **Giải pháp**: Singleton pattern để reuse connection
- **Lợi ích**: Giảm ~2-5s overhead mỗi request

```python
_openai_client: Optional[AsyncOpenAI] = None

def get_openai_client() -> AsyncOpenAI:
    global _openai_client
    if _openai_client is None:
        _openai_client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=30.0,  # Timeout ngắn hơn
            max_retries=2,  # Fail fast
        )
    return _openai_client
```

### 2. ✅ Event Loop Reuse
- **Vấn đề**: Tạo event loop mới mỗi request → overhead
- **Giải pháp**: Reuse global event loop
- **Lợi ích**: Giảm ~1-2s overhead

```python
_global_event_loop: Optional[asyncio.AbstractEventLoop] = None

def get_or_create_event_loop():
    global _global_event_loop
    if _global_event_loop is None or _global_event_loop.is_closed():
        _global_event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_global_event_loop)
    return _global_event_loop
```

### 3. ✅ Query Parameters Tối ưu
- **top_k**: 3 (giảm từ 5)
- **max_token_for_text_unit**: 1000 (giảm từ 1500)
- **llm_max_tokens**: 800 (giảm từ 1000)
- **Mode**: Naive (nhanh nhất)

### 4. ✅ Caching Strategy
- Response cache với TTL 1 giờ
- Embedding cache để tránh gọi API lặp lại
- Auto cleanup expired entries

## Các tối ưu tiếp theo (chưa implement)

### A. Response Streaming ⏳
**Mục tiêu**: Giảm Time To First Token (TTFT)

```python
# Thay vì chờ toàn bộ response:
answer = await self.rag.aquery(question, param=query_param)

# Stream response:
async for chunk in self.rag.aquery_stream(question, param=query_param):
    yield chunk  # Trả về ngay khi có token đầu tiên
```

**Lợi ích**: 
- User thấy response ngay (perceived latency giảm)
- TTFT: ~2-3s thay vì 15-30s

### B. Parallel Processing ⏳
**Mục tiêu**: Chạy song song các operations độc lập

```python
# Sequential (hiện tại):
embedding = await get_embedding(query)
results = await vector_search(embedding)
answer = await llm_generate(results)

# Parallel:
embedding_task = get_embedding(query)
# Trong khi chờ embedding, có thể pre-fetch common data
embedding = await embedding_task
results = await vector_search(embedding)
answer = await llm_generate(results)
```

**Lợi ích**: Giảm ~3-5s

### C. Pre-computation & Pre-warming ⏳
**Mục tiêu**: Pre-compute embeddings cho common queries

```python
# Pre-warm cache với popular questions
COMMON_QUERIES = [
    "Bảo hiểm xe máy là gì?",
    "Phí bảo hiểm xe máy bao nhiêu?",
    "Quy trình mua bảo hiểm xe máy?",
]

async def pre_warm_cache():
    for query in COMMON_QUERIES:
        await get_openai_embedding_func([query])
```

**Lợi ích**: Cache hit rate tăng → response time giảm

### D. Vector Database Optimization ⏳
**Mục tiêu**: Tối ưu vector search

1. **Index optimization**: Đảm bảo vector index được optimize
2. **Batch queries**: Batch multiple queries nếu có thể
3. **Approximate search**: Sử dụng approximate nearest neighbor (ANN) thay vì exact

### E. LLM Optimization ⏳
**Mục tiêu**: Tối ưu LLM generation

1. **Temperature**: Giảm temperature để generation nhanh hơn
2. **Stop sequences**: Thêm stop sequences để dừng sớm
3. **Streaming**: Stream tokens thay vì chờ toàn bộ

### F. Database Connection Pooling ⏳
**Mục tiêu**: Tối ưu Neo4J connections

```python
# Neo4J connection pool
neo4j_driver = GraphDatabase.driver(
    uri,
    auth=(username, password),
    max_connection_lifetime=3600,
    max_connection_pool_size=50,  # Tăng pool size
    connection_acquisition_timeout=5,
)
```

## Best Practices từ các công ty lớn

### 1. OpenAI ChatGPT
- **Streaming responses**: Luôn stream để giảm perceived latency
- **Connection pooling**: Reuse HTTP connections
- **Timeout management**: Fail fast với timeout ngắn
- **Retry logic**: Exponential backoff với max retries

### 2. Anthropic Claude
- **Pre-computation**: Pre-compute embeddings cho common queries
- **Caching**: Aggressive caching strategy
- **Parallel processing**: Parallelize independent operations

### 3. Google Bard/Gemini
- **Approximate search**: Sử dụng ANN cho vector search
- **Batch processing**: Batch multiple requests
- **Edge caching**: Cache ở edge locations

## Monitoring & Metrics

### Key Metrics:
1. **Query time**: Thời gian MiniRAG query (mục tiêu: < 10s)
2. **Total processing time**: Tổng thời gian từ request đến response (mục tiêu: < 16s)
3. **TTFT (Time To First Token)**: Thời gian đến token đầu tiên (mục tiêu: < 3s)
4. **Cache hit rate**: Tỷ lệ cache hits (mục tiêu: > 50%)
5. **API call count**: Số lượng API calls (mục tiêu: minimize)

### Logging:
```bash
# Monitor performance
docker-compose logs insurance-bot | grep -E "(Query time|Total time|Cache hit|API call)"

# Track bottlenecks
docker-compose logs insurance-bot | grep -E "(Fetching|HTTP Request|timeout)"
```

## Implementation Priority

### Phase 1 (Đã làm) ✅
1. Singleton OpenAI client
2. Event loop reuse
3. Query parameters optimization
4. Caching improvements

### Phase 2 (Ưu tiên cao) 🔥
1. Response streaming
2. Parallel processing
3. Pre-warming cache

### Phase 3 (Ưu tiên trung bình) 📋
1. Vector database optimization
2. LLM optimization
3. Database connection pooling

## Expected Results

### Current (sau Phase 1):
- Processing time: **~29s**
- Query time: **~15-20s**

### After Phase 2:
- Processing time: **~12-15s** ✅
- TTFT: **~2-3s** ✅
- Query time: **~8-10s**

### After Phase 3:
- Processing time: **~8-12s** ✅
- TTFT: **~1-2s** ✅
- Query time: **~5-8s**

## References

- [OpenAI Best Practices](https://platform.openai.com/docs/guides/production-best-practices)
- [RAG Optimization Guide](https://www.pinecone.io/learn/retrieval-augmented-generation/)
- [Vector Database Performance](https://www.pinecone.io/learn/vector-database/)
- [Async Python Best Practices](https://docs.python.org/3/library/asyncio-dev.html)


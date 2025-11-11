# 📖 Hướng dẫn Test API qua Swagger UI

## 🚀 Bước 1: Mở Swagger UI

1. Mở browser (Chrome, Firefox, Safari...)
2. Vào địa chỉ: **http://localhost:8001/api/docs**
3. Bạn sẽ thấy giao diện Swagger UI với danh sách các API endpoints

---

## 🔐 Bước 2: Xác thực API Key

### Cách 1: Dùng nút Authorize (Khuyên dùng)

1. **Tìm nút "Authorize"** ở góc trên bên phải màn hình (🔒 icon)
2. **Click vào nút "Authorize"**
3. **Nhập API Key:**
   ```
   fiss-c61197f847cc4682a91ada560bbd7119
   ```
4. **Click "Authorize"** → **Click "Close"**

✅ Bây giờ tất cả requests sẽ tự động có API key

### Cách 2: Nhập trực tiếp trong request

- Khi test endpoint, nhập API key vào header:
  ```
  Authorization: Bearer fiss-c61197f847cc4682a91ada560bbd7119
  ```

---

## 🧪 Bước 3: Test Health Check Endpoint

1. **Tìm endpoint:** `GET /health`
2. **Click vào endpoint** để mở rộng
3. **Click nút "Try it out"** (màu xanh)
4. **Click "Execute"** (màu xanh)
5. **Xem kết quả:**
   ```json
   {
     "status": "healthy",
     "bot_ready": true,
     "version": "1.0.0",
     "timestamp": 1234567890.123
   }
   ```

---

## 💬 Bước 4: Test Chat Endpoint

### 4.1. Mở Chat Endpoint

1. **Tìm endpoint:** `POST /chat`
2. **Click vào endpoint** để mở rộng
3. **Click nút "Try it out"**

### 4.2. Nhập Request Body

Trong phần **"Request body"**, nhập JSON:

```json
{
  "message": "Xin chào, tôi muốn hỏi về bảo hiểm"
}
```

**Hoặc test với câu hỏi khác:**
```json
{
  "message": "Bảo hiểm y tế có những loại nào?"
}
```

### 4.3. Execute Request

1. **Click nút "Execute"** (màu xanh)
2. **Đợi response** (có thể mất 2-5 giây)
3. **Xem kết quả** ở phần **"Responses"**

### 4.4. Xem Response

**Response thành công sẽ có dạng:**
```json
{
  "response": "Câu trả lời từ bot...",
  "status": "success",
  "timestamp": 1234567890.123
}
```

**Response lỗi (nếu thiếu API key):**
```json
{
  "error": {
    "message": "Missing API key...",
    "type": "authentication_error",
    "code": "missing_api_key"
  }
}
```

---

## 📝 Ví dụ Request Body

### Test 1: Câu hỏi đơn giản
```json
{
  "message": "Hello"
}
```

### Test 2: Câu hỏi về bảo hiểm
```json
{
  "message": "Bảo hiểm y tế có những quyền lợi gì?"
}
```

### Test 3: Câu hỏi phức tạp
```json
{
  "message": "Tôi muốn biết về quy trình đăng ký bảo hiểm xã hội"
}
```

---

## ⚠️ Lưu ý quan trọng

### Nếu gặp lỗi "401 Unauthorized":
- ✅ Kiểm tra đã nhập API key vào nút "Authorize" chưa
- ✅ API key phải đúng: `fiss-c61197f847cc4682a91ada560bbd7119`
- ✅ Format: `Bearer fiss-c61197f847cc4682a91ada560bbd7119`

### Nếu gặp lỗi "500 Internal Server Error":
- ✅ Check logs: `docker-compose logs insurance-bot`
- ✅ Kiểm tra Neo4J connection trong `.env`
- ✅ Kiểm tra OpenAI API key

### Nếu response chậm:
- ✅ Bình thường, API cần 2-5 giây để xử lý
- ✅ Lần đầu tiên có thể chậm hơn do load model

---

## 🎯 Quick Test với cURL

Nếu không muốn dùng Swagger UI, có thể test bằng terminal:

```bash
# Health check
curl http://localhost:8001/health

# Chat API
curl -X POST http://localhost:8001/chat \
  -H "Authorization: Bearer fiss-c61197f847cc4682a91ada560bbd7119" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, test API"}'
```

---

## 📸 Screenshot mô tả

**Swagger UI sẽ trông như thế này:**

```
┌─────────────────────────────────────────┐
│  Swagger UI                    [Authorize]│
├─────────────────────────────────────────┤
│                                         │
│  GET  /health                           │
│  POST /chat                             │
│                                         │
│  [POST /chat]                           │
│  ┌─────────────────────────────────┐   │
│  │ [Try it out]                    │   │
│  │                                 │   │
│  │ Request body:                   │   │
│  │ {                               │   │
│  │   "message": "Hello"            │   │
│  │ }                               │   │
│  │                                 │   │
│  │ [Execute]                       │   │
│  └─────────────────────────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```

---

## ✅ Checklist Test

- [ ] Mở được Swagger UI tại http://localhost:8001/api/docs
- [ ] Click "Authorize" và nhập API key thành công
- [ ] Test GET /health trả về status "healthy"
- [ ] Test POST /chat với message đơn giản
- [ ] Nhận được response từ bot
- [ ] Không có lỗi authentication

---

**🎉 Chúc bạn test thành công!**


# 🔧 Quick Fix: Set API Key trong Swagger UI

## ⚡ Cách nhanh nhất (1 lần duy nhất):

### Bước 1: Mở Swagger UI
Vào: http://localhost:8001/api/docs

### Bước 2: Mở Console (F12)
- Nhấn **F12** hoặc **Cmd+Option+I** (Mac) / **Ctrl+Shift+I** (Windows)
- Chọn tab **"Console"**

### Bước 3: Copy và paste script này vào Console:

```javascript
const apiKey = 'fiss-c61197f847cc4682a91ada560bbd7119';
if (window.ui && typeof window.ui.preauthorizeApiKey === 'function') {
    window.ui.preauthorizeApiKey('BearerAuth', apiKey);
    window.ui.preauthorizeApiKey('ApiKeyAuth', apiKey);
    console.log('✅ API Key đã được set:', apiKey);
} else {
    console.error('❌ Swagger UI chưa load. Refresh trang và thử lại.');
}
```

### Bước 4: Nhấn Enter
- Bạn sẽ thấy: `✅ API Key đã được set: fiss-c61197f847cc4682a91ada560bbd7119`
- **API key sẽ được lưu tự động** và không mất khi refresh!

---

## ✅ Kiểm tra API key đã được set:

1. Click nút **"Authorize"** (góc trên bên phải)
2. Bạn sẽ thấy API key đã có sẵn trong cả 2 options:
   - **BearerAuth**: `fiss-c61197f847cc4682a91ada560bbd7119`
   - **ApiKeyAuth**: `fiss-c61197f847cc4682a91ada560bbd7119`

---

## 🎯 Test ngay:

1. Click vào **POST /chat**
2. Click **"Try it out"**
3. Nhập message:
   ```json
   {
     "message": "Bảo hiểm xe máy là gì?"
   }
   ```
4. Click **"Execute"**
5. ✅ **Không còn lỗi 401!**

---

## 💡 Lưu ý:

- **Chỉ cần chạy script 1 lần** - API key sẽ được lưu trong localStorage
- **Refresh trang vẫn giữ API key** - Không cần nhập lại
- **Nếu mất API key** - Chạy lại script trên

---

## 🔄 Nếu vẫn không hoạt động:

1. **Clear localStorage:**
   ```javascript
   localStorage.clear();
   location.reload();
   ```

2. **Chạy lại script** (Bước 3 ở trên)

3. **Kiểm tra Console** có lỗi gì không

---

**🎉 Chúc bạn test thành công!**


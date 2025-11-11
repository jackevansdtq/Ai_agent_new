# 🔍 Debug Lỗi 401 - Hướng dẫn Chi tiết

## ✅ Xác nhận: Authentication hoạt động đúng

Đã test và xác nhận:
- ✅ Request **KHÔNG có headers**: 401 (đúng)
- ✅ Request **có Bearer token**: 200 (đúng)
- ✅ Request **có X-API-Key**: 200 (đúng)

**Vấn đề:** Swagger UI không gửi headers khi click "Execute"

---

## 🔍 Bước 1: Kiểm tra Headers trong Browser

### Mở Developer Tools:
1. Mở Swagger UI: http://localhost:8001/api/docs
2. Nhấn **F12** (hoặc Cmd+Option+I trên Mac)
3. Chọn tab **"Network"**

### Test Request:
1. Click vào **POST /chat**
2. Click **"Try it out"**
3. **QUAN TRỌNG:** Click nút **"Authorize"** (góc trên bên phải)
4. Nhập API key: `fiss-c61197f847cc4682a91ada560bbd7119`
5. Click **"Authorize"** → **"Close"**
6. Nhập message:
   ```json
   {
     "message": "test"
   }
   ```
7. Click **"Execute"**

### Kiểm tra Request trong Network tab:
1. Tìm request **POST /chat** trong danh sách
2. Click vào request đó
3. Chọn tab **"Headers"**
4. **Kiểm tra:**
   - Có header `Authorization: Bearer fiss-c61197f847cc4682a91ada560bbd7119` không?
   - HOẶC có header `X-API-Key: fiss-c61197f847cc4682a91ada560bbd7119` không?

**Nếu KHÔNG có headers → Đây là nguyên nhân!**

---

## 🔍 Bước 2: Xem Logs Server

Sau khi test, chạy lệnh này để xem logs:

```bash
cd /Volumes/data/MINIRAG
docker-compose logs insurance-bot | grep "DEBUG AUTH" | tail -20
```

**Bạn sẽ thấy:**
- Headers nào được gửi lên
- API key nào được extract
- Tại sao authentication fail

---

## 🔧 Fix Nếu Swagger UI Không Gửi Headers

### Cách 1: Thử lại với cả 2 security schemes

1. Click **"Authorize"**
2. **Nhập API key vào CẢ 2 options:**
   - **BearerAuth**: `fiss-c61197f847cc4682a91ada560bbd7119`
   - **ApiKeyAuth**: `fiss-c61197f847cc4682a91ada560bbd7119`
3. Click **"Authorize"** cho cả 2
4. Click **"Close"**
5. Test lại

### Cách 2: Check Console Logs

1. Mở **Console** tab (F12)
2. Test request
3. Xem có lỗi gì không
4. Xem có message `✅ API Key auto-set` không

### Cách 3: Clear và Set lại

1. Click **"Authorize"**
2. Click **"Logout"** cho cả 2 schemes
3. Click **"Close"**
4. Refresh trang (F5)
5. Click **"Authorize"** lại
6. Nhập API key vào cả 2
7. Test lại

---

## 📋 Checklist Debug

- [ ] Đã mở Network tab trong Developer Tools
- [ ] Đã click "Authorize" và nhập API key
- [ ] Đã check request POST /chat trong Network tab
- [ ] Đã check headers có Authorization hoặc X-API-Key không
- [ ] Đã xem logs server với `docker-compose logs insurance-bot | grep "DEBUG AUTH"`

---

## 🎯 Kết quả mong đợi

**Nếu headers được gửi đúng:**
- Request sẽ thành công (200)
- Logs sẽ hiển thị: `✅ AUTH SUCCESS - API key validated`

**Nếu headers KHÔNG được gửi:**
- Request sẽ fail (401)
- Logs sẽ hiển thị: `❌ AUTH FAILED - Missing both Authorization and X-API-Key headers`

---

**Hãy làm theo các bước trên và báo lại kết quả!**


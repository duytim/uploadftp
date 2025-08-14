# Ứng dụng Upload Báo Cáo qua FTP

Ứng dụng này là một công cụ web cho phép người dùng upload các file ảnh báo cáo lên máy chủ FTP, xem lịch sử file đã upload và kiểm tra trạng thái các báo cáo theo ngày. Ứng dụng được xây dựng với giao diện thân thiện, hỗ trợ kéo-thả file, và tích hợp chế độ sáng/tối.

## ✨ **Tính năng chính**

### **📤 Upload & Quản lý File**
- **Upload file ảnh**: Hỗ trợ upload tối đa 5 file ảnh (JPEG, PNG, GIF) lên máy chủ FTP với giới hạn kích thước 10MB mỗi file.
- **File Preview từ FTP**: Xem trước ảnh trực tiếp từ máy chủ FTP mà không cần tải về.
- **Quản lý tài khoản FTP**: Cho phép chọn các tài khoản FTP được cấu hình sẵn (BN_LTT, HN_NVL, HN_NVC).
- **Loại báo cáo**: Hỗ trợ nhiều loại báo cáo (Báo Cáo Biên Bản Đóng Mở Cửa, Báo Cáo Giao Ban, v.v.) và tùy chỉnh tên báo cáo.

### **🔍 Lịch sử & Kiểm tra**
- **Lịch sử file**: Xem danh sách các file đã upload theo ngày và tài khoản FTP.
- **Kiểm tra báo cáo**: Kiểm tra xem các loại báo cáo đã được upload lên FTP theo ngày cụ thể.

### **🎨 Giao diện & UX**
- **Giao diện responsive**: Tương thích với nhiều thiết bị (máy tính, tablet, điện thoại).
- **Chế độ sáng/tối**: Chuyển đổi giao diện sáng/tối để tăng trải nghiệm người dùng.
- **Drag & Drop cải tiến**: Hỗ trợ kéo thả file từ desktop với hiệu ứng trực quan.
- **Progress Bar real-time**: Hiển thị tiến trình upload chi tiết với animation đẹp mắt.
- **Keyboard Shortcuts**: Phím tắt để thao tác nhanh (Ctrl+U, Ctrl+D, Ctrl+H, Ctrl+K).
- **Auto-save**: Tự động lưu form khi đang nhập dở để tránh mất dữ liệu.

### **🔔 Thông báo & Feedback**
- **Toast Notifications**: Thông báo popup đẹp mắt khi upload hoàn tất hoặc có lỗi.
- **Success Indicators**: Hiển thị rõ ràng các file đã upload thành công.
- **Error Handling**: Xử lý lỗi chi tiết với thông báo rõ ràng.

### **🔒 Bảo mật**
- **Bảo mật thông tin FTP**: Sử dụng tệp `.env` để lưu trữ thông tin nhạy cảm (địa chỉ server, username, password).

## 🚀 **Tính năng mới trong phiên bản nâng cấp**

### **File Preview từ FTP**
- Xem trước ảnh trực tiếp từ máy chủ FTP
- Modal popup với thông tin chi tiết file
- Hỗ trợ tất cả định dạng ảnh (JPEG, PNG, GIF)

### **Progress Bar Real-time**
- Hiển thị tiến trình upload theo từng file
- Animation gradient đẹp mắt
- Thông tin chi tiết về file đang xử lý

### **Keyboard Shortcuts**
- **Ctrl+U**: Upload form
- **Ctrl+D**: Mở dialog chọn file
- **Ctrl+H**: Mở lịch sử
- **Ctrl+K**: Mở kiểm tra báo cáo

### **Auto-save Form**
- Tự động lưu dữ liệu form mỗi 2 giây
- Khôi phục dữ liệu khi refresh trang
- Indicator hiển thị trạng thái lưu

### **Drag & Drop cải tiến**
- Hiệu ứng visual khi kéo file
- Hiển thị số lượng file đang kéo
- Animation mượt mà

## 🛠️ **Công nghệ sử dụng**

- **Backend**: Flask (Python), ftplib
- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Icons**: Font Awesome 6.0
- **Quản lý biến môi trường**: python-dotenv
- **Giao diện**: CSS tùy chỉnh với hỗ trợ chế độ sáng/tối, hiệu ứng động và responsive
- **Hệ thống thời gian**: Sử dụng múi giờ Asia/Ho_Chi_Minh (UTC+7)

## 📁 **Cấu trúc thư mục**

```
project/
├── static/
│   ├── styles.css          # File CSS cho giao diện (đã nâng cấp)
│   └── script.js           # File JavaScript (đã nâng cấp)
├── templates/
│   └── index.html          # File HTML giao diện chính (đã nâng cấp)
├── .env                    # File lưu thông tin FTP (không đẩy lên git)
├── app.py                  # File Python chính chứa logic backend (đã nâng cấp)
├── README.md               # Tài liệu hướng dẫn (đã cập nhật)
└── .gitignore              # File cấu hình git ignore
```

## ⚙️ **Yêu cầu hệ thống**

- Python 3.8+
- pip (Python package manager)
- Truy cập vào máy chủ FTP với thông tin đăng nhập hợp lệ
- Trình duyệt web hiện đại hỗ trợ ES6+ và CSS Grid/Flexbox

## 📦 **Hướng dẫn cài đặt**

1. **Clone repository**:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Tạo môi trường ảo (khuyến nghị)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Cài đặt các thư viện cần thiết**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Tạo tệp `.env`**:
   - Tạo tệp `.env` trong thư mục gốc với nội dung sau:
     ```
     FTP_SERVER=<địa_chỉ_server_ftp>
     FTP_PASSWORD=<mật_khẩu_ftp>
     FTP_USERNAME_BN_LTT=<username_bn_ltt>
     FTP_USERNAME_HN_NVL=<username_hn_nvl>
     FTP_USERNAME_HN_NVC=<username_hn_nvc>
     ```
   - Thay thế `<địa_chỉ_server_ftp>`, `<mật_khẩu_ftp>`, `<username_...>` bằng thông tin thực tế của bạn.

5. **Cập nhật `.gitignore`**:
   - Thêm dòng sau vào tệp `.gitignore` để bảo vệ thông tin nhạy cảm:
     ```
     .env
     ```

6. **Chạy ứng dụng**:
   ```bash
   python app.py
   ```
   - Ứng dụng sẽ chạy tại `http://localhost:5000` (hoặc cổng được chỉ định trong biến môi trường `PORT`).

## 📖 **Hướng dẫn sử dụng**

### **1. Upload file**
- Chọn tài khoản FTP từ menu dropdown
- Chọn loại báo cáo hoặc nhập tên tùy chỉnh
- Tùy chọn: Chọn ngày upload hoặc sử dụng ngày hiện tại
- Kéo-thả hoặc chọn tối đa 5 file ảnh
- Nhấn **Upload** hoặc sử dụng **Ctrl+U**

### **2. Xem lịch sử**
- Nhấn **Lịch sử** hoặc sử dụng **Ctrl+H**
- Chọn tài khoản FTP và ngày
- Nhấn **Tìm kiếm** để xem danh sách file
- Nhấn **Xem trước** để xem ảnh trực tiếp từ FTP

### **3. Kiểm tra báo cáo**
- Nhấn **Kiểm tra** hoặc sử dụng **Ctrl+K**
- Chọn tài khoản FTP và ngày
- Nhấn **Kiểm tra** để xem trạng thái các loại báo cáo

### **4. Phím tắt**
- **Ctrl+U**: Upload form
- **Ctrl+D**: Mở dialog chọn file
- **Ctrl+H**: Mở lịch sử
- **Ctrl+K**: Mở kiểm tra báo cáo

### **5. Chuyển đổi giao diện**
- Nhấn nút hình mặt trăng/mặt trời ở góc phải trên để chuyển đổi giữa chế độ sáng và tối

## 🔧 **Tính năng kỹ thuật**

### **File Preview từ FTP**
- Sử dụng base64 encoding để hiển thị ảnh
- Hỗ trợ tất cả định dạng ảnh phổ biến
- Modal popup responsive

### **Progress Bar Real-time**
- Animation gradient với hiệu ứng shine
- Hiển thị thông tin chi tiết từng file
- Responsive design cho mobile

### **Auto-save**
- Debounced input handling (2 giây)
- LocalStorage để lưu trữ dữ liệu
- Khôi phục tự động khi refresh

### **Drag & Drop**
- Hỗ trợ multiple files
- Visual feedback khi kéo file
- Validation file type và size

## 🎨 **Giao diện**

- **Design System**: Sử dụng CSS Grid và Flexbox
- **Color Scheme**: Hỗ trợ light/dark mode
- **Typography**: Font system responsive
- **Animations**: CSS transitions và keyframes
- **Icons**: Font Awesome với fallback

## 📱 **Responsive Design**

- **Mobile First**: Thiết kế ưu tiên mobile
- **Breakpoints**: 480px, 768px, 1024px
- **Touch Friendly**: Buttons và controls tối ưu cho touch
- **Performance**: Lazy loading và optimization

## 🔒 **Bảo mật**

- Thông tin FTP được lưu trữ trong tệp `.env` và không được mã hóa cứng trong mã nguồn
- Đảm bảo tệp `.env` không được đẩy lên repository công khai
- Ứng dụng kiểm tra định dạng file, kích thước file, và số lượng file để đảm bảo an toàn khi upload
- Validation input và sanitization

## 🐛 **Xử lý lỗi**

- Nếu gặp lỗi kết nối FTP, kiểm tra thông tin trong tệp `.env` và đảm bảo máy chủ FTP đang hoạt động
- Nếu không thấy file trong lịch sử hoặc kiểm tra báo cáo, kiểm tra ngày và tài khoản FTP đã chọn
- Log được ghi lại với định dạng chi tiết để hỗ trợ debug (xem trong console hoặc tệp log)
- Error boundaries và fallback UI

## 🚀 **Performance**

- **Lazy Loading**: Chỉ tải ảnh khi cần thiết
- **Debouncing**: Tối ưu auto-save và input handling
- **Caching**: LocalStorage cho form data
- **Optimization**: CSS và JavaScript minification ready

## 🔮 **Roadmap**

### **Phiên bản tiếp theo**
- [ ] Hệ thống đăng nhập và phân quyền
- [ ] Compression ảnh tự động
- [ ] Batch operations
- [ ] REST API
- [ ] Mobile app

### **Tính năng nâng cao**
- [ ] Watermark tự động
- [ ] Scheduling upload
- [ ] Third-party integrations
- [ ] Advanced reporting

## 🤝 **Đóng góp**

- Nếu bạn muốn đóng góp, vui lòng tạo pull request hoặc mở issue trên repository
- Đảm bảo tuân thủ coding style (PEP 8 cho Python) và kiểm tra kỹ trước khi gửi
- Test trên nhiều trình duyệt và thiết bị

## 📄 **Giấy phép**

Dự án này được phát triển để sử dụng nội bộ và không đi kèm giấy phép công khai. Vui lòng liên hệ tác giả để biết thêm chi tiết.

## 📞 **Liên hệ**

Nếu có câu hỏi hoặc cần hỗ trợ, liên hệ qua email: [your-email@example.com] hoặc mở issue trên repository.

---

**Phiên bản**: 2.0.0  
**Cập nhật lần cuối**: Tháng 12, 2024  
**Trạng thái**: Stable với các tính năng nâng cấp mới

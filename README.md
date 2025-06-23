# Ứng dụng Upload Báo Cáo qua FTP

Ứng dụng này là một công cụ web cho phép người dùng upload các file ảnh báo cáo lên máy chủ FTP, xem lịch sử file đã upload và kiểm tra trạng thái các báo cáo theo ngày. Ứng dụng được xây dựng với giao diện thân thiện, hỗ trợ kéo-thả file, và tích hợp chế độ sáng/tối.

## Tính năng chính
- **Upload file ảnh**: Hỗ trợ upload tối đa 5 file ảnh (JPEG, PNG, GIF) lên máy chủ FTP với giới hạn kích thước 10MB mỗi file.
- **Quản lý tài khoản FTP**: Cho phép chọn các tài khoản FTP được cấu hình sẵn (BN_LTT, HN_NVL, HN_NVC).
- **Loại báo cáo**: Hỗ trợ nhiều loại báo cáo (Báo Cáo Biên Bản Đóng Mở Cửa, Báo Cáo Giao Ban, v.v.) và tùy chỉnh tên báo cáo.
- **Lịch sử file**: Xem danh sách các file đã upload theo ngày và tài khoản FTP.
- **Kiểm tra báo cáo**: Kiểm tra xem các loại báo cáo đã được upload lên FTP theo ngày cụ thể.
- **Giao diện responsive**: Tương thích với nhiều thiết bị (máy tính, tablet, điện thoại).
- **Chế độ sáng/tối**: Chuyển đổi giao diện sáng/tối để tăng trải nghiệm người dùng.
- **Bảo mật thông tin FTP**: Sử dụng tệp `.env` để lưu trữ thông tin nhạy cảm (địa chỉ server, username, password).

## Công nghệ sử dụng
- **Backend**: Flask (Python), ftplib
- **Frontend**: HTML, CSS, JavaScript
- **Quản lý biến môi trường**: python-dotenv
- **Giao diện**: CSS tùy chỉnh với hỗ trợ chế độ sáng/tối, hiệu ứng động và responsive
- **Hệ thống thời gian**: Sử dụng múi giờ Asia/Ho_Chi_Minh (UTC+7)

## Cấu trúc thư mục
```
project/
├── static/
│   └── styles.css       # File CSS cho giao diện
├── templates/
│   └── index.html       # File HTML giao diện chính
├── .env                 # File lưu thông tin FTP (không đẩy lên git)
├── app.py               # File Python chính chứa logic backend
├── README.md            # Tài liệu hướng dẫn
└── .gitignore           # File cấu hình git ignore
```

## Yêu cầu hệ thống
- Python 3.8+
- pip (Python package manager)
- Truy cập vào máy chủ FTP với thông tin đăng nhập hợp lệ

## Hướng dẫn cài đặt
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
   pip install flask python-dotenv
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
   - Ví dụ:
     ```
     FTP_SERVER=123.30.3.61
     FTP_PASSWORD=ksqtvhc
     FTP_USERNAME_BN_LTT=ksqtbacninh
     FTP_USERNAME_HN_NVL=ksqtsaidong
     FTP_USERNAME_HN_NVC=ksqtlongbien
     ```

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

## Hướng dẫn sử dụng
1. **Truy cập ứng dụng**:
   - Mở trình duyệt và truy cập `http://localhost:5000`.
2. **Upload file**:
   - Chọn tài khoản FTP từ menu dropdown.
   - Chọn loại báo cáo hoặc nhập tên tùy chỉnh (nếu chọn "Bổ Sung Báo Cáo Khác").
   - Tùy chọn: Chọn ngày upload hoặc sử dụng ngày hiện tại.
   - Kéo-thả hoặc chọn tối đa 5 file ảnh (JPEG, PNG, GIF).
   - Nhấn nút **Upload** để tải file lên FTP.
3. **Xem lịch sử**:
   - Nhấn nút **Lịch sử**, chọn tài khoản FTP và ngày, sau đó nhấn **Tìm kiếm** để xem danh sách file đã upload.
4. **Kiểm tra báo cáo**:
   - Nhấn nút **Kiểm tra**, chọn tài khoản FTP và ngày, sau đó nhấn **Kiểm tra** để xem trạng thái các loại báo cáo.
5. **Chuyển đổi giao diện**:
   - Nhấn nút hình mặt trăng/mặt trời ở góc phải trên để chuyển đổi giữa chế độ sáng và tối.

## Bảo mật
- Thông tin FTP (server, username, password) được lưu trữ trong tệp `.env` và không được mã hóa cứng trong mã nguồn.
- Đảm bảo tệp `.env` không được đẩy lên repository công khai.
- Ứng dụng kiểm tra định dạng file, kích thước file, và số lượng file để đảm bảo an toàn khi upload.

## Xử lý lỗi
- Nếu gặp lỗi kết nối FTP, kiểm tra thông tin trong tệp `.env` và đảm bảo máy chủ FTP đang hoạt động.
- Nếu không thấy file trong lịch sử hoặc kiểm tra báo cáo, kiểm tra ngày và tài khoản FTP đã chọn.
- Log được ghi lại với định dạng chi tiết để hỗ trợ debug (xem trong console hoặc tệp log).

## Đóng góp
- Nếu bạn muốn đóng góp, vui lòng tạo pull request hoặc mở issue trên repository.
- Đảm bảo tuân thủ coding style (PEP 8 cho Python) và kiểm tra kỹ trước khi gửi.

## Giấy phép
Dự án này được phát triển để sử dụng nội bộ và không đi kèm giấy phép công khai. Vui lòng liên hệ tác giả để biết thêm chi tiết.

## Liên hệ
Nếu có câu hỏi hoặc cần hỗ trợ, liên hệ qua email: [your-email@example.com] hoặc mở issue trên repository.

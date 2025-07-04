from flask import Flask, request, render_template, jsonify
import ftplib
import os
from datetime import datetime
import logging
import pytz
from dotenv import load_dotenv

app = Flask(__name__)

# Tải biến môi trường từ tệp .env
load_dotenv()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Lấy thông tin FTP từ biến môi trường
FTP_SERVER = os.getenv('FTP_SERVER')
FTP_PASSWORD = os.getenv('FTP_PASSWORD')

FTP_ACCOUNTS = {
    '1': {
        'server': FTP_SERVER,
        'username': os.getenv('FTP_USERNAME_BN_LTT'),
        'password': FTP_PASSWORD,
        'description': 'BN_LTT - Bắc Ninh'
    },
    '2': {
        'server': FTP_SERVER,
        'username': os.getenv('FTP_USERNAME_HN_NVL'),
        'password': FTP_PASSWORD,
        'description': 'HN_NVL - Sài Đồng'
    },
    '3': {
        'server': FTP_SERVER,
        'username': os.getenv('FTP_USERNAME_HN_NVC'),
        'password': FTP_PASSWORD,
        'description': 'HN_NVC - Long Biên'
    }
}

ALLOWED_TYPES = {'image/jpeg', 'image/png', 'image/gif'}
MAX_FILE_SIZE = 10 * 1024 * 1024
MAX_FILES = 10
TIMEZONE = pytz.timezone('Asia/Ho_Chi_Minh')

@app.route('/')
def index():
    logger.debug("Serving index page")
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    ftp_conn = None
    try:
        logger.debug("Upload request received")
        ftp_account_id = request.form.get('ftpAccount')
        if not ftp_account_id or ftp_account_id not in FTP_ACCOUNTS:
            logger.error(f"Invalid FTP account: {ftp_account_id}")
            return jsonify({'success': False, 'message': 'Tài khoản FTP không hợp lệ!'}), 400

        ftp = FTP_ACCOUNTS[ftp_account_id]
        files = request.files.getlist('images[]')
        if not files or len(files) > MAX_FILES:
            logger.error(f"Invalid file count: {len(files)}")
            return jsonify({'success': False, 'message': f'Vui lòng chọn tối đa {MAX_FILES} ảnh!'}), 400

        report_type = request.form.get('reportType')
        custom_name = request.form.get('customName', '').strip()
        custom_date = request.form.get('customDate')
        if not report_type:
            logger.error("Missing report type")
            return jsonify({'success': False, 'message': 'Vui lòng chọn loại báo cáo!'}), 400
        if report_type == 'Custom' and not custom_name:
            logger.error("Missing custom name for Custom report")
            return jsonify({'success': False, 'message': 'Vui lòng nhập tên file cho báo cáo tùy chỉnh!'}), 400
        if custom_date:
            try:
                selected_date = datetime.strptime(custom_date, '%Y-%m-%d')
                date = selected_date.strftime('%d.%m.%y')
            except ValueError:
                logger.error("Invalid custom date format")
                return jsonify({'success': False, 'message': 'Định dạng ngày không hợp lệ!'}), 400
        else:
            date = datetime.now(TIMEZONE).strftime('%d.%m.%y')

        logger.debug(f"Connecting to FTP: {ftp['server']}")
        ftp_conn = ftplib.FTP()
        ftp_conn.connect(ftp['server'], timeout=60)
        ftp_conn.login(ftp['username'], ftp['password'])
        ftp_conn.set_pasv(True)

        ftp_directory = f"/KSQT/{date}/"
        logger.debug(f"Checking FTP directory: {ftp_directory}")
        try:
            ftp_conn.cwd(ftp_directory)
        except ftplib.all_errors:
            logger.debug(f"Creating FTP directory: {ftp_directory}")
            ftp_conn.mkd(ftp_directory)
            ftp_conn.cwd(ftp_directory)

        existing_files = set()
        try:
            existing_files = set(ftp_conn.nlst() or [])
            existing_files = {f.lower() for f in existing_files}
        except ftplib.all_errors as e:
            logger.warning(f"Failed to list files: {str(e)}")
        logger.debug(f"Existing files: {existing_files}")

        uploaded_files = []
        for i, file in enumerate(files[:MAX_FILES]):
            logger.debug(f"Processing file: {file.filename}")
            if file.mimetype not in ALLOWED_TYPES:
                logger.warning(f"Invalid file type: {file.mimetype}")
                continue
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)
            if file_size > MAX_FILE_SIZE:
                logger.warning(f"File too large: {file.filename}, size: {file_size}")
                continue

            extension = os.path.splitext(file.filename)[1].lower()
            file_prefix = report_type if report_type != 'Custom' else custom_name
            file_name = f"{date}-{file_prefix}{extension}" if len(files) == 1 else f"{date}-{file_prefix}-{i+1}{extension}"
            remote_file = file_name

            counter = 1
            base_name = f"{date}-{file_prefix}"
            while remote_file.lower() in existing_files:
                remote_file = f"{base_name}-{counter}{extension}"
                counter += 1

            logger.debug(f"Uploading to: {ftp_directory}{remote_file}")
            ftp_conn.storbinary(f'STOR {remote_file}', file.stream)
            uploaded_files.append(remote_file)
            existing_files.add(remote_file.lower())

        if not uploaded_files:
            logger.warning("No files uploaded")
            return jsonify({'success': False, 'message': 'Không có file nào được upload thành công'}), 400

        logger.info(f"Uploaded files: {uploaded_files}")
        return jsonify({
            'success': True,
            'message': f"Đã upload thành công {len(uploaded_files)} file lên {ftp['description']}: {', '.join(uploaded_files)}",
            'files': uploaded_files
        })

    except ftplib.all_errors as e:
        logger.error(f"FTP error: {str(e)}")
        return jsonify({'success': False, 'message': f'Lỗi FTP: {str(e)}'}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'success': False, 'message': f'Lỗi không xác định: {str(e)}'}), 500
    finally:
        if ftp_conn:
            try:
                ftp_conn.quit()
                logger.debug("FTP connection closed")
            except:
                pass

@app.route('/list_files_by_date', methods=['POST'])
def list_files_by_date():
    ftp_conn = None
    try:
        ftp_account_id = request.form.get('ftpAccount')
        date = request.form.get('date')
        if not ftp_account_id or ftp_account_id not in FTP_ACCOUNTS:
            return jsonify({'success': False, 'message': 'Tài khoản FTP không hợp lệ!'}), 400
        if not date:
            return jsonify({'success': False, 'message': 'Vui lòng chọn ngày!'}), 400

        ftp = FTP_ACCOUNTS[ftp_account_id]
        ftp_conn = ftplib.FTP()
        ftp_conn.connect(ftp['server'], timeout=60)
        ftp_conn.login(ftp['username'], ftp['password'])
        ftp_conn.set_pasv(True)

        try:
            selected_date = datetime.strptime(date, '%Y-%m-%d')
            ftp_date = selected_date.strftime('%d.%m.%y')
        except ValueError:
            return jsonify({'success': False, 'message': 'Định dạng ngày không hợp lệ!'}), 400

        ftp_directory = f"/KSQT/{ftp_date}/"
        logger.debug(f"Checking FTP directory: {ftp_directory}")
        try:
            ftp_conn.cwd(ftp_directory)
        except ftplib.all_errors:
            return jsonify({'success': False, 'message': f'Thư mục cho ngày {ftp_date} không tồn tại!'}), 404

        files = ftp_conn.nlst() or []
        if not files:
            return jsonify({'success': False, 'message': f'Thư mục cho ngày {ftp_date} trống!'}), 200

        return jsonify({'success': True, 'files': files})
    except ftplib.all_errors as e:
        logger.error(f"FTP error: {str(e)}")
        return jsonify({'success': False, 'message': f'Lỗi kết nối FTP: {str(e)}'}), 500
    finally:
        if ftp_conn:
            try:
                ftp_conn.quit()
                logger.debug("FTP connection closed")
            except:
                pass

@app.route('/check_reports', methods=['POST'])
def check_reports():
    ftp_conn = None
    try:
        ftp_account_id = request.form.get('ftpAccount')
        date = request.form.get('date')
        if not ftp_account_id or ftp_account_id not in FTP_ACCOUNTS:
            return jsonify({'success': False, 'message': 'Tài khoản FTP không hợp lệ!'}), 400
        if not date:
            return jsonify({'success': False, 'message': 'Vui lòng chọn ngày!'}), 400

        ftp = FTP_ACCOUNTS[ftp_account_id]
        ftp_conn = ftplib.FTP()
        ftp_conn.connect(ftp['server'], timeout=60)
        ftp_conn.login(ftp['username'], ftp['password'])
        ftp_conn.set_pasv(True)

        try:
            selected_date = datetime.strptime(date, '%Y-%m-%d')
            ftp_date = selected_date.strftime('%d.%m.%y')
        except ValueError:
            return jsonify({'success': False, 'message': 'Định dạng ngày không hợp lệ!'}), 400

        ftp_directory = f"/KSQT/{ftp_date}/"
        logger.debug(f"Checking FTP directory: {ftp_directory}")
        try:
            ftp_conn.cwd(ftp_directory)
        except ftplib.all_errors:
            return jsonify({'success': False, 'message': f'Thư mục cho ngày {ftp_date} không tồn tại!'}), 404

        files = ftp_conn.nlst() or []
        files_lower = [f.lower() for f in files]
        report_types = ['BCDongMoCua', 'BaoCaoGiaoBan', 'ThayDoiGia', 'BatTatMatTien', 'BCDaoTao']
        reports_status = {}
        for report in report_types:
            reports_status[report] = any(report.lower() in f for f in files_lower)

        return jsonify({
            'success': True,
            'reports': reports_status
        })
    except ftplib.all_errors as e:
        logger.error(f"FTP error: {str(e)}")
        return jsonify({'success': False, 'message': f'Lỗi kết nối FTP: {str(e)}'}), 500
    finally:
        if ftp_conn:
            try:
                ftp_conn.quit()
                logger.debug("FTP connection closed")
            except:
                pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
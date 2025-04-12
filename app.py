from flask import Flask, request, render_template, jsonify
import ftplib
import os
from datetime import datetime
import logging

app = Flask(__name__)

# Thiết lập logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

FTP_ACCOUNTS = {
    '1': {'server': '123.30.3.61', 'username': 'ksqtbacninh', 'password': 'ksqtvhc', 'description': 'BN_LTT - Bắc Ninh'},
    '2': {'server': '123.30.3.61', 'username': 'ksqtsaidong', 'password': 'ksqtvhc', 'description': 'HN_NVL - Sài Đồng'},
    '3': {'server': '123.30.3.61', 'username': 'ksqtlongbien', 'password': 'ksqtvhc', 'description': 'HN_NVC - Long Biên'}
}

ALLOWED_TYPES = {'image/jpeg', 'image/png', 'image/gif'}
MAX_FILE_SIZE = 3 * 1024 * 1024  # Giảm xuống 3MB để tiết kiệm RAM
MAX_FILES = 3

@app.route('/')
def index():
    logger.debug("Serving index page")
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    ftp_conn = None
    try:
        logger.debug("Upload request received")
        # Trích xuất dữ liệu trong context chính
        ftp_account_id = request.form.get('ftpAccount')
        if not ftp_account_id or ftp_account_id not in FTP_ACCOUNTS:
            logger.error(f"Invalid FTP account: {ftp_account_id}")
            return jsonify({'success': False, 'message': 'Tài khoản FTP không hợp lệ!'})

        ftp = FTP_ACCOUNTS[ftp_account_id]
        files = request.files.getlist('images[]')
        if not files or len(files) > MAX_FILES:
            logger.error(f"Invalid file count: {len(files)}")
            return jsonify({'success': False, 'message': f'Vui lòng chọn tối đa {MAX_FILES} ảnh!'})

        report_type = request.form.get('reportType')
        custom_name = request.form.get('customName', '')

        logger.debug(f"Connecting to FTP: {ftp['server']}")
        ftp_conn = ftplib.FTP()
        ftp_conn.connect(ftp['server'], timeout=30)
        ftp_conn.login(ftp['username'], ftp['password'])
        ftp_conn.set_pasv(True)

        date = datetime.now().strftime('%d.%m.%y')
        ftp_directory = f"/KSQT/{date}/"
        logger.debug(f"Checking FTP directory: {ftp_directory}")
        try:
            ftp_conn.cwd(ftp_directory)
        except ftplib.all_errors:
            logger.debug(f"Creating FTP directory: {ftp_directory}")
            ftp_conn.mkd(ftp_directory)
            ftp_conn.cwd('/')

        existing_files = set(ftp_conn.nlst(ftp_directory) or [])
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

            original_name = os.path.splitext(file.filename)[0]
            extension = os.path.splitext(file.filename)[1].lower()
            file_prefix = sanitize_file_name(custom_name if report_type == 'Custom' and custom_name else report_type)
            file_name = f"{date}-{file_prefix}-{i+1}{extension}" if len(files) > 1 else f"{date}-{file_prefix}{extension}"
            remote_file = f"{ftp_directory}{file_name}"

            counter = 1
            while remote_file in existing_files:
                remote_file = f"{ftp_directory}{sanitize_file_name(original_name)}-{counter}{extension}"
                counter += 1

            logger.debug(f"Uploading to: {remote_file}")
            ftp_conn.storbinary(f'STOR {remote_file}', file.stream)
            uploaded_files.append(file_name)
            existing_files.add(remote_file)

        if not uploaded_files:
            logger.warning("No files uploaded")
            return jsonify({'success': False, 'message': 'Không có file nào được upload thành công'})

        logger.info(f"Uploaded files: {uploaded_files}")
        return jsonify({
            'success': True,
            'message': f"Đã upload thành công {len(uploaded_files)} file lên {ftp['description']}: {', '.join(uploaded_files)}",
            'files': uploaded_files
        })

    except ftplib.all_errors as e:
        logger.error(f"FTP error: {str(e)}")
        return jsonify({'success': False, 'message': f'Lỗi FTP: {str(e)}'})
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'success': False, 'message': f'Lỗi không xác định: {str(e)}'})
    finally:
        if ftp_conn:
            try:
                ftp_conn.quit()
                logger.debug("FTP connection closed")
            except:
                pass

def sanitize_file_name(name):
    """Sanitize file name to match client-side logic"""
    return name.lower().replace('[^a-z0-9-_]', '').strip()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

from flask import Flask, request, Response, render_template
import ftplib
import os
from datetime import datetime
import json

app = Flask(__name__)

FTP_ACCOUNTS = {
    '1': {'server': '123.30.3.61', 'username': 'ksqtbacninh', 'password': 'ksqtvhc', 'description': 'BN_LTT - Bắc Ninh'},
    '2': {'server': '123.30.3.61', 'username': 'ksqtsaidong', 'password': 'ksqtvhc', 'description': 'HN_NVL - Sài Đồng'},
    '3': {'server': '123.30.3.61', 'username': 'ksqtlongbien', 'password': 'ksqtvhc', 'description': 'HN_NVC - Long Biên'}
}

ALLOWED_TYPES = {'image/jpeg', 'image/png', 'image/gif'}
MAX_FILE_SIZE = 5 * 1024 * 1024
MAX_FILES = 3

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    def generate():
        try:
            ftp_account_id = request.form.get('ftpAccount')
            if not ftp_account_id or ftp_account_id not in FTP_ACCOUNTS:
                yield json.dumps({'success': False, 'message': 'Tài khoản FTP không hợp lệ!'}) + '\n'
                return

            ftp = FTP_ACCOUNTS[ftp_account_id]
            files = request.files.getlist('images[]')
            if not files or len(files) > MAX_FILES:
                yield json.dumps({'success': False, 'message': f'Vui lòng chọn tối đa {MAX_FILES} ảnh!'}) + '\n'
                return

            ftp_conn = ftplib.FTP(ftp['server'], ftp['username'], ftp['password'], timeout=10)
            ftp_conn.set_pasv(True)

            date = datetime.now().strftime('%d.%m.%y')
            ftp_directory = f"/KSQT/{date}/"
            try:
                ftp_conn.cwd(ftp_directory)
            except:
                ftp_conn.mkd(ftp_directory)
                ftp_conn.cwd('/')

            existing_files = set(ftp_conn.nlst(ftp_directory))

            uploaded_files = []
            for i, file in enumerate(files[:MAX_FILES]):
                if file.mimetype not in ALLOWED_TYPES or file.content_length > MAX_FILE_SIZE:
                    continue

                original_name = os.path.splitext(file.filename)[0]
                extension = os.path.splitext(file.filename)[1].lower()
                report_type = request.form.get('reportType')
                custom_name = request.form.get('customName', '')
                file_prefix = custom_name if report_type == 'Custom' and custom_name else report_type
                file_name = f"{date}-{file_prefix}-{i+1}{extension}" if len(files) > 1 else f"{date}-{file_prefix}{extension}"
                remote_file = f"{ftp_directory}{file_name}"

                counter = 1
                while remote_file in existing_files:
                    remote_file = f"{ftp_directory}{original_name}-{counter}{extension}"
                    counter += 1

                ftp_conn.storbinary(f'STOR {remote_file}', file.stream)
                uploaded_files.append(file_name)
                existing_files.add(remote_file)
                yield json.dumps({'fileProgress': file_name}) + '\n'

            ftp_conn.quit()

            if not uploaded_files:
                yield json.dumps({'success': False, 'message': 'Không có file nào được upload thành công'}) + '\n'
            else:
                yield json.dumps({
                    'success': True,
                    'message': f"Đã upload thành công {len(uploaded_files)} file lên {ftp['description']}: {', '.join(uploaded_files)}"
                }) + '\n'

        except Exception as e:
            yield json.dumps({'success': False, 'message': f'Lỗi: {str(e)}'}) + '\n'

    return Response(generate(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
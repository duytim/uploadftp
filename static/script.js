document.addEventListener('DOMContentLoaded', () => {
    // Kiểm tra và áp dụng dark mode dựa trên prefers-color-scheme
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.body.classList.add('dark-mode');
    }

    // Lấy các phần tử DOM
    const uploadForm = document.getElementById('uploadForm');
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const previewContainer = document.getElementById('previewContainer');
    const uploadButton = document.getElementById('uploadButton');
    const reportType = document.getElementById('reportType');
    const customName = document.getElementById('customName');
    const checkButton = document.getElementById('checkButton');
    const historyButton = document.getElementById('historyButton');
    const themeToggle = document.getElementById('themeToggle');
    const checkFtpAccount = document.getElementById('checkFtpAccount');
    const checkDate = document.getElementById('checkDate');
    const checkTableContainer = document.getElementById('checkTableContainer');
    const historyFtpAccount = document.getElementById('historyFtpAccount');
    const historyDate = document.getElementById('historyDate');
    const historyTableContainer = document.getElementById('historyTableContainer');

    // Xử lý kéo thả file
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        const files = e.dataTransfer.files;
        fileInput.files = files;
        displayPreviews(files);
    });

    dropZone.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', () => displayPreviews(fileInput.files));

    // Hiển thị xem trước ảnh
    function displayPreviews(files) {
        previewContainer.innerHTML = '';
        uploadButton.disabled = files.length === 0;
        Array.from(files).forEach((file, index) => {
            if (!file.type.match('image.*')) return;
            const reader = new FileReader();
            reader.onload = (e) => {
                const preview = document.createElement('div');
                preview.className = 'preview';
                preview.innerHTML = `
                    <img src="${e.target.result}" alt="Xem trước ảnh ${index + 1}">
                    <span class="remove-preview" data-index="${index}">&times;</span>
                `;
                previewContainer.appendChild(preview);
            };
            reader.readAsDataURL(file);
        });
    }

    // Xóa ảnh xem trước
    previewContainer.addEventListener('click', (e) => {
        if (e.target.classList.contains('remove-preview')) {
            const index = e.target.dataset.index;
            const dt = new DataTransfer();
            Array.from(fileInput.files).forEach((file, i) => {
                if (i != index) dt.items.add(file);
            });
            fileInput.files = dt.files;
            displayPreviews(fileInput.files);
        }
    });

    // Hiển thị input tên tùy chỉnh khi chọn báo cáo Custom
    reportType.addEventListener('change', () => {
        customName.style.display = reportType.value === 'Custom' ? 'block' : 'none';
    });

    // Gửi form upload
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(uploadForm);
        uploadButton.disabled = true;
        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            if (data.success) {
                showPopup('successPopup', data.message);
                uploadForm.reset();
                previewContainer.innerHTML = '';
                uploadButton.disabled = true;
                customName.style.display = 'none';
            } else {
                showPopup('errorPopup', data.message);
            }
        } catch (error) {
            showPopup('errorPopup', 'Lỗi kết nối server!');
        } finally {
            uploadButton.disabled = false;
        }
    });

    // Xử lý nút kiểm tra báo cáo
    checkButton.addEventListener('click', () => {
        showPopup('checkPopup');
        checkTableContainer.classList.remove('loading');
        checkTableContainer.querySelector('tbody').innerHTML = '';
    });

    // Xử lý kiểm tra báo cáo
    checkFtpAccount.addEventListener('change', fetchCheckReports);
    checkDate.addEventListener('change', fetchCheckReports);

    async function fetchCheckReports() {
        if (!checkFtpAccount.value || !checkDate.value) return;
        checkTableContainer.classList.add('loading');
        try {
            const formData = new FormData();
            formData.append('ftpAccount', checkFtpAccount.value);
            formData.append('date', checkDate.value);
            const response = await fetch('/check_reports', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            checkTableContainer.classList.remove('loading');
            if (data.success) {
                const tbody = checkTableContainer.querySelector('tbody');
                tbody.innerHTML = '';
                for (const [report, status] of Object.entries(data.reports)) {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${report}</td>
                        <td>${status ? 'Có' : 'Không'}</td>
                    `;
                    tbody.appendChild(tr);
                }
            } else {
                showPopup('errorPopup', data.message);
            }
        } catch (error) {
            checkTableContainer.classList.remove('loading');
            showPopup('errorPopup', 'Lỗi kết nối server!');
        }
    }

    // Xử lý nút xem lịch sử
    historyButton.addEventListener('click', () => {
        showPopup('historyPopup');
        historyTableContainer.classList.remove('loading');
        historyTableContainer.querySelector('tbody').innerHTML = '';
    });

    // Xử lý xem lịch sử
    historyFtpAccount.addEventListener('change', fetchHistory);
    historyDate.addEventListener('change', fetchHistory);

    async function fetchHistory() {
        if (!historyFtpAccount.value || !historyDate.value) return;
        historyTableContainer.classList.add('loading');
        try {
            const formData = new FormData();
            formData.append('ftpAccount', historyFtpAccount.value);
            formData.append('date', historyDate.value);
            const response = await fetch('/list_files_by_date', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            historyTableContainer.classList.remove('loading');
            if (data.success) {
                const tbody = historyTableContainer.querySelector('tbody');
                tbody.innerHTML = '';
                data.files.forEach(file => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${file}</td>
                        <td><a href="#" class="action-preview">Xem</a></td>
                    `;
                    tbody.appendChild(tr);
                });
            } else {
                showPopup('errorPopup', data.message);
            }
        } catch (error) {
            historyTableContainer.classList.remove('loading');
            showPopup('errorPopup', 'Lỗi kết nối server!');
        }
    }

    // Chuyển đổi giao diện sáng/tối
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
    });

    // Hiển thị popup
    function showPopup(popupId, message) {
        const popup = document.getElementById(popupId);
        if (message) {
            popup.querySelector('p').textContent = message;
        }
        popup.classList.add('active');
    }

    // Đóng popup
    window.closePopup = (popupId) => {
        document.getElementById(popupId).classList.remove('active');
    };
});

class MonReader {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8000';
        this.currentFile = null;
        this.initializeElements();
        this.attachEventListeners();
    }

    initializeElements() {
        this.uploadArea = document.getElementById('uploadArea');
        this.fileInput = document.getElementById('fileInput');
        this.fileInfo = document.getElementById('fileInfo');
        this.imagePreview = document.getElementById('imagePreview');
        this.fileName = document.getElementById('fileName');
        this.fileSize = document.getElementById('fileSize');
        this.processBtn = document.getElementById('processBtn');
        this.loadingSection = document.getElementById('loadingSection');
        this.resultsSection = document.getElementById('resultsSection');
        this.extractedText = document.getElementById('extractedText');
        this.audioPlayer = document.getElementById('audioPlayer');
        this.copyTextBtn = document.getElementById('copyTextBtn');
        this.downloadAudioBtn = document.getElementById('downloadAudioBtn');
        this.newImageBtn = document.getElementById('newImageBtn');
        this.errorSection = document.getElementById('errorSection');
        this.errorMessage = document.getElementById('errorMessage');
        this.retryBtn = document.getElementById('retryBtn');
    }

    attachEventListeners() {
        // Upload area events
        this.uploadArea.addEventListener('click', () => this.fileInput.click());
        this.uploadArea.addEventListener('dragover', this.handleDragOver.bind(this));
        this.uploadArea.addEventListener('dragleave', this.handleDragLeave.bind(this));
        this.uploadArea.addEventListener('drop', this.handleDrop.bind(this));

        // File input change
        this.fileInput.addEventListener('change', this.handleFileSelect.bind(this));

        // Button events
        this.processBtn.addEventListener('click', this.processImage.bind(this));
        this.copyTextBtn.addEventListener('click', this.copyText.bind(this));
        this.downloadAudioBtn.addEventListener('click', this.downloadAudio.bind(this));
        this.newImageBtn.addEventListener('click', this.resetApp.bind(this));
        this.retryBtn.addEventListener('click', this.processImage.bind(this));

        // Browse link
        const browseLink = document.querySelector('.browse-link');
        browseLink.addEventListener('click', () => this.fileInput.click());
    }

    handleDragOver(e) {
        e.preventDefault();
        this.uploadArea.classList.add('dragover');
    }

    handleDragLeave(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('dragover');
    }

    handleDrop(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.handleFile(files[0]);
        }
    }

    handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            this.handleFile(file);
        }
    }

    handleFile(file) {
        // Validate file type
        if (!file.type.startsWith('image/')) {
            this.showError('Please select a valid image file.');
            return;
        }

        // Validate file size (10MB limit)
        if (file.size > 10 * 1024 * 1024) {
            this.showError('Image size should be less than 10MB.');
            return;
        }

        this.currentFile = file;
        this.displayFileInfo(file);
    }

    displayFileInfo(file) {
        // Show file info section
        this.uploadArea.style.display = 'none';
        this.fileInfo.style.display = 'block';

        // Set file details
        this.fileName.textContent = file.name;
        this.fileSize.textContent = this.formatFileSize(file.size);

        // Create image preview
        const reader = new FileReader();
        reader.onload = (e) => {
            this.imagePreview.src = e.target.result;
        };
        reader.readAsDataURL(file);
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    async processImage() {
        if (!this.currentFile) {
            this.showError('No file selected.');
            return;
        }

        this.showLoading();

        try {
            const formData = new FormData();
            formData.append('file', this.currentFile);

            const response = await fetch(`${this.apiBaseUrl}/upload-and-process`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();

            if (result.success) {
                this.showResults(result);
            } else {
                throw new Error(result.message || 'Processing failed');
            }

        } catch (error) {
            console.error('Error processing image:', error);
            this.showError(error.message || 'Failed to process image. Please try again.');
        }
    }

    showLoading() {
        this.hideAllSections();
        this.loadingSection.style.display = 'block';
    }

    showResults(result) {
        this.hideAllSections();
        this.resultsSection.style.display = 'block';

        // Display extracted text
        this.extractedText.textContent = result.text || 'No text found in the image.';

        // Setup audio player if audio is available
        if (result.audio_url) {
            const audioUrl = `${this.apiBaseUrl}${result.audio_url}`;
            this.audioPlayer.src = audioUrl;
            this.audioPlayer.load();
            
            // Enable download button
            this.downloadAudioBtn.disabled = false;
            this.downloadAudioBtn.onclick = () => {
                const link = document.createElement('a');
                link.href = audioUrl;
                link.download = `extracted_audio_${Date.now()}.mp3`;
                link.click();
            };
        } else {
            this.audioPlayer.style.display = 'none';
            this.downloadAudioBtn.style.display = 'none';
        }
    }

    showError(message) {
        this.hideAllSections();
        this.errorSection.style.display = 'block';
        this.errorMessage.textContent = message;
    }

    hideAllSections() {
        this.loadingSection.style.display = 'none';
        this.resultsSection.style.display = 'none';
        this.errorSection.style.display = 'none';
    }

    copyText() {
        const text = this.extractedText.textContent;
        if (text && text !== 'No text found in the image.') {
            navigator.clipboard.writeText(text).then(() => {
                // Visual feedback
                const originalText = this.copyTextBtn.innerHTML;
                this.copyTextBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
                this.copyTextBtn.classList.add('btn-success');
                
                setTimeout(() => {
                    this.copyTextBtn.innerHTML = originalText;
                    this.copyTextBtn.classList.remove('btn-success');
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy text:', err);
                this.showNotification('Failed to copy text', 'error');
            });
        }
    }

    downloadAudio() {
        if (this.audioPlayer.src) {
            const link = document.createElement('a');
            link.href = this.audioPlayer.src;
            link.download = `extracted_audio_${Date.now()}.mp3`;
            link.click();
        }
    }

    resetApp() {
        this.currentFile = null;
        this.fileInput.value = '';
        this.hideAllSections();
        this.uploadArea.style.display = 'block';
        this.fileInfo.style.display = 'none';
        this.audioPlayer.src = '';
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        Object.assign(notification.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            padding: '12px 24px',
            borderRadius: '8px',
            color: 'white',
            fontWeight: '500',
            zIndex: '1000',
            opacity: '0',
            transform: 'translateY(-20px)',
            transition: 'all 0.3s ease'
        });

        if (type === 'success') {
            notification.style.background = 'var(--success-color)';
        } else if (type === 'error') {
            notification.style.background = 'var(--error-color)';
        } else {
            notification.style.background = 'var(--primary-color)';
        }

        document.body.appendChild(notification);

        // Animate in
        requestAnimationFrame(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateY(0)';
        });

        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateY(-20px)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new MonReader();
});

// Add some utility CSS for notifications
const style = document.createElement('style');
style.textContent = `
    .btn-success {
        background: var(--success-color) !important;
        color: white !important;
    }
    
    .notification {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        backdrop-filter: blur(10px);
    }
`;
document.head.appendChild(style);
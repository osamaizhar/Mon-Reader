class MonReader {
    constructor() {
        // Use relative URLs for Docker deployment, fallback to localhost for development
        this.apiBaseUrl = window.location.hostname === 'localhost' ? 'http://localhost:8000' : '/api';
        this.currentFile = null;
        this.initializeElements();
        this.attachEventListeners();
        this.checkApiConnection();
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
        this.audioResult = document.getElementById('audioResult');
        this.playAudioBtn = document.getElementById('playAudioBtn');
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

        // Play audio button
        if (this.playAudioBtn) {
            this.playAudioBtn.addEventListener('click', () => {
                if (this.audioPlayer && this.audioPlayer.src) {
                    if (this.audioPlayer.paused) {
                        this.audioPlayer.play();
                        this.playAudioBtn.innerHTML = '<i class="fas fa-pause"></i> Pause Audio';
                    } else {
                        this.audioPlayer.pause();
                        this.playAudioBtn.innerHTML = '<i class="fas fa-play"></i> Play Audio';
                    }
                }
            });
        }

        // Browse link
        const browseLink = document.querySelector('.browse-link');
        browseLink.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.fileInput.click();
        });

        // Auto-process on file select
        this.fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                this.handleFile(file);
                // Auto-process after a short delay to allow preview to load
                setTimeout(() => this.processImage(), 500);
            }
        });
    }

    async checkApiConnection() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                }
            });

            if (response.ok) {
                console.log('API connection successful');
            } else {
                console.error('API connection failed');
                this.showNotification('API server is not responding. Please check if the server is running.', 'error');
            }
        } catch (error) {
            console.error('API connection error:', error);
            this.showNotification('Cannot connect to API server. Please check if the server is running.', 'error');
        }
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
            // Auto-process after a short delay to allow preview to load
            setTimeout(() => this.processImage(), 500);
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

            console.log('Sending image for processing...');

            // Test direct audio access
            console.log('Testing audio endpoint access...');
            try {
                const audioTestResponse = await fetch(`${this.apiBaseUrl}/audio/73a8d1d7-d04c-4fca-87a2-2ef6b10cc672.mp3`, {
                    method: 'HEAD'
                });
                console.log('Audio test response status:', audioTestResponse.status);
                console.log('Audio test response headers:',
                    Array.from(audioTestResponse.headers.entries())
                        .map(([key, value]) => `${key}: ${value}`)
                        .join(', ')
                );
            } catch (audioTestError) {
                console.error('Audio test error:', audioTestError);
            }

            const response = await fetch(`${this.apiBaseUrl}/upload-and-process`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            console.log('Processing result:', result);

            if (result.success) {
                // Test if audio URL is accessible
                if (result.audio_url) {
                    const audioUrl = `${this.apiBaseUrl}${result.audio_url}`;
                    console.log('Testing audio URL accessibility:', audioUrl);
                    try {
                        const audioCheckResponse = await fetch(audioUrl, { method: 'HEAD' });
                        console.log('Audio URL check status:', audioCheckResponse.status);
                        console.log('Audio URL content type:', audioCheckResponse.headers.get('content-type'));
                        console.log('Audio URL content length:', audioCheckResponse.headers.get('content-length'));
                    } catch (audioCheckError) {
                        console.error('Audio URL check error:', audioCheckError);
                    }
                }

                this.showResults(result);
                this.showNotification('Image processed successfully!', 'success');
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

        // Enhanced debugging for audio
        console.log('Result object:', JSON.stringify(result));

        // Setup audio player if audio is available
        if (result.audio_url) {
            const audioUrl = `${this.apiBaseUrl}${result.audio_url}`;
            console.log('Audio URL:', audioUrl);

            // Make sure audio player container is visible
            if (this.audioResult) {
                this.audioResult.style.display = 'block';
                console.log('Audio result container displayed');
            }

            // Set audio source and display player
            this.audioPlayer.src = audioUrl;
            this.audioPlayer.style.display = 'block';
            this.audioPlayer.controls = true;
            console.log('Audio player source set to:', audioUrl);

            // Add error handling for audio loading
            this.audioPlayer.onerror = (e) => {
                console.error('Audio player error:', e);
                console.error('Error code:', this.audioPlayer.error ? this.audioPlayer.error.code : 'unknown');
                this.showNotification('Error loading audio. Please try again.', 'error');
            };

            // Force reload the audio element
            this.audioPlayer.load();
            console.log('Audio player reloaded');

            // Update play button text
            if (this.playAudioBtn) {
                this.playAudioBtn.innerHTML = '<i class="fas fa-play"></i> Play Audio';
                this.playAudioBtn.disabled = false;
                this.playAudioBtn.style.display = 'inline-flex';
                console.log('Play button enabled');

                // Add event listener for play button
                this.playAudioBtn.onclick = () => {
                    console.log('Play button clicked, audio paused state:', this.audioPlayer.paused);
                    if (this.audioPlayer.paused) {
                        const playPromise = this.audioPlayer.play();
                        if (playPromise !== undefined) {
                            playPromise.then(() => {
                                console.log('Audio playback started successfully');
                                this.playAudioBtn.innerHTML = '<i class="fas fa-pause"></i> Pause Audio';
                            }).catch(error => {
                                console.error('Audio playback failed:', error);
                                this.showNotification('Audio playback failed. Please try again.', 'error');
                            });
                        }
                    } else {
                        this.audioPlayer.pause();
                        this.playAudioBtn.innerHTML = '<i class="fas fa-play"></i> Play Audio';
                        console.log('Audio playback paused');
                    }
                };
            }

            // Enable download button
            this.downloadAudioBtn.disabled = false;
            this.downloadAudioBtn.style.display = 'inline-flex';
            console.log('Download button enabled');
            this.downloadAudioBtn.onclick = () => {
                const link = document.createElement('a');
                link.href = audioUrl;
                link.download = `extracted_audio_${Date.now()}.mp3`;
                console.log('Downloading audio from:', link.href);
                link.click();
            };

            // Add audio ended event listener
            this.audioPlayer.onended = () => {
                if (this.playAudioBtn) {
                    this.playAudioBtn.innerHTML = '<i class="fas fa-play"></i> Play Audio';
                    console.log('Audio playback ended');
                }
            };

            // Show notification that audio is ready
            this.showNotification('Audio generated successfully! Click Play to listen.', 'success');

        } else {
            // Hide audio section if no audio available
            console.log('No audio URL provided in the response');
            this.audioPlayer.style.display = 'none';
            if (this.playAudioBtn) this.playAudioBtn.style.display = 'none';
            this.downloadAudioBtn.style.display = 'none';

            if (this.audioResult) {
                this.audioResult.style.display = 'none';
            }

            // Show notification that audio generation failed
            this.showNotification('Text extracted, but audio generation failed.', 'warning');
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
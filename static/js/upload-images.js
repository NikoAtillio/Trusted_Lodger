class ImageUploadHandler {
    constructor() {
        this.dropZone = document.getElementById('drop-zone');
        this.fileInput = document.getElementById('images');
        this.previewContainer = document.getElementById('image-preview');
        this.progressBar = document.getElementById('upload-progress');
        this.uploadedFiles = new Set();
        this.maxFiles = 10;
        this.sortable = null;

        this.initializeEventListeners();
        this.initializeSortable();
    }

    initializeEventListeners() {
        if (this.dropZone && this.fileInput) {
            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                this.dropZone.addEventListener(eventName, this.preventDefaults);
            });

            ['dragenter', 'dragover'].forEach(eventName => {
                this.dropZone.addEventListener(eventName, () => {
                    this.dropZone.classList.add('highlight');
                });
            });

            ['dragleave', 'drop'].forEach(eventName => {
                this.dropZone.addEventListener(eventName, () => {
                    this.dropZone.classList.remove('highlight');
                });
            });

            this.dropZone.addEventListener('drop', (e) => {
                const droppedFiles = e.dataTransfer.files;
                this.handleFiles(droppedFiles);
            });

            this.fileInput.addEventListener('change', (e) => {
                this.handleFiles(e.target.files);
            });
        }

        const uploadButton = document.getElementById('upload-button');
        if (uploadButton) {
            uploadButton.addEventListener('click', () => this.uploadImages());
        }

        const bulkRemoveButton = document.getElementById('bulk-remove');
        if (bulkRemoveButton) {
            bulkRemoveButton.addEventListener('click', () => this.handleBulkRemove());
        }
    }

    initializeSortable() {
        this.sortable = new Sortable(this.previewContainer, {
            animation: 150,
            ghostClass: 'sortable-ghost',
            onEnd: () => {
                this.updateImageOrder();
            }
        });
    }

    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    async handleFiles(files) {
        if (this.uploadedFiles.size + files.length > this.maxFiles) {
            alert(`Maximum ${this.maxFiles} images allowed`);
            return;
        }

        const validFiles = Array.from(files).filter(file => this.validateFile(file));
        
        for (const file of validFiles) {
            await this.processFile(file);
        }
    }

    validateFile(file) {
        const validTypes = ['image/jpeg', 'image/png', 'image/jpg'];
        const maxSize = 5 * 1024 * 1024; // 5MB

        if (!validTypes.includes(file.type)) {
            alert(`Invalid file type: ${file.name}. Use JPEG or PNG`);
            return false;
        }

        if (file.size > maxSize) {
            alert(`File too large: ${file.name}. Maximum size is 5MB`);
            return false;
        }

        return true;
    }

    async processFile(file) {
        try {
            this.updateProgress(0);
            const compressedFile = await this.compressImage(file);
            const preview = await this.createPreview(compressedFile);
            
            this.uploadedFiles.add(compressedFile);
            this.previewContainer.appendChild(preview);
            
            this.updateProgress(100);
            setTimeout(() => this.hideProgress(), 1000);
        } catch (error) {
            console.error('Error processing file:', error);
            alert('Error processing file: ' + file.name);
        }
    }

    async compressImage(file) {
        return new Promise((resolve) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = (e) => {
                const img = new Image();
                img.src = e.target.result;
                img.onload = () => {
                    const canvas = document.createElement('canvas');
                    const ctx = canvas.getContext('2d');
                    
                    let width = img.width;
                    let height = img.height;
                    const maxDimension = 1920;
                    
                    if (width > maxDimension || height > maxDimension) {
                        const ratio = Math.min(maxDimension / width, maxDimension / height);
                        width *= ratio;
                        height *= ratio;
                    }
                    
                    canvas.width = width;
                    canvas.height = height;
                    ctx.drawImage(img, 0, 0, width, height);
                    
                    canvas.toBlob((blob) => {
                        const compressedFile = new File([blob], file.name, {
                            type: 'image/jpeg',
                            lastModified: Date.now()
                        });
                        resolve(compressedFile);
                    }, 'image/jpeg', 0.85);
                };
            };
        });
    }

    createPreview(file) {
        return new Promise((resolve) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onloadend = () => {
                const preview = document.createElement('div');
                preview.className = 'preview-item';
                preview.setAttribute('data-filename', file.name);
                preview.innerHTML = `
                    <img src="${reader.result}" alt="${file.name}">
                    <div class="preview-controls">
                        <input type="checkbox" class="bulk-select">
                    </div>
                    <div class="preview-progress"></div>
                `;

                const checkbox = preview.querySelector('.bulk-select');
                checkbox.addEventListener('change', () => {
                    preview.classList.toggle('selected', checkbox.checked);
                });

                resolve(preview);
            };
        });
    }

    handleBulkRemove() {
        // Handle existing images
        const existingCheckedBoxes = document.querySelectorAll('.existing-images .bulk-select:checked');
        existingCheckedBoxes.forEach(checkbox => {
            const imageId = checkbox.dataset.imageId;
            if (imageId) {
                fetch(`/accounts/delete-image/${imageId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': this.getCsrfToken(),
                    },
                })
                .then(response => {
                    if (response.ok) {
                        checkbox.closest('.existing-image-item').remove();
                    }
                })
                .catch(error => console.error('Error deleting image:', error));
            }
        });

        // Handle new preview images
        const previewCheckedBoxes = document.querySelectorAll('.image-preview .bulk-select:checked');
        previewCheckedBoxes.forEach(checkbox => {
            const previewItem = checkbox.closest('.preview-item');
            const filename = previewItem.getAttribute('data-filename');
            this.uploadedFiles.forEach(file => {
                if (file.name === filename) {
                    this.uploadedFiles.delete(file);
                }
            });
            previewItem.remove();
        });
    }

    async uploadImages() {
        const formData = new FormData();
        this.uploadedFiles.forEach(file => {
            formData.append('images', file);
        });

        try {
            const response = await fetch(window.location.href, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': this.getCsrfToken(),
                }
            });

            if (response.ok) {
                const data = await response.json();
                alert(data.message || 'Images uploaded successfully!');
                window.location.reload();
            } else {
                const errorData = await response.json();
                alert(errorData.error || 'An error occurred while uploading images.');
            }
        } catch (error) {
            console.error('Error uploading images:', error);
            alert('An unexpected error occurred. Please try again.');
        }
    }

    updateProgress(percent) {
        this.progressBar.style.width = percent + '%';
        this.progressBar.style.display = percent > 0 ? 'block' : 'none';
    }

    hideProgress() {
        this.progressBar.style.display = 'none';
    }

    updateImageOrder() {
        const previews = this.previewContainer.querySelectorAll('.preview-item');
        previews.forEach((preview, index) => {
            preview.setAttribute('data-order', index);
        });
    }

    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
}

// Initialize the handler when the document is ready
document.addEventListener('DOMContentLoaded', () => {
    new ImageUploadHandler();
});
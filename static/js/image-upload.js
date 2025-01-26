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

        // Bulk remove button
        document.getElementById('bulk-remove').addEventListener('click', () => {
            this.bulkRemove();
        });
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
            // Show progress
            this.updateProgress(0);
            
            // Compress image if needed
            const compressedFile = await this.compressImage(file);
            
            // Create preview
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
                    
                    // Calculate new dimensions
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
                        <button type="button" class="remove-btn">&times;</button>
                        <input type="checkbox" class="bulk-select">
                    </div>
                    <div class="preview-progress"></div>
                `;

                preview.querySelector('.remove-btn').addEventListener('click', () => {
                    this.uploadedFiles.delete(file);
                    preview.remove();
                });

                resolve(preview);
            };
        });
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
            const filename = preview.getAttribute('data-filename');
            // You can store the order in a hidden input or data attribute
            preview.setAttribute('data-order', index);
        });
    }

    bulkRemove() {
        const selected = this.previewContainer.querySelectorAll('.bulk-select:checked');
        selected.forEach(checkbox => {
            const preview = checkbox.closest('.preview-item');
            const filename = preview.getAttribute('data-filename');
            this.uploadedFiles.delete(Array.from(this.uploadedFiles)
                .find(file => file.name === filename));
            preview.remove();
        });
    }
}
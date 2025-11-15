/**
 * BUD Flight Validator - Frontend Application
 * Budapest Airport Flight Validation Client
 */

class FlightValidatorApp {
  constructor() {
    this.selectedFile = null;
    this.apiUrl = '/api/validate';
    this.initializeElements();
    this.attachEventListeners();
  }

  /**
   * DOM elemek inicializálása
   */
  initializeElements() {
    this.uploadArea = document.getElementById('uploadArea');
    this.fileInput = document.getElementById('fileInput');
    this.fileInfo = document.getElementById('fileInfo');
    this.fileName = document.getElementById('fileName');
    this.fileSize = document.getElementById('fileSize');
    this.removeFileBtn = document.getElementById('removeFile');
    this.validateBtn = document.getElementById('validateBtn');
    this.progressContainer = document.getElementById('progressContainer');
    this.progressFill = document.getElementById('progressFill');
    this.progressText = document.getElementById('progressText');
    this.resultPanel = document.getElementById('resultPanel');
    this.resultIcon = document.getElementById('resultIcon');
    this.resultTitle = document.getElementById('resultTitle');
    this.resultMessage = document.getElementById('resultMessage');
    this.downloadTemplateBtn = document.getElementById('downloadTemplate');
  }

  /**
   * Event listener-ek csatolása
   */
  attachEventListeners() {
    // Fájl input változás
    this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));

    // Drag & Drop
    this.uploadArea.addEventListener('click', () => this.fileInput.click());
    this.uploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
    this.uploadArea.addEventListener('dragleave', (e) => this.handleDragLeave(e));
    this.uploadArea.addEventListener('drop', (e) => this.handleDrop(e));

    // Fájl eltávolítása
    this.removeFileBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      this.removeFile();
    });

    // Validálás indítása
    this.validateBtn.addEventListener('click', () => this.validateFile());

    // Sablon letöltése
    this.downloadTemplateBtn.addEventListener('click', () => this.downloadTemplate());
  }

  /**
   * Drag over kezelése
   */
  handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    this.uploadArea.classList.add('drag-over');
  }

  /**
   * Drag leave kezelése
   */
  handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    this.uploadArea.classList.remove('drag-over');
  }

  /**
   * Drop kezelése
   */
  handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    this.uploadArea.classList.remove('drag-over');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      this.setFile(files[0]);
    }
  }

  /**
   * Fájl kiválasztás kezelése
   */
  handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
      this.setFile(file);
    }
  }

  /**
   * Fájl beállítása és validálása
   */
  setFile(file) {
    // Fájl típus ellenőrzése
    const allowedTypes = [
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', // .xlsx
      'application/vnd.ms-excel', // .xls
      'text/csv' // .csv
    ];

    const allowedExtensions = ['.xlsx', '.xls', '.csv'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();

    if (!allowedTypes.includes(file.type) && !allowedExtensions.includes(fileExtension)) {
      this.showError('Csak Excel (.xlsx, .xls) és CSV fájlok engedélyezettek!');
      return;
    }

    // Fájl méret ellenőrzése (max 10 MB)
    const maxSize = 10 * 1024 * 1024; // 10 MB
    if (file.size > maxSize) {
      this.showError('A fájl túl nagy! Maximum 10 MB engedélyezett.');
      return;
    }

    this.selectedFile = file;
    this.displayFileInfo(file);
  }

  /**
   * Fájl információk megjelenítése
   */
  displayFileInfo(file) {
    this.fileName.textContent = file.name;
    this.fileSize.textContent = this.formatFileSize(file.size);

    // UI frissítés
    this.uploadArea.style.display = 'none';
    this.fileInfo.style.display = 'flex';
    this.validateBtn.style.display = 'block';
    this.resultPanel.style.display = 'none';
  }

  /**
   * Fájl eltávolítása
   */
  removeFile() {
    this.selectedFile = null;
    this.fileInput.value = '';

    // UI visszaállítás
    this.uploadArea.style.display = 'block';
    this.fileInfo.style.display = 'none';
    this.validateBtn.style.display = 'none';
    this.progressContainer.style.display = 'none';
    this.resultPanel.style.display = 'none';
  }

  /**
   * Fájl méret formázása
   */
  formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  }

  /**
   * Fájl validálása - API hívás
   */
  async validateFile() {
    if (!this.selectedFile) {
      this.showError('Nincs kiválasztott fájl!');
      return;
    }

    // UI előkészítés
    this.validateBtn.disabled = true;
    this.progressContainer.style.display = 'block';
    this.resultPanel.style.display = 'none';
    this.updateProgress(0, 'Feltöltés...');

    try {
      // FormData készítés
      const formData = new FormData();
      formData.append('excelFile', this.selectedFile);

      // Progress animáció indítása
      this.animateProgress(0, 30, 1000);

      // API hívás
      const response = await fetch(this.apiUrl, {
        method: 'POST',
        body: formData
      });

      // Progress 30-60%
      this.animateProgress(30, 60, 500);

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Hiba történt a feldolgozás során');
      }

      // Progress 60-90%
      this.animateProgress(60, 90, 500);

      // Válasz fogadása Blob-ként (Excel fájl)
      const blob = await response.blob();

      // Progress 90-100%
      this.animateProgress(90, 100, 300);

      // Fájl letöltése
      this.downloadFile(blob, 'budapest-flights-validated.xlsx');

      // Siker üzenet
      setTimeout(() => {
        this.showSuccess('Sikeres ellenőrzés! A módosított fájl letöltése megkezdődött.');
      }, 500);

    } catch (error) {
      console.error('Validálási hiba:', error);
      this.showError(error.message || 'Ismeretlen hiba történt');
    } finally {
      this.validateBtn.disabled = false;
    }
  }

  /**
   * Progress bar animáció
   */
  animateProgress(from, to, duration) {
    const startTime = Date.now();
    const animate = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const currentValue = from + (to - from) * progress;

      this.updateProgress(currentValue, this.getProgressMessage(currentValue));

      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };

    animate();
  }

  /**
   * Progress frissítése
   */
  updateProgress(percent, message) {
    this.progressFill.style.width = percent + '%';
    this.progressText.textContent = message;
  }

  /**
   * Progress üzenet generálása
   */
  getProgressMessage(percent) {
    if (percent < 30) return 'Fájl feltöltése...';
    if (percent < 60) return 'Járatok ellenőrzése...';
    if (percent < 90) return 'Eredmények összeállítása...';
    return 'Fájl előkészítése letöltésre...';
  }

  /**
   * Fájl letöltése
   */
  downloadFile(blob, filename) {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  }

  /**
   * Sikeres eredmény megjelenítése
   */
  showSuccess(message) {
    this.progressContainer.style.display = 'none';
    this.resultPanel.style.display = 'block';
    this.resultPanel.className = 'result-panel success';
    this.resultIcon.textContent = '✅';
    this.resultTitle.textContent = 'Sikeres ellenőrzés!';
    this.resultMessage.textContent = message;
  }

  /**
   * Hiba megjelenítése
   */
  showError(message) {
    this.progressContainer.style.display = 'none';
    this.resultPanel.style.display = 'block';
    this.resultPanel.className = 'result-panel error';
    this.resultIcon.textContent = '❌';
    this.resultTitle.textContent = 'Hiba történt';
    this.resultMessage.textContent = message;
  }

  /**
   * Sablon letöltése
   */
  downloadTemplate() {
    // Egyszerű CSV sablon generálása
    const csvContent = [
      'Járatszám,Dátum,Idő,Megjegyzés',
      'FR8025,2025-11-15,10:30,',
      'W63701,2025-11-15,11:45,',
      'LH1345,2025-11-15,14:20,',
      'OS711,2025-11-15,09:15,'
    ].join('\n');

    const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
    this.downloadFile(blob, 'budapest-flights-template.csv');
  }
}

// Alkalmazás inicializálása
document.addEventListener('DOMContentLoaded', () => {
  new FlightValidatorApp();
  console.log('🛬 BUD Flight Validator App betöltve');
});

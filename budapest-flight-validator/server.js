const express = require('express');
const multer = require('multer');
const cors = require('cors');
const path = require('path');
const fs = require('fs').promises;
require('dotenv').config();

const ExcelProcessor = require('./src/excelProcessor');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Multer konfiguráció - fájl feltöltés
const storage = multer.diskStorage({
  destination: async (req, file, cb) => {
    const uploadDir = path.join(__dirname, 'uploads');
    try {
      await fs.mkdir(uploadDir, { recursive: true });
      cb(null, uploadDir);
    } catch (error) {
      cb(error);
    }
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, 'flight-' + uniqueSuffix + path.extname(file.originalname));
  }
});

const upload = multer({
  storage: storage,
  fileFilter: (req, file, cb) => {
    const allowedExtensions = ['.xlsx', '.xls', '.csv'];
    const ext = path.extname(file.originalname).toLowerCase();

    if (allowedExtensions.includes(ext)) {
      cb(null, true);
    } else {
      cb(new Error('Csak Excel (.xlsx, .xls) és CSV fájlok engedélyezettek!'));
    }
  },
  limits: {
    fileSize: 10 * 1024 * 1024 // 10 MB max
  }
});

// Főoldal
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'OK',
    message: 'BUD Flight Validator API működik',
    timestamp: new Date().toISOString()
  });
});

// Excel fájl feltöltése és feldolgozása
app.post('/api/validate', upload.single('excelFile'), async (req, res) => {
  let inputFilePath = null;
  let outputFilePath = null;

  try {
    if (!req.file) {
      return res.status(400).json({
        success: false,
        error: 'Nem található feltöltött fájl.'
      });
    }

    inputFilePath = req.file.path;
    const processor = new ExcelProcessor();

    // 1. Fájl struktúra validálása
    console.log('Fájl validálása:', inputFilePath);
    const validation = await processor.validateExcelStructure(inputFilePath);

    if (!validation.valid) {
      await fs.unlink(inputFilePath); // Töröljük a hibás fájlt
      return res.status(400).json({
        success: false,
        error: validation.error
      });
    }

    console.log(`Struktúra OK. ${validation.rowCount} sor feldolgozása...`);

    // 2. Excel feldolgozása
    outputFilePath = inputFilePath.replace('.xlsx', '-validated.xlsx');
    const result = await processor.processExcelFile(inputFilePath, outputFilePath);

    console.log(`Feldolgozás kész: ${result.processedRows} sor ellenőrizve.`);

    // 3. Fájl letöltésének visszaadása
    res.download(outputFilePath, 'budapest-flights-validated.xlsx', async (err) => {
      // Cleanup - fájlok törlése a letöltés után
      try {
        if (inputFilePath) await fs.unlink(inputFilePath);
        if (outputFilePath) await fs.unlink(outputFilePath);
      } catch (cleanupError) {
        console.error('Cleanup hiba:', cleanupError);
      }

      if (err) {
        console.error('Letöltési hiba:', err);
        if (!res.headersSent) {
          res.status(500).json({
            success: false,
            error: 'Fájl letöltési hiba történt.'
          });
        }
      }
    });
  } catch (error) {
    console.error('Feldolgozási hiba:', error);

    // Cleanup hibás fájlok
    try {
      if (inputFilePath) await fs.unlink(inputFilePath);
      if (outputFilePath) await fs.unlink(outputFilePath);
    } catch (cleanupError) {
      console.error('Cleanup hiba:', cleanupError);
    }

    res.status(500).json({
      success: false,
      error: error.message || 'Ismeretlen hiba történt a feldolgozás során.'
    });
  }
});

// Hibakezelés
app.use((error, req, res, next) => {
  console.error('Szerver hiba:', error);

  if (error instanceof multer.MulterError) {
    if (error.code === 'LIMIT_FILE_SIZE') {
      return res.status(400).json({
        success: false,
        error: 'A fájl túl nagy. Maximum 10 MB engedélyezett.'
      });
    }
  }

  res.status(500).json({
    success: false,
    error: error.message || 'Szerver hiba történt.'
  });
});

// 404 kezelés
app.use((req, res) => {
  res.status(404).json({
    success: false,
    error: 'Nem található endpoint.'
  });
});

// Szerver indítása
app.listen(PORT, () => {
  console.log('╔════════════════════════════════════════════════════╗');
  console.log('║   🛬 BUD Érkező Járatszám Ellenőrző SZERVER   🛬   ║');
  console.log('╚════════════════════════════════════════════════════╝');
  console.log('');
  console.log(`✅ Szerver fut: http://localhost:${PORT}`);
  console.log(`📂 API endpoint: http://localhost:${PORT}/api/validate`);
  console.log('');
  console.log('A szerver leállításához: Ctrl+C');
  console.log('════════════════════════════════════════════════════');
});

module.exports = app;

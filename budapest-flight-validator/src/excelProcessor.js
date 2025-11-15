const ExcelJS = require('exceljs');
const FlightValidator = require('./flightValidator');

/**
 * Excel feldolgozó modul
 * Kezeli az Excel fájlok beolvasását, módosítását és visszaírását
 * KRITIKUS: Csak a Megjegyzés oszlopot módosítja, minden mást érintetlenül hagy
 */

class ExcelProcessor {
  constructor() {
    this.validator = new FlightValidator();
    this.notesColumnNames = ['Megjegyzés', 'Notes', 'megjegyzés', 'notes', 'MEGJEGYZÉS', 'NOTES'];
    this.flightNumberColumnNames = ['Járatszám', 'Flight Number', 'Járat', 'Flight', 'járatszám', 'flight number'];
    this.dateColumnNames = ['Dátum', 'Date', 'Érkezés dátuma', 'Arrival Date', 'dátum', 'date'];
    this.timeColumnNames = ['Idő', 'Time', 'Időpont', 'Érkezési idő', 'Arrival Time', 'idő', 'time'];
  }

  /**
   * Fő feldolgozó függvény
   */
  async processExcelFile(inputPath, outputPath) {
    try {
      const workbook = new ExcelJS.Workbook();

      // Excel fájl beolvasása - MINDEN formázással együtt
      await workbook.xlsx.readFile(inputPath);

      // Első munkalap feldolgozása (vagy később minden lapot)
      const worksheet = workbook.getWorksheet(1);

      if (!worksheet) {
        throw new Error('A fájl nem tartalmaz munkalapot.');
      }

      // Oszlopok azonosítása
      const columns = this.identifyColumns(worksheet);

      if (!columns.flightNumber || !columns.notes) {
        throw new Error('Nem találhatók meg a szükséges oszlopok (Járatszám, Megjegyzés).');
      }

      // Sorok feldolgozása (2. sortól, mert az 1. fejléc)
      const rowCount = worksheet.rowCount;
      const processedRows = [];

      for (let rowNum = 2; rowNum <= rowCount; rowNum++) {
        const row = worksheet.getRow(rowNum);

        // Csak akkor dolgozzuk fel, ha van járatszám
        const flightNumber = this.getCellValue(row, columns.flightNumber);

        if (flightNumber) {
          const date = this.getCellValue(row, columns.date);
          const time = this.getCellValue(row, columns.time);

          // Járat validálása
          const validationResult = await this.validator.validateFlight(flightNumber, date, time);

          // KRITIKUS: Csak a Notes oszlopot módosítjuk!
          // Az eredeti cella formázását megtartjuk
          const notesCell = row.getCell(columns.notes);

          if (validationResult.error || validationResult.message) {
            notesCell.value = validationResult.message;
          } else {
            // Ha nincs hiba, üresen hagyjuk
            notesCell.value = '';
          }

          // NEM módosítjuk a cella formázását!
          // A notesCell.style automatikusan megtartja az eredeti style-t

          processedRows.push({
            row: rowNum,
            flightNumber,
            result: validationResult.message || 'OK'
          });
        }
      }

      // Módosított fájl mentése - MINDEN eredeti formázással
      await workbook.xlsx.writeFile(outputPath);

      return {
        success: true,
        processedRows: processedRows.length,
        details: processedRows
      };
    } catch (error) {
      console.error('Excel feldolgozási hiba:', error);
      throw error;
    }
  }

  /**
   * Oszlopok azonosítása a fejlécben
   */
  identifyColumns(worksheet) {
    const headerRow = worksheet.getRow(1);
    const columns = {
      flightNumber: null,
      date: null,
      time: null,
      notes: null
    };

    headerRow.eachCell((cell, colNumber) => {
      const cellValue = String(cell.value || '').trim();

      // Járatszám oszlop keresése
      if (this.flightNumberColumnNames.some(name => cellValue.includes(name))) {
        columns.flightNumber = colNumber;
      }

      // Dátum oszlop keresése
      if (this.dateColumnNames.some(name => cellValue.includes(name))) {
        columns.date = colNumber;
      }

      // Idő oszlop keresése
      if (this.timeColumnNames.some(name => cellValue.includes(name))) {
        columns.time = colNumber;
      }

      // Megjegyzés oszlop keresése
      if (this.notesColumnNames.some(name => cellValue.includes(name))) {
        columns.notes = colNumber;
      }
    });

    return columns;
  }

  /**
   * Cella értékének biztonságos kiolvasása
   */
  getCellValue(row, columnNumber) {
    if (!columnNumber) return null;

    const cell = row.getCell(columnNumber);

    if (!cell || cell.value === null || cell.value === undefined) {
      return null;
    }

    // Ha dátum típus
    if (cell.value instanceof Date) {
      return cell.value;
    }

    // Ha formula eredménye
    if (cell.type === ExcelJS.ValueType.Formula && cell.result !== undefined) {
      return cell.result;
    }

    // Egyébként string-ként visszaadjuk
    return cell.value;
  }

  /**
   * Excel fájl validálása feltöltés előtt
   */
  async validateExcelStructure(filePath) {
    try {
      const workbook = new ExcelJS.Workbook();
      await workbook.xlsx.readFile(filePath);

      const worksheet = workbook.getWorksheet(1);
      if (!worksheet) {
        return {
          valid: false,
          error: 'A fájl nem tartalmaz munkalapot.'
        };
      }

      const columns = this.identifyColumns(worksheet);

      if (!columns.flightNumber) {
        return {
          valid: false,
          error: 'Nem található "Járatszám" vagy "Flight Number" oszlop.'
        };
      }

      if (!columns.notes) {
        return {
          valid: false,
          error: 'Nem található "Megjegyzés" vagy "Notes" oszlop.'
        };
      }

      return {
        valid: true,
        columns,
        rowCount: worksheet.rowCount - 1 // Fejléc nélkül
      };
    } catch (error) {
      return {
        valid: false,
        error: `Fájl olvasási hiba: ${error.message}`
      };
    }
  }
}

module.exports = ExcelProcessor;

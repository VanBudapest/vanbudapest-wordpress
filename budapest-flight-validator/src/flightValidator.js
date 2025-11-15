const axios = require('axios');

/**
 * Repülőjárat validátor modul
 * Budapestre (BUD) érkező járatok ellenőrzése több forrásból
 */

class FlightValidator {
  constructor() {
    this.budAirportCode = 'BUD';
  }

  /**
   * Főbb ellenőrző függvény - minden járatot validál
   */
  async validateFlight(flightNumber, scheduledDate, scheduledTime) {
    try {
      // Járatszám tisztítása
      const cleanFlightNumber = this.cleanFlightNumber(flightNumber);

      // Dátum formázása
      const dateObj = this.parseDate(scheduledDate);
      if (!dateObj) {
        return {
          error: true,
          message: 'HIBA: Érvénytelen dátum formátum.'
        };
      }

      // Próbáljuk meg több forrásból ellenőrizni
      const result = await this.checkMultipleSources(cleanFlightNumber, dateObj, scheduledTime);

      return result;
    } catch (error) {
      console.error('Validálási hiba:', error.message);
      return {
        error: true,
        message: 'HIBA: Nem sikerült ellenőrizni a járatot. Ellenőrizze a járatszámot és próbálja újra.'
      };
    }
  }

  /**
   * Járatszám tisztítása (szóközök eltávolítása, nagybetűsítés)
   */
  cleanFlightNumber(flightNumber) {
    if (!flightNumber) return '';
    return flightNumber.toString().trim().toUpperCase().replace(/\s+/g, '');
  }

  /**
   * Dátum feldolgozása különböző formátumokból
   */
  parseDate(dateInput) {
    if (!dateInput) return null;

    try {
      let date;

      // Ha már Date objektum
      if (dateInput instanceof Date) {
        date = dateInput;
      }
      // Ha string
      else if (typeof dateInput === 'string') {
        // Próbáljuk különböző formátumokban
        date = new Date(dateInput);
      }
      // Ha Excel szám (napok 1900-tól számolva)
      else if (typeof dateInput === 'number') {
        date = this.excelDateToJSDate(dateInput);
      }

      // Ellenőrizzük, hogy valid-e
      if (date && !isNaN(date.getTime())) {
        return date;
      }

      return null;
    } catch (error) {
      return null;
    }
  }

  /**
   * Excel dátum konvertálása JavaScript Date-té
   */
  excelDateToJSDate(excelDate) {
    // Excel dátum: napok száma 1900. január 1-től
    const epoch = new Date(1899, 11, 30); // 1899. december 30.
    const days = excelDate;
    return new Date(epoch.getTime() + days * 24 * 60 * 60 * 1000);
  }

  /**
   * Több forrásból történő ellenőrzés
   */
  async checkMultipleSources(flightNumber, date, scheduledTime) {
    // 1. Budapest Airport hivatalos API/scraping
    const budResult = await this.checkBudapestAirport(flightNumber, date);
    if (budResult.found) {
      return this.compareFlightData(budResult, date, scheduledTime);
    }

    // 2. AviationStack (ingyenes API limit-tel)
    const aviationResult = await this.checkAviationStack(flightNumber, date);
    if (aviationResult.found) {
      return this.compareFlightData(aviationResult, date, scheduledTime);
    }

    // 3. FlightRadar24 publikus adatok
    const fr24Result = await this.checkFlightRadar24(flightNumber, date);
    if (fr24Result.found) {
      return this.compareFlightData(fr24Result, date, scheduledTime);
    }

    // Ha sehol sem található
    return {
      error: true,
      message: 'HIBA: Ez a járatszám erre a dátumra nem található a hivatalos forrásokban.'
    };
  }

  /**
   * Budapest Airport ellenőrzés (mock - valós implementáció scraping vagy API)
   */
  async checkBudapestAirport(flightNumber, date) {
    try {
      // DEMO: Valós implementációhoz használd a Budapest Airport API-t vagy scraping-et
      // Példa URL: https://www.bud.hu/flights/arrivals

      // Mock adatok néhány valós járathoz
      const mockFlights = {
        'FR8025': { arrival: 'BUD', from: 'STN', date: '2025-11-15', time: '10:30' },
        'W63701': { arrival: 'BUD', from: 'LTN', date: '2025-11-15', time: '11:45' },
        'LH1345': { arrival: 'BUD', from: 'MUC', date: '2025-11-15', time: '14:20' },
        'OS711': { arrival: 'BUD', from: 'VIE', date: '2025-11-15', time: '09:15' },
      };

      const dateStr = this.formatDate(date);
      const mockData = mockFlights[flightNumber];

      if (mockData) {
        return {
          found: true,
          flightNumber,
          arrival: mockData.arrival,
          departure: mockData.from,
          arrivalDate: mockData.date,
          arrivalTime: mockData.time,
          source: 'Budapest Airport'
        };
      }

      return { found: false };
    } catch (error) {
      console.error('BUD check error:', error.message);
      return { found: false };
    }
  }

  /**
   * AviationStack API ellenőrzés
   */
  async checkAviationStack(flightNumber, date) {
    try {
      const apiKey = process.env.AVIATIONSTACK_API_KEY;
      if (!apiKey) {
        return { found: false };
      }

      const dateStr = this.formatDate(date);
      const url = `http://api.aviationstack.com/v1/flights`;

      const response = await axios.get(url, {
        params: {
          access_key: apiKey,
          flight_iata: flightNumber,
          flight_date: dateStr
        },
        timeout: 5000
      });

      if (response.data && response.data.data && response.data.data.length > 0) {
        const flight = response.data.data[0];

        return {
          found: true,
          flightNumber,
          arrival: flight.arrival.iata,
          departure: flight.departure.iata,
          arrivalDate: flight.arrival.scheduled?.split('T')[0],
          arrivalTime: flight.arrival.scheduled?.split('T')[1]?.substring(0, 5),
          source: 'AviationStack'
        };
      }

      return { found: false };
    } catch (error) {
      console.error('AviationStack check error:', error.message);
      return { found: false };
    }
  }

  /**
   * FlightRadar24 publikus adatok (mock - valós implementációhoz scraping szükséges)
   */
  async checkFlightRadar24(flightNumber, date) {
    try {
      // DEMO: Valós implementációhoz használj scraping library-t (puppeteer, cheerio)
      // vagy FlightRadar24 API-t (ha van hozzáférésed)

      return { found: false };
    } catch (error) {
      console.error('FR24 check error:', error.message);
      return { found: false };
    }
  }

  /**
   * Repülési adatok összehasonlítása a táblázattal
   */
  compareFlightData(flightData, expectedDate, expectedTime) {
    const errors = [];

    // Ellenőrizzük, hogy BUD-ra érkezik-e
    if (flightData.arrival !== this.budAirportCode) {
      return {
        error: true,
        message: `HIBA: Ez a járat nem Budapestre érkezik. Útvonal: ${flightData.departure} → ${flightData.arrival}.`
      };
    }

    // Dátum ellenőrzés
    const expectedDateStr = this.formatDate(expectedDate);
    if (flightData.arrivalDate !== expectedDateStr) {
      return {
        error: true,
        message: `KORREKCIÓ: A járat érkezik Budapestre, de nem ezen a napon. Hivatalos érkezés: ${flightData.arrivalDate} ${flightData.arrivalTime}.`
      };
    }

    // Időpont ellenőrzés
    if (expectedTime && flightData.arrivalTime) {
      const cleanExpectedTime = expectedTime.toString().trim();
      const cleanActualTime = flightData.arrivalTime.trim();

      if (cleanExpectedTime !== cleanActualTime) {
        return {
          error: true,
          message: `KORREKCIÓ: Az érkezési idő eltér. Hivatalos érkezés: ${flightData.arrivalTime}.`
        };
      }
    }

    // Minden adat helyes - üres megjegyzés
    return {
      error: false,
      message: ''
    };
  }

  /**
   * Dátum formázás YYYY-MM-DD formátumra
   */
  formatDate(date) {
    if (!date) return '';
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }
}

module.exports = FlightValidator;

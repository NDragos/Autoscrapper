# Autoscrapper

A powerful Python-based web scraper designed to extract and collect data about vehicles from various online sources. This tool automates the process of gathering vehicle information, making it easy to compile comprehensive datasets for analysis, comparison, or research purposes.

## Overview

Autoscrapper is a specialized web scraping tool that helps you collect vehicle data efficiently. Whether you're looking to gather information about car specifications, pricing, availability, or market trends, this scraper provides a reliable and automated solution.

## Features

- **Automated Data Collection**: Automatically scrapes vehicle information from multiple sources
- **Customizable Scraping**: Configure which data fields to extract based on your needs
- **Data Export**: Export scraped data in various formats (CSV, JSON, Excel)
- **Error Handling**: Robust error handling and retry mechanisms for reliable scraping
- **Rate Limiting**: Built-in rate limiting to respect website policies
- **Data Validation**: Validates and cleans scraped data for consistency
- **Multi-threading Support**: Parallel scraping for improved performance

## Vehicle Data Fields

The scraper can collect various types of vehicle information, including:

- Make and Model
- Year of manufacture
- Price (new/used)
- Mileage
- Engine specifications
- Fuel type
- Transmission type
- Color
- VIN (Vehicle Identification Number)
- Location
- Seller information
- Vehicle features and options
- Images and media

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/NDragos/Autoscrapper.git
cd Autoscrapper
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
   - A `.env` file has been created for you with a default MongoDB connection string.
   - **Security Note:** Never commit your real production secrets to version control.

## Usage

### 1. Scraping Data
Run the scraper to collect data from Autovit.
```bash
cd scripts
python scrapper.py
```
This will generate CSV files in the `data/` directory (e.g., `daciasandero.csv`).
*Note: You can modify the `scrape_autovit` call at the bottom of `scripts/scrapper.py` to scrape different car models.*

### 2. Populating the Database
Import the scraped CSV data into MongoDB.
```bash
cd scripts
python populate_db.py
```
This script reads `data/date_autovit_test.csv` (or your scraped file if you update the script) and uploads it to the MongoDB collection specified in `.env`.

### 3. Running the Backend Server
Start the Flask API server.
```bash
cd scripts
python server.py
```
The server will start (usually on `http://127.0.0.1:5000`), serving endpoints like `/api/optiuni` and `/api/cauta`.

### 4. Frontend
Open `website/index.html` in your browser to interact with the application.


2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Dependencies

The scraper relies on the following Python libraries:

- **requests**: For making HTTP requests
- **BeautifulSoup4**: For parsing HTML content
- **selenium**: For dynamic content scraping (if needed)
- **pandas**: For data manipulation and export
- **lxml**: For efficient HTML/XML parsing

## Usage

### Basic Usage

```python
from autoscrapper import VehicleScraper

# Initialize the scraper
scraper = VehicleScraper()

# Scrape vehicle data
vehicles = scraper.scrape(url="https://example-auto-site.com")

# Export data
scraper.export_to_csv(vehicles, "vehicle_data.csv")
```

### Advanced Configuration

```python
from autoscrapper import VehicleScraper

# Configure scraper with custom settings
scraper = VehicleScraper(
    max_pages=10,
    delay=2,  # seconds between requests
    timeout=30,
    output_format="json"
)

# Scrape with filters
vehicles = scraper.scrape(
    url="https://example-auto-site.com",
    filters={
        "make": "Toyota",
        "year_min": 2020,
        "price_max": 30000
    }
)

# Process results
for vehicle in vehicles:
    print(f"{vehicle['year']} {vehicle['make']} {vehicle['model']} - ${vehicle['price']}")
```

## Configuration

Create a `config.json` file to customize scraper behavior:

```json
{
    "scraping": {
        "max_concurrent_requests": 5,
        "request_delay": 2,
        "timeout": 30,
        "retry_attempts": 3
    },
    "data": {
        "output_directory": "./output",
        "default_format": "csv",
        "include_images": false
    },
    "filters": {
        "min_year": 2015,
        "max_price": 50000
    }
}
```

## Output Formats

The scraper supports multiple output formats:

- **CSV**: Comma-separated values for spreadsheet applications
- **JSON**: JavaScript Object Notation for web applications
- **Excel**: `.xlsx` format for Microsoft Excel
- **SQLite**: Database storage for large datasets

## Best Practices

1. **Respect robots.txt**: Always check and follow the website's robots.txt file
2. **Rate Limiting**: Don't overwhelm servers with too many requests
3. **User Agent**: Use appropriate user agent strings
4. **Legal Compliance**: Ensure your scraping activities comply with local laws and website terms of service
5. **Data Privacy**: Handle scraped data responsibly and respect privacy regulations

## Troubleshooting

### Common Issues

- **Connection Errors**: Check your internet connection and verify the target URL is accessible
- **Parsing Errors**: Website structure may have changed; update selectors accordingly
- **Rate Limiting**: Increase delay between requests if getting blocked
- **Missing Data**: Verify the website contains the expected data fields

## Contributing

Contributions are welcome! To contribute to Autoscrapper:

1. Fork the repository
2. Create a new branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure your code follows the project's coding standards and includes appropriate tests.

## Ethical Considerations

- Always review and comply with the target website's Terms of Service
- Respect copyright and intellectual property rights
- Use scraped data responsibly and ethically
- Implement appropriate delays to avoid overloading servers
- Consider the impact of your scraping activities on website performance

## Roadmap

Future enhancements planned:

- [ ] Support for additional vehicle listing websites
- [ ] Image downloading and processing
- [ ] Machine learning integration for data classification
- [ ] Real-time monitoring and alerts
- [ ] API integration for direct data access
- [ ] Web dashboard for data visualization

## License

This project is available for use under standard software licensing terms. Users are responsible for ensuring their use complies with applicable laws and regulations.

## Copyright

Copyright (c) 2025 NDragos. All rights reserved.

This software is provided for educational and research purposes. Users must ensure compliance with all applicable laws, regulations, and website terms of service when using this scraper.

## Disclaimer

This tool is intended for educational and research purposes only. Users are solely responsible for ensuring their web scraping activities comply with:

- Applicable laws and regulations
- Website terms of service
- Data protection and privacy laws (GDPR, CCPA, etc.)
- Copyright and intellectual property rights

The authors and contributors of this project accept no liability for misuse of this software or any resulting damages.

## Contact

For questions, suggestions, or issues, please open an issue on the GitHub repository.

## Acknowledgments

Special thanks to all contributors and the open-source community for their valuable libraries and tools that make this project possible.

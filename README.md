# Real Estate Agent Data Scraper

This project scrapes real estate agent data from realestate.com.au, collecting comprehensive information about agents across different regions in Australia.

## Features

- Scrapes agent data from multiple regions
- Collects detailed information including:
  - Basic information (name, company)
  - Contact details
  - Profile images
  - Ratings and reviews
  - Agent descriptions
  - Sold properties
  - Current properties for sale
  - Sales statistics
- Saves data in both CSV and JSON formats
- Implements rate limiting and random delays to avoid being blocked
- Uses headless browser for efficient scraping
- Periodic data saving to prevent data loss

## Requirements

- Python 3.8+
- Chrome browser installed
- Internet connection

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the scraper:
```bash
python scraper.py
```

2. The script will:
   - Automatically detect available regions
   - Scrape agent listings from each region
   - Collect detailed information from each agent's profile
   - Save data periodically to the `output` directory

3. Output files:
   - `output/agents_data.json`: Complete data in JSON format
   - `output/agents_data.csv`: Data in CSV format for easy viewing in spreadsheet applications

## Notes

- The scraper implements random delays between requests to avoid overwhelming the server
- Data is saved every 100 agents to prevent data loss
- The script uses a headless browser, so you won't see the browser window
- If the script is interrupted, you can restart it and it will continue from where it left off

## Error Handling

- The script includes comprehensive error handling
- Failed requests are logged but won't stop the scraping process
- Missing data fields are handled gracefully and stored as null values

## Legal Notice

Please ensure you comply with the website's terms of service and robots.txt file when using this scraper. The script includes appropriate delays to avoid overloading the server. 
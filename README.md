# Contact Scraper

A powerful tool for scraping contact information such as emails and phone numbers from websites based on search queries .

## Overview

This tool searches the web for specific keywords related to contacts (recruiters, professors, researchers, etc.), then extracts contact information including:

- Names
- Email addresses
- Phone numbers
- Job titles/roles

The data is saved in a structured CSV format, making it easy to import into contact management systems or email marketing tools.

## Features

- 🔍 Intelligent search based on configurable keywords
- 📧 Email extraction with context-aware name and role detection
- 📱 Phone number detection
- 🔄 Duplicate prevention - won't add contacts that already exist in your CSV
- 🧠 Smart parsing to associate names with the right contact information
- 🔄 Append mode to keep building your contact database

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/contact-scraper.git
   cd contact-scraper
   ```

2. Install the required dependencies:
   ```
   pip install -r requirement.txt
   ```

## Usage

1. Customize the search keywords in `config.py` to target specific types of contacts:

   ```python
   SEARCH_KEYWORDS = [
       "AI researcher email contact",
       "Machine Learning recruiter email",
       # Add your own keywords here
   ]
   ```

2. Run the main script:

   ```
   python main.py
   ```

3. Your contacts will be stored in `data/contacts.csv`

## How It Works

1. The tool searches the web using the Google search API based on your keywords
2. It visits each search result URL and extracts page content
3. Using pattern matching, it identifies emails, phone numbers, and contextual information
4. It attempts to associate names and roles with each contact by analyzing surrounding text
5. All new, unique contacts are saved to the CSV file

## Project Structure

- `main.py` - Main entry point for the application
- `config.py` - Configuration settings including search keywords
- `scraper/`
  - `search_engine.py` - Handles web searches
  - `email_scraper.py` - Extracts contacts from web pages
  - `utils.py` - Helper functions
- `data/` - Where extracted contacts are stored

## Future Improvements

- Add LinkedIn specific scraping
- Enhance name detection algorithm
- Add company detection
- Support for export to different formats (JSON, Excel)
- Web interface for managing contacts

## Legal Notice

This tool is for educational purposes only. Always respect website terms of service and privacy policies when scraping content. Use responsibly and ethically.

## License

MIT License

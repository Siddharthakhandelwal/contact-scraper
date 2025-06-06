# Contact Scraper

A powerful tool for scraping contact information such as emails and phone numbers from websites based on search queries.

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
- 📨 Email sender to reach out to contacts with personalized messages and attachments

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

### Contact Scraping

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

### Email Sender

The tool includes an email sender to contact the scraped leads with personalized messages:

1. Create an email template or use the provided `email_template.txt`

2. Run the email sender (with a resume or file attachment):

   ```
   python email_sender.py --attachment path/to/your/resume.pdf --subject "Your Subject Line"
   ```

3. Additional options:

   ```
   python email_sender.py --help
   ```

   Key options:

   - `--csv`: Path to the contacts CSV (default: data/contacts.csv)
   - `--template`: Path to your email template file
   - `--delay`: Delay between emails in seconds (default: 5)
   - `--limit`: Limit the number of emails to send
   - `--test`: Test mode to preview emails without sending

4. **Important Note for Gmail Users**: You need to use an "App Password" instead of your regular password. [Learn how to create an App Password](https://support.google.com/accounts/answer/185833).

## How It Works

1. The tool searches the web using the Google search API based on your keywords
2. It visits each search result URL and extracts page content
3. Using pattern matching, it identifies emails, phone numbers, and contextual information
4. It attempts to associate names and roles with each contact by analyzing surrounding text
5. All new, unique contacts are saved to the CSV file
6. The email sender can then use this CSV to send personalized outreach emails

## Project Structure

- `main.py` - Main entry point for the application
- `config.py` - Configuration settings including search keywords
- `email_sender.py` - Tool for sending personalized emails to contacts
- `email_template.txt` - Sample template for outreach emails
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
- Email tracking and analytics

## Legal Notice

This tool is for educational purposes only. Always respect website terms of service and privacy policies when scraping content. Use responsibly and ethically.

When sending emails, ensure you comply with anti-spam laws such as CAN-SPAM, GDPR, and CASL. Always provide an unsubscribe option and your physical address.

## License

MIT License

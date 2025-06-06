 # Contact Scraper

A Python-based tool for automatically scraping contact information from search results based on specified keywords. The tool extracts names, email addresses, phone numbers, and professional roles, saving them to a CSV file while avoiding duplicates.

## Features

- 🔍 Automated Google search based on keywords
- 📧 Email and contact information extraction
- 📱 Phone number detection
- 📊 CSV export with deduplication
- ✉️ Email sending capability
- 🔄 Status tracking for contacts

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/contact-scraper.git
   cd contact-scraper
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirement.txt
   ```

## Configuration

1. Create or modify `config.py` with your search keywords:
   ```python
   SEARCH_KEYWORDS = [
       "your search keyword 1",
       "your search keyword 2"
   ]
   ```

2. For email functionality, configure your email settings in `config.py`:
   ```python
   EMAIL_CONFIG = {
       "smtp_server": "smtp.gmail.com",
       "smtp_port": 587,
       "username": "your-email@gmail.com",
       "password": "your-app-specific-password"  # Use app-specific password for Gmail
   }
   ```

## Project Structure

```
contact-scraper/
├── data/               # Directory for storing scraped data
├── scraper/           # Core scraping functionality
├── config.py          # Configuration settings
├── email_sender.py    # Email sending functionality
├── main.py           # Main script
├── test_email.py     # Email testing script
└── requirement.txt   # Project dependencies
```

## Usage

1. Run the main scraper:
   ```bash
   python main.py
   ```
   This will:
   - Search for contacts based on keywords in `config.py`
   - Extract contact information from search results
   - Save unique contacts to `data/contacts.csv`



## Output Format

The scraped data is saved in `data/contacts.csv` with the following columns:
- Name
- Email
- Phone
- Title/Role
- Source URL
- Status

## Important Notes

1. Respect website terms of service and robots.txt when scraping
2. Use appropriate delays between requests to avoid being blocked
3. Keep your email credentials secure
4. For Gmail, use App Passwords instead of your account password

## Troubleshooting

1. If you encounter SMTP authentication issues:
   - For Gmail, enable 2-factor authentication and use an App Password
   - Check your email server settings in config.py

2. If scraping results are limited:
   - Try adjusting your search keywords
   - Check if you're being rate-limited
   - Ensure you have a stable internet connection

## Contributing

Feel free to fork the repository and submit pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
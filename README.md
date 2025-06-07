# Contact Scraper

A Python-based tool for automatically scraping contact information from search results based on specified keywords. The tool extracts names, email addresses, phone numbers, and professional roles, saving them to a CSV file while avoiding duplicates.

## Features

- 🔍 Automated Google search based on keywords
- 📧 Email and contact information extraction with context awareness
- 📱 Phone number detection with international format support
- 📊 CSV export with deduplication and status tracking
- ✉️ Bulk email sending with personalization and rate limiting
- 🔄 Status tracking for contacts (Pending/Sent)
- 🛡️ User agent rotation to avoid blocking
- ⏳ Configurable delays between requests

## Core Components

### Main Modules:
1. **main.py** - Orchestrates the scraping workflow:
   - Reads existing contacts to avoid duplicates
   - Executes searches for each keyword
   - Processes results through the scraper
   - Saves new contacts to CSV

2. **email_sender.py** - Handles email operations:
   - Loads contacts with "Pending" status
   - Sends personalized emails with template support
   - Updates contact status to "Sent"
   - Includes self-test mode for configuration verification
   - Implements rate limiting (max 450 emails per run)

3. **scraper/email_scraper.py** - Contact extraction:
   - Extracts emails using regex patterns
   - Finds phone numbers in various formats
   - Identifies names and roles near email addresses
   - Uses random user agents to avoid detection

4. **scraper/search_engine.py** - Search functionality:
   - Performs Google searches for each keyword
   - Returns unique search results
   - Handles search errors gracefully

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Required packages (install via `pip install -r requirement.txt`):
  - beautifulsoup4
  - requests
  - googlesearch-python

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

1. Edit `config.py` with your search keywords:
   ```python
   SEARCH_KEYWORDS = [
       "your search keyword 1",
       "your search keyword 2"
       # Add more keywords as needed
   ]
   ```

2. For email functionality, configure your SMTP settings:
   ```python
   EMAIL_CONFIG = {
       "smtp_server": "smtp.gmail.com",  # Your SMTP server
       "smtp_port": 587,                 # Typically 587 for TLS
       "username": "your-email@gmail.com",
       "password": "your-app-specific-password"  # Use app-specific password for Gmail
   }
   ```

## Usage

### Scraping Contacts:
```bash
python main.py
```
This will:
1. Search for contacts based on keywords in `config.py`
2. Extract contact information from search results
3. Save unique contacts to `data/contacts.csv`

### Sending Emails:
```bash
python email_sender.py
```
Options:
- `--csv`: Specify alternate CSV file (default: data/contacts.csv)
- `--subject`: Custom email subject
- `--template`: Path to email template file
- `--delay`: Seconds between emails (default: 5)
- `--test`: Test mode (prints emails without sending)
- `--self-test`: Send test email to yourself

## Data Structure

The scraped data is saved in `data/contacts.csv` with columns:
- Name: Full name (when detected)
- Email: Email address
- Phone: Phone number (when available)
- Title/Role: Professional role (when detected)
- Source URL: Website where contact was found
- Status: "Pending" or "Sent"

## Scraping Methodology

1. **Search Execution**:
   - Uses Google search with specified keywords
   - Collects top 100 results per keyword
   - Removes duplicate URLs

2. **Contact Extraction**:
   - Downloads page content with random user agents
   - Extracts emails using regex pattern matching
   - Looks for names near email addresses
   - Identifies common professional roles
   - Extracts phone numbers in various formats

3. **Data Processing**:
   - Deduplicates by email address
   - Preserves source information
   - Tracks sending status

## Email Sending Best Practices

1. **Template Personalization**:
   - Uses `[ROLE]` placeholder that gets replaced with contact's title
   - Automatically addresses contacts by name when available
   - Supports custom templates via `--template` option

2. **Rate Limiting**:
   - Maximum 450 emails per run
   - Configurable delay between sends (default: 5 seconds)
   - Status tracking prevents duplicate sends

3. **Testing**:
   - Always test with `--self-test` first
   - Use `--test` mode to preview emails
   - Start with small batches

## Important Notes

1. **Legal Considerations**:
   - Respect website terms of service and robots.txt
   - Use appropriate delays between requests (5+ seconds recommended)
   - Only scrape publicly available information

2. **Email Best Practices**:
   - For Gmail, use App Passwords instead of account password
   - Keep your email credentials secure
   - Comply with anti-spam regulations (CAN-SPAM, GDPR)

3. **Performance Tips**:
   - Narrow your search keywords for better results
   - Monitor your success rate and adjust delays as needed
   - Consider using proxies if you experience blocking

## Troubleshooting

### Common Issues:

1. **No contacts found**:
   - Try different/more specific keywords
   - Check if you're being rate-limited by Google
   - Verify your internet connection

2. **SMTP authentication errors**:
   - For Gmail: enable 2FA and use App Password
   - Verify SMTP server/port settings
   - Check firewall/antivirus settings

3. **Blocked by websites**:
   - Increase delays between requests
   - Rotate user agents more frequently
   - Consider using proxies

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details.

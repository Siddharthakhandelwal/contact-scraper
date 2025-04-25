# email_scraper.py

import requests
import re
import random
from bs4 import BeautifulSoup
#
# List of real browser user agents to bypass 403 errors
HEADERS_LIST = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
    },
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    },
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/117 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    },
]

# Roles to look for near emails
ROLES = ["Professor", "Researcher", "Recruiter", "Engineer", "Scientist", "Coordinator", "Lecturer", "Internship Coordinator", "Hiring Manager"]

def extract_info_from_url(url):
    headers = random.choice(HEADERS_LIST)
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator=' ')
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return []

    # Extract emails and phone numbers
    emails = list(set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)))
    phones = list(set(re.findall(r"(\+?\d{1,3}[\s-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}", text)))

    people_info = []

    for email in emails:
        # Search around email for context
        index = text.find(email)
        snippet = text[max(0, index - 100):index + 100]

        # Try to detect a name (capitalized first + last)
        name_match = re.search(r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)", snippet)
        name = name_match.group(0) if name_match else ""

        # Try to find job title or role
        role = next((r for r in ROLES if r.lower() in snippet.lower()), "")

        people_info.append({
            "Name": name,
            "Email": email,
            "Phone": phones[0] if phones else "",
            "Title/Role": role,
            "Source URL": url
        })

    return people_info

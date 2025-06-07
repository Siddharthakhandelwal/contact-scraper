import requests
import re
import random
import time
from bs4 import BeautifulSoup

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

# Expanded roles to improve extraction accuracy
ROLES = [
    # Real Estate
    "Realtor", "Real Estate Agent", "Real Estate Broker", "Real Estate Investor", "Property Manager",
    "Real Estate Developer", "Mortgage Broker", "Loan Officer", "Mortgage Insurance Agent", "Title Agent",
    "Real Estate Attorney", "Appraiser", "Home Inspector", "Escrow Officer", "Commercial Real Estate Agent",
    "Luxury Real Estate Agent", "Real Estate Photographer", "Real Estate Videographer", "Real Estate Coach",
    "Real Estate Mentor", "Real Estate Syndicator", "Short-Term Rental Manager", "Airbnb Manager",
    "Real Estate Influencer",

    # Mixed Niches
    "Startup Founder", "Entrepreneur", "Business Coach", "Podcast Host", "YouTuber", "Content Creator",
    "Influencer", "Health Coach", "Fitness Trainer", "Nutritionist", "Life Coach", "Public Speaker",
    "Author", "Course Creator", "Digital Marketer", "Marketing Consultant", "Consultant",
    "Personal Brand Strategist", "E-commerce Business Owner", "Dropshipping Expert", "Shopify Store Owner",
    "Angel Investor", "Venture Capitalist",

    # Banking & Finance
    "Private Banker", "Wealth Manager", "Financial Advisor", "Investment Banker", "Credit Analyst",
    "Bank Branch Manager", "Commercial Banker", "Retail Banker", "Fintech Founder", "Fintech Executive",
    "Hedge Fund Manager", "Risk Management Consultant", "Insurance Agent", "Treasury Analyst",
    "Corporate Finance Consultant", "Estate Planner", "Tax Consultant", "Financial Planner",
    "CFA", "CPA", "Finance Coach"
]


def extract_info_from_url(url, retries=3, delay=2):
    for attempt in range(retries):
        headers = random.choice(HEADERS_LIST)
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text(separator=' ')
            break  # successful fetch
        except Exception as e:
            print(f"❌ Error fetching {url}: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
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

    time.sleep(random.uniform(1.5, 3.5))  # polite delay between requests
    return people_info

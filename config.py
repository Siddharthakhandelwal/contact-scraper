# config.py - Configuration settings for contact scraper

# Email credentials
SENDER_EMAIL = "your_email@example.com"  # Replace with your email
SENDER_PASSWORD = "your_app_password"    # Replace with your app password

# Email sending settings
DAILY_EMAIL_LIMIT = 450  # Max emails per day
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Groq API settings
GROQ_API_KEY = "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"  # Replace with your Groq API key
GROQ_MODEL = "llama-3.1-8b-instant"  # Default model for email generation

# Target people/domains and their search keywords
DOMAIN_KEYWORDS = {
    "real_estate": [
        "Realtor", "Real Estate Agent", "Real Estate Broker", "Real Estate Investor",
        "Property Manager", "Real Estate Developer", "Mortgage Broker", "Loan Officer",
        "Mortgage Insurance Agent", "Title Agent", "Real Estate Attorney", "Home Inspector",
        "Appraiser", "Escrow Officer", "Commercial Real Estate", "Luxury Real Estate",
        "Real Estate Photographer", "Real Estate Videographer", "Airbnb Manager",
        "Real Estate Coach", "Real Estate Mentor", "Real Estate Syndicator",
        "Real Estate Influencer", "Short-Term Rental Manager"
    ],
    "mixed_niches": [
        "Startup Founder", "Entrepreneur", "Business Coach", "Podcast Host",
        "YouTuber", "Content Creator", "Influencer", "Health Coach", "Fitness Trainer",
        "Nutritionist", "Life Coach", "Public Speaker", "Author", "Course Creator",
        "Digital Marketer", "Marketing Consultant", "Consultant", "Personal Brand Strategist",
        "E-commerce Business Owner", "Dropshipping Expert", "Shopify Store Owner",
        "Angel Investor", "Venture Capitalist"
    ],
    "banking": [
        "Private Banker", "Wealth Manager", "Financial Advisor", "Investment Banker",
        "Loan Officer", "Credit Analyst", "Mortgage Broker", "Bank Branch Manager",
        "Commercial Banker", "Retail Banker", "Fintech Founder", "Fintech Executive",
        "Hedge Fund Manager", "Risk Management Consultant", "Insurance Agent",
        "Treasury Analyst", "Corporate Finance Consultant", "Estate Planner",
        "Tax Consultant", "Financial Planner", "CFA", "CPA", "Finance Coach"
    ]
}

# Additional keywords for broader searches
DEFAULT_KEYWORDS = [
    "professional contact information",
    "business email addresses",
    "industry contacts",
    "networking contacts"
]

def get_keywords_for_domain(domain):
    """Get appropriate search keywords based on target category"""
    # For this version, we'll return all keywords since we're targeting specific people types
    # regardless of domain. Can be enhanced later for domain-specific filtering.
    all_keywords = []
    for category in DOMAIN_KEYWORDS.values():
        all_keywords.extend(category)
    return list(set(all_keywords))  # Remove duplicates

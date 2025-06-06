import csv
import os
from scraper.search_engine import run_queries
from scraper.email_scraper import extract_info_from_url

# Function to read existing contacts to avoid duplicates
def get_existing_contacts(csv_path):
    existing_contacts = set()
    if os.path.exists(csv_path):
        with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Use email as unique identifier
                if row.get("Email"):
                    existing_contacts.add(row["Email"])
    return existing_contacts

def extract_domain(email):
    """Extract domain from email address"""
    return email.split('@')[-1].lower() if '@' in email else ''

csv_file = "data/contacts.csv"

# Get existing contacts
existing_contacts = get_existing_contacts(csv_file)
print(f"Found {len(existing_contacts)} existing contacts.")

# Scrape new contacts
all_people_info = []
domains_to_search = set()

# First pass: Collect unique domains from existing contacts
if os.path.exists(csv_file):
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('domain'):
                domains_to_search.add(row['domain'])

# Search for each domain
for domain in domains_to_search:
    print(f"\n🔍 Searching for domain: {domain}")
    urls = run_queries(domain)
    print(f"Found {len(urls)} URLs for {domain}")
    for url in urls:
        people = extract_info_from_url(url)
        for person in people:
            if person["Email"] and person["Email"] not in existing_contacts:
                all_people_info.append(person)
                existing_contacts.add(person["Email"])

# Also search with default keywords for new domains
print("\n🔍 Searching with default keywords")
urls = run_queries()
print(f"Found {len(urls)} URLs from default search")
for url in urls:
    people = extract_info_from_url(url)
    for person in people:
        if person["Email"] and person["Email"] not in existing_contacts:
            all_people_info.append(person)
            existing_contacts.add(person["Email"])

# Append new contacts to CSV if file exists, otherwise create new file
fieldnames = ["Name", "Email", "Phone", "Title/Role", "Source URL", "mail_sent", "domain"]
mode = 'a' if os.path.exists(csv_file) else 'w'
with open(csv_file, mode=mode, newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    if mode == 'w':  # Only write header for new files
        writer.writeheader()
    
    # Add domain and mail_sent status
    for contact in all_people_info:
        contact['domain'] = extract_domain(contact['Email'])
        contact['mail_sent'] = ''
        writer.writerow(contact)

print(f"\n✅ Added {len(all_people_info)} new contact(s) to {csv_file}")
print("Scraping process completed. Use email_sender.py to send emails.")

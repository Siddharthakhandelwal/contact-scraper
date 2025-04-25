
#
import csv
import os
from config import SEARCH_KEYWORDS
from scraper.search_engine import get_search_results
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

all_people_info = []
csv_file = "data/contacts.csv"

# Get existing contacts
existing_contacts = get_existing_contacts(csv_file)
print(f"Found {len(existing_contacts)} existing contacts.")

for keyword in SEARCH_KEYWORDS:
    print(f"\n🔍 Searching for: {keyword}")
    urls = get_search_results(keyword)
    print(f"Found {len(urls)} URLs.")
    for url in urls:
        people = extract_info_from_url(url)
        # Only add new contacts that don't exist in the CSV already
        for person in people:
            if person["Email"] and person["Email"] not in existing_contacts:
                all_people_info.append(person)
                existing_contacts.add(person["Email"])  # Add to set to avoid duplicates in current run

# Append new contacts to CSV if file exists, otherwise create new file
mode = 'a' if os.path.exists(csv_file) else 'w'
with open(csv_file, mode=mode, newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Name", "Email", "Phone", "Title/Role", "Source URL"])
    if mode == 'w':  # Only write header for new files
        writer.writeheader()
    writer.writerows(all_people_info)

print(f"\n✅ Added {len(all_people_info)} new contact(s) to {csv_file}")

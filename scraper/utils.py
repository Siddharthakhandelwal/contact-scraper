# scraper/utils.py
import csv
import os

def save_contacts(filename, data):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Website", "Email"])
        writer.writerows(data)

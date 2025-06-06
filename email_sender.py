#!/usr/bin/env python
# email_sender.py

import csv
import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass
import argparse

MAX_EMAILS = 450

def load_contacts(csv_file):
    """Load contacts where status is not 'Sent'."""
    contacts = []
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = list(csv.DictReader(file))
        for row in reader:
            if row.get("Email") and row.get("Status", "").strip().lower() != "sent":
                contacts.append(row)
    return contacts

def update_status(csv_file, email):
    """Update status for a specific email to 'Sent'."""
    updated_rows = []
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        for row in reader:
            if row.get("Email") == email:
                row["Status"] = "Sent"
            updated_rows.append(row)

    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

def send_email(sender_email, sender_password, recipient, subject, body, smtp_server="smtp.gmail.com", smtp_port=587):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient['Email']
    msg['Subject'] = subject

    if recipient.get('Name'):
        personalized_body = f"Dear {recipient['Name']},\n\n{body}"
    else:
        personalized_body = f"Hello,\n\n{body}"

    if recipient.get('Title/Role'):
        personalized_body = personalized_body.replace("[ROLE]", recipient['Title/Role'])
    else:
        personalized_body = personalized_body.replace("[ROLE]", "professional")

    msg.attach(MIMEText(personalized_body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email to {recipient['Email']}: {str(e)}")
        return False

def self_test():
    print("\n=== SELF-TEST MODE ===")
    sender_email = input("Enter your email address: ")
    sender_password = getpass.getpass("Enter your email app password: ")

    recipient = {
        "Email": sender_email,
        "Name": "Siddhartha",
        "Title/Role": "Developer"
    }

    subject = "Curious how I found you?"
    email_body = "Hi,\n\nThis is a test email sent by your script. [ROLE] placeholder test."

    personalized_body = f"Dear {recipient['Name']},\n\n{email_body}".replace("[ROLE]", "Developer")

    print("\nPreview of email content:")
    print("---------------------------")
    print(personalized_body)
    print("---------------------------")

    success = send_email(sender_email, sender_password, recipient, subject, email_body)
    if success:
        print("\n✅ Test email sent successfully!")
    else:
        print("\n❌ Failed to send test email.")
    return success

def main():
    parser = argparse.ArgumentParser(description='Send emails to contacts in CSV file.')
    parser.add_argument('--csv', default='data/contacts.csv', help='Path to contacts CSV file')
    parser.add_argument('--subject', default='Curious how I found you?', help='Email subject')
    parser.add_argument('--template', help='Path to email template file')
    parser.add_argument('--delay', type=int, default=5, help='Delay between emails in seconds')
    parser.add_argument('--test', action='store_true', help='Test mode - print emails instead of sending')
    parser.add_argument('--self-test', action='store_true', help='Send a test email to yourself to verify setup')
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return

    if not os.path.exists(args.csv):
        print(f"Error: CSV file {args.csv} not found.")
        return

    contacts = load_contacts(args.csv)
    if not contacts:
        print("No unsent contacts found.")
        return

    print(f"Loaded {len(contacts)} unsent contacts from {args.csv}")

    if args.template and os.path.exists(args.template):
        with open(args.template, 'r', encoding='utf-8') as file:
            email_body = file.read()
    else:
        email_body = "Hi,\n\nI'm reaching out because I believe you might be the right [ROLE] to connect with."
        print("\nUsing default email template.")

    sender_email = input("Enter your email address: ")
    sender_password = getpass.getpass("Enter your email app password: ")

    count = 0
    for contact in contacts:
        if count >= MAX_EMAILS:
            print(f"\n✅ Reached the maximum of {MAX_EMAILS} emails. Stopping.")
            break

        if args.test:
            print(f"[TEST MODE] Would send email to: {contact['Email']}")
            continue

        print(f"\nSending email to: {contact['Email']}...")
        success = send_email(
            sender_email,
            sender_password,
            contact,
            args.subject,
            email_body
        )
        if success:
            print(f"✅ Email sent to {contact['Email']}")
            update_status(args.csv, contact["Email"])
            count += 1
        else:
            print(f"❌ Failed to send email to {contact['Email']}")

        time.sleep(args.delay)

if __name__ == "__main__":
    main()

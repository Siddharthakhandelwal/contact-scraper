#!/usr/bin/env python
# email_sender.py

import csv
import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import getpass
import argparse

def load_contacts(csv_file):
    """Load contacts from CSV file."""
    contacts = []
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("Email"):  # Only include contacts with valid emails
                contacts.append(row)
    return contacts

def send_email(sender_email, sender_password, recipient, subject, body, attachment_path=None, smtp_server="smtp.gmail.com", smtp_port=587):
    """Send an email with optional attachment."""
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient['Email']
    msg['Subject'] = subject
    
    # Personalize the email body if name is available
    personalized_body = body
    if recipient.get('Name'):
        personalized_body = f"Dear {recipient['Name']},\n\n{body}"
    else:
        personalized_body = f"Hello,\n\n{body}"
    
    # Add the role/title if available
    if recipient.get('Title/Role'):
        personalized_body = personalized_body.replace("[ROLE]", recipient['Title/Role'])
    else:
        personalized_body = personalized_body.replace("[ROLE]", "professional")
        
    # Attach body
    msg.attach(MIMEText(personalized_body, 'plain'))
    
    # Attach file if provided
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as file:
            attachment = MIMEApplication(file.read(), Name=os.path.basename(attachment_path))
            attachment['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
            msg.attach(attachment)
    
    # Send email
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

def self_test(attachment_path=None):
    """Send a test email to yourself to verify everything is working."""
    print("\n=== SELF-TEST MODE ===")
    print("This will send a test email to your own email address to verify the setup works.")
    
    # Email content
    sender_email = "siddharthakhandelwal9@gmail.com"  # Your email
    sender_password = "odgd xydu sbwi rvcv"  # Your app password
    
    # Use siddhartha_khandelwal.pdf as default attachment if none specified
    if not attachment_path:
        default_attachment = "siddhartha_khandelwal.pdf"
        if os.path.exists(default_attachment):
            attachment_path = default_attachment
            print(f"Using default attachment: {default_attachment}")
        else:
            print(f"Default attachment {default_attachment} not found.")
    
    recipient = {
        "Email": sender_email,
        "Name": "Siddhartha",
        "Title/Role": "Developer"
    }
    subject = "Curious how I found you?"
    
    # Load template if it exists, otherwise use default
    if os.path.exists("email_template.txt"):
        with open("email_template.txt", 'r', encoding='utf-8') as file:
            email_body = file.read()
    else:
        email_body = """Hi,

I'm a student and recently built a small project in Python that can scrape email IDs of researchers and professors, that's actually how I reached out to you!

You can check out the project here: https://github.com/Siddharthakhandelwal/contact-scraper
Some of my other interesting repos: https://github.com/Siddharthakhandelwal

Also, here's my LinkedIn: https://www.linkedin.com/in/siddhartha-khandelwal/

I've attached my CV as well, if there's any internship opportunity available this summer, I'd be really grateful to be considered.

Thank you!
Siddhartha Khandelwal
+917300608902"""
    
    # Print preview of email
    print(f"\nSending test email to: {sender_email}")
    print("Subject: Curious how I found you?")
    print("\nPreview of email content:")
    print("---------------------------")
    personalized_body = f"Dear Siddhartha,\n\n{email_body}"
    personalized_body = personalized_body.replace("[ROLE]", "Developer")
    print(personalized_body)
    print("---------------------------")
    print(f"Attachment: {attachment_path if attachment_path else 'None'}")
    
    # Send the test email
    print("\nSending test email...")
    success = send_email(
        sender_email,
        sender_password,
        recipient,
        subject,
        email_body,
        attachment_path
    )
    
    if success:
        print("\n✅ Test email sent successfully to your email address!")
        print("Check your inbox to verify it was received correctly.")
    else:
        print("\n❌ Failed to send test email. Please check your app password and try again.")
    
    return success

def main():
    parser = argparse.ArgumentParser(description='Send emails to contacts in CSV file.')
    parser.add_argument('--csv', default='data/contacts.csv', help='Path to contacts CSV file')
    parser.add_argument('--attachment', default='siddhartha_khandelwal.pdf', help='Path to file attachment')
    parser.add_argument('--subject', default='Curious how I found you?', help='Email subject')
    parser.add_argument('--template', help='Path to email template file')
    parser.add_argument('--delay', type=int, default=5, help='Delay between emails in seconds')
    parser.add_argument('--limit', type=int, help='Limit number of emails to send')
    parser.add_argument('--test', action='store_true', help='Test mode - print emails instead of sending')
    parser.add_argument('--self-test', action='store_true', help='Send a test email to yourself to verify setup')
    args = parser.parse_args()

    # Run self-test if requested
    if args.self_test:
        self_test(args.attachment)
        return

    # Check if CSV file exists
    if not os.path.exists(args.csv):
        print(f"Error: CSV file {args.csv} not found.")
        return

    # Load contacts
    contacts = load_contacts(args.csv)
    if not contacts:
        print("No valid contacts found in CSV.")
        return
    
    print(f"Loaded {len(contacts)} contacts from {args.csv}")
    
    # Get email template
    if args.template and os.path.exists(args.template):
        with open(args.template, 'r', encoding='utf-8') as file:
            email_body = file.read()
    else:
        # Default template without indentation
        email_body = """Hi,

I'm a student and recently built a small project in Python that can scrape email IDs of researchers and professors, that's actually how I reached out to you!

You can check out the project here: https://github.com/Siddharthakhandelwal/contact-scraper
Some of my other interesting repos: https://github.com/Siddharthakhandelwal

Also, here's my LinkedIn: https://www.linkedin.com/in/siddhartha-khandelwal/

I've attached my CV as well, if there's any internship opportunity available this summer, I'd be really grateful to be considered.

Thank you!
Siddhartha Khandelwal
+917300608902"""
        print("\nUsing default email template. Create a text file with your template for better results.")
        print("Template placeholders: [ROLE] will be replaced with the recipient's role.\n")

    # Get sender credentials
    sender_email = "siddharthakhandelwal9@gmail.com"
    sender_password = "odgd xydu sbwi rvcv"
    
    # Ask for confirmation before sending
    limit_text = f"first {args.limit}" if args.limit else "all"
    if args.test:
        print(f"\nTEST MODE: Will print emails to the {limit_text} contacts instead of sending.")
    else:
        confirm = input(f"\nReady to send emails to the {limit_text} contacts with a {args.delay}s delay between each. Proceed? (y/n): ")
        if confirm.lower() != 'y':
            print("Operation cancelled.")
            return
    
    # Process contacts
    successful = 0
    total_to_process = min(len(contacts), args.limit) if args.limit else len(contacts)
    
    for i, contact in enumerate(contacts[:args.limit] if args.limit else contacts):
        print(f"\nProcessing {i+1}/{total_to_process}: {contact.get('Name', 'Unknown')} <{contact['Email']}>")
        
        if args.test:
            # Print the email instead of sending in test mode
            print(f"\nSubject: {args.subject}")
            personalized_body = email_body
            if contact.get('Name'):
                personalized_body = f"Dear {contact['Name']},\n\n{email_body}"
            else:
                personalized_body = f"Hello,\n\n{email_body}"
                
            if contact.get('Title/Role'):
                personalized_body = personalized_body.replace("[ROLE]", contact['Title/Role'])
            else:
                personalized_body = personalized_body.replace("[ROLE]", "professional")
                
            print(f"\nBody:\n{personalized_body}")
            print(f"\nAttachment: {args.attachment if args.attachment else 'None'}")
            successful += 1
        else:
            # Actually send the email
            success = send_email(
                sender_email, 
                sender_password, 
                contact, 
                args.subject, 
                email_body, 
                args.attachment
            )
            if success:
                successful += 1
                print(f"Email sent successfully to {contact['Email']}")
            else:
                print(f"Failed to send email to {contact['Email']}")
        
        # Delay between emails (if not the last contact)
        if i < total_to_process - 1 and not args.test:
            print(f"Waiting {args.delay} seconds before sending next email...")
            time.sleep(args.delay)
    
    print(f"\nComplete: {successful} of {total_to_process} emails {'generated' if args.test else 'sent'} successfully.")

if __name__ == "__main__":
    main() 
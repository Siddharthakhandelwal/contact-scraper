import csv
import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import getpass
import argparse
try:
    from groq import Groq
except ImportError:
    Groq = None
from config import GROQ_API_KEY, GROQ_MODEL

def load_contacts(csv_file):
    """Load contacts from CSV file."""
    contacts = []
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row.get("Email"):  # Only include contacts with valid emails
                contacts.append(row)
    return contacts

def generate_groq_email(contact, template=None):
    """Generate email content using Groq API"""
    if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key":
        raise ValueError("Groq API key not configured")
    
    client = Groq(api_key=GROQ_API_KEY)
    prompt = f"""Generate a professional email to {contact.get('Name', 'them')},
    a {contact.get('Title/Role', 'professional')}. Keep it concise (3 paragraphs max)."""
    
    if template:
        prompt += f"\n\nTemplate:\n{template}"
    
    completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=GROQ_MODEL,
        temperature=0.7
    )
    return completion.choices[0].message.content

def generate_email_content(contact, template=None, use_groq=True):
    """Generate email content - uses Groq by default or falls back to template"""
    if use_groq:
        try:
            return generate_groq_email(contact, template)
        except Exception as e:
            print(f"Groq error: {e}. Falling back to template.")
    
    return template or f"""Hi {contact.get('Name', 'there')},

I came across your profile and wanted to connect regarding your work as a {contact.get('Title/Role', 'professional')}.

Best regards,
[Your Name]"""

def update_contact_status(csv_file, contact):
    """Update mail_sent status for a contact in the CSV file."""
    # Read all contacts
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        rows = list(reader)
    
    # Find and update the contact
    for row in rows:
        if row['Email'] == contact['Email']:
            row['mail_sent'] = 'true'
            break
    
    # Write back to file
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def send_email(sender_email, sender_password, recipient, subject, body, smtp_server="smtp.gmail.com", smtp_port=587):
    """Send an email immediately without delay"""
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient['Email']
    msg['Subject'] = subject
    
    # Personalize greeting
    greeting = f"Dear {recipient['Name']},\n\n" if recipient.get('Name') else "Hello,\n\n"
    msg.attach(MIMEText(greeting + body, 'plain'))
    
    # Uncomment below to enable attachments
    """
    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as file:
            part = MIMEApplication(file.read(), Name=os.path.basename(attachment_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
            msg.attach(part)
    """
    
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
    
    # Email content from config with error handling
    try:
        from config import SENDER_EMAIL, SENDER_PASSWORD
        if not SENDER_EMAIL or SENDER_EMAIL == "your_email@example.com":
            raise ValueError("Please configure SENDER_EMAIL in config.py")
        if not SENDER_PASSWORD or SENDER_PASSWORD == "your_app_password":
            raise ValueError("Please configure SENDER_PASSWORD in config.py")
        sender_email = SENDER_EMAIL
        sender_password = SENDER_PASSWORD
    except ImportError:
        print("Error: config.py not found. Please create it from config.example.py")
        return
    except ValueError as e:
        print(f"Configuration error: {str(e)}")
        return
    
    # Use resume.pdf as default attachment if none specified
    if not attachment_path:
        default_attachment = "resume.pdf"
        if os.path.exists(default_attachment):
            attachment_path = default_attachment
            print(f"Using default attachment: {default_attachment}")
        else:
            print(f"Default attachment {default_attachment} not found.")
    
    recipient = {
        "Email": sender_email,
        "Name": "Test User",
        "Title/Role": "Developer"
    }
    subject = "Curious how I found you?"
    
    # Load template if it exists, otherwise use default
    if os.path.exists("email_template.txt"):
        with open("email_template.txt", 'r', encoding='utf-8') as file:
            email_body = file.read()
    else:
        email_body = """Hi,

This is a test email from the automated contact system. The actual emails will be dynamically generated based on the recipient's profile and domain.

Thank you!"""
    
    # Print preview of email
    print(f"\nSending test email to: {sender_email}")
    print("Subject: Curious how I found you?")
    print("\nPreview of email content:")
    print("---------------------------")
    personalized_body = f"Dear Test User,\n\n{email_body}"
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
    # parser.add_argument('--attachment', help='Path to file attachment (commented out by default)')
    parser.add_argument('--subject', default='Opportunity to connect', help='Email subject')
    parser.add_argument('--template', help='Path to custom email template file')
    parser.add_argument('--no-groq', action='store_true', help='Disable Groq AI and use template only')
    parser.add_argument('--limit', type=int, help='Max emails to send')
    parser.add_argument('--test', action='store_true', help='Test mode - print emails without sending')
    parser.add_argument('--self-test', action='store_true', help='Send test email to yourself')
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
    template_content = None
    if args.template and os.path.exists(args.template):
        with open(args.template, 'r', encoding='utf-8') as file:
            template_content = file.read()
    
    # Generate email content (dynamic if Groq available)
    email_body = generate_email_content(contacts[0] if contacts else {}, template_content)
    if not email_body:
        # Fallback template
        email_body = """Hi,

This is an automated email from our contact system. The content will be dynamically generated based on your profile and domain.

For any inquiries, please reply to this email.

Thank you!"""
        print("\nUsing default email template. Create a text file with your template for better results.")
        print("Template placeholders: [ROLE] will be replaced with the recipient's role.\n")

    # Get sender credentials from config with error handling
    try:
        from config import SENDER_EMAIL, SENDER_PASSWORD
        if not SENDER_EMAIL or SENDER_EMAIL == "your_email@example.com":
            raise ValueError("Please configure SENDER_EMAIL in config.py")
        if not SENDER_PASSWORD or SENDER_PASSWORD == "your_app_password":
            raise ValueError("Please configure SENDER_PASSWORD in config.py")
        sender_email = SENDER_EMAIL
        sender_password = SENDER_PASSWORD
    except ImportError:
        print("Error: config.py not found. Please create it from config.example.py")
        return
    except ValueError as e:
        print(f"Configuration error: {str(e)}")
        return
    
    # Check daily limit
    daily_limit = 450
    sent_today = sum(1 for c in contacts if c.get('mail_sent', '').lower() == 'true')
    remaining = daily_limit - sent_today
    
    if remaining <= 0:
        print(f"Daily limit of {daily_limit} emails reached. Try again tomorrow.")
        return
    
    if args.limit and args.limit > remaining:
        print(f"Warning: Requested limit {args.limit} exceeds remaining daily limit {remaining}")
        args.limit = remaining
    
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
                email_body
            )
            if success:
                successful += 1
                print(f"Email sent successfully to {contact['Email']}")
                # Update mail_sent status in CSV
                contact['mail_sent'] = 'true'
                update_contact_status(args.csv, contact)
            else:
                print(f"Failed to send email to {contact['Email']}")
        
        # Delay between emails (if not the last contact)
        if i < total_to_process - 1 and not args.test:
            print(f"Waiting {args.delay} seconds before sending next email...")
            time.sleep(args.delay)
    
    print(f"\nComplete: {successful} of {total_to_process} emails {'generated' if args.test else 'sent'} successfully.")

if __name__ == "__main__":
    main()

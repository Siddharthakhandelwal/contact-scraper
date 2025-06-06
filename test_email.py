#!/usr/bin/env python
# test_email.py
# Simple script to run the self-test email function

import os
import sys

# Default PDF attachment
default_attachment = "siddhartha_khandelwal.pdf"

# Check if resume file exists
if len(sys.argv) > 1:
    attachment = sys.argv[1]
    if not os.path.exists(attachment):
        print(f"⚠️ Warning: Attachment file '{attachment}' not found.")
        response = input("Continue without attachment? (y/n): ")
        if response.lower() != 'y':
            print("Exiting...")
            sys.exit(1)
else:
    # Use the default attachment if it exists
    if os.path.exists(default_attachment):
        attachment = default_attachment
        print(f"Using default attachment: {default_attachment}")
    else:
        print(f"Default attachment {default_attachment} not found.")
        attachment = None

# Run the self-test command
command = f"python email_sender.py --self-test"
if attachment:
    command += f" --attachment {attachment}"

print(f"\nRunning: {command}")
os.system(command) 
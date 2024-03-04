import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Email configuration
sender_email = ''
sender_name = 'Nick'
password = ''

# File to be attached
attachment_file = '.pdf'  # Change this to the name of your attachment file

# Read CSV file with recipient information (assuming 'emails.csv' has columns: Name, Email)
with open('.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        receiver_name = row['Name']
        receiver_email = row['Email']

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['From'] = f'{sender_name} <{sender_email}'
        msg['To'] = receiver_email
        msg['Subject'] = ''

        # Customize the email body with the recipient's name
        text = f"""Good Afternoon {receiver_name},"""

        # Attach the HTML version of the message to the email.
        part1 = MIMEText(text, 'html')
        msg.attach(part1)

        # Attaching the file
        attachment = open(attachment_file, 'rb')
        part2 = MIMEBase('application', 'octet-stream')
        part2.set_payload(attachment.read())
        encoders.encode_base64(part2)
        part2.add_header('Content-Disposition', f"attachment; filename= {attachment_file}")
        msg.attach(part2)

        # Create a secure SSL context and send the email
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print(f"Email sent successfully to {receiver_name}!")
        except Exception as e:
            print(f"Error sending email to {receiver_name}: {e}")
        finally:
            server.quit()
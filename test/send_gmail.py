import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(sender_email, sender_password, recipient_email, subject, body):
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Set up the server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection

        # Login to your Gmail account
        server.login(sender_email, sender_password)

        # Send the email
        server.send_message(msg)
        print('Email sent successfully!')
    except Exception as e:
        print(f'Error occurred: {e}')
    finally:
        # Terminate the SMTP session
        server.quit()


# Example usage
if __name__ == '__main__':
    sender_email = 'leave@aumanimation.com'
    sender_password = 'app pass'  # Use App Password if 2FA is enabled
    recipient_email = 'sanath.shetty@aumanimation.com'
    subject = 'Test Email'
    body = 'This is a test email sent from Python!'

    send_email(sender_email, sender_password, recipient_email, subject, body)
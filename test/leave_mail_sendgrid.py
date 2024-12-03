import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email='sanath.shetty@aumanimation.com',
    to_emails='sanaths645@gmail.com',
    subject='Sent from Twilio SendGrid',
    html_content='<strong>Sent using Python</strong>')
try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e)


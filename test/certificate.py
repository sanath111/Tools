import os
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

certs_dir = "/home/sanath/Pictures/certificates/"
output_dir = os.path.join(certs_dir, 'output_certificates_HM_2')
data_file = os.path.join(certs_dir, 'names.xlsx')
template = os.path.join(certs_dir, 'certificate_HM.png')
font_path = os.path.join(certs_dir, 'Radley-Regular.ttf')

data = pd.read_excel(data_file)[['NAME', 'E-MAIL']]
name_email_dict = dict(zip(data['NAME'], data['E-MAIL']))

font_size = 100
font = ImageFont.truetype(font_path, font_size)

smtp_server = 'smtp.gmail.com'
smtp_port = 587
username = 'totgvs@gmail.com'
app_password = 'wljp heiq lzbn ngta '

from_addr = username
# to_addr = 'recipient@example.com'
subject = 'e-certificate'
body = ('Dear Sir, Madam\n\n'
        'Thanks for being a part of the training program "Learning made easy with positive energy", We hope that you will continue the practices which was taught to you and be able to get 100% results in your school.\n\n'
        'If you want us to do training at your school please contact Mr Madhav Bhandari +91 90084 99981\n\n'
        'If there is any suggestions/ correction please reply back to this mail id\n\n'
        'Thanks\n'
        'Team GVS &UK')

def generate_certificates(name):
    print(name)
    if name:
        image = Image.open(template)
        draw = ImageDraw.Draw(image)

        text_width = draw.textlength(name, font=font)
        text_height = font.getbbox(name)[3]
        image_width, image_height = image.size

        x = (image_width - text_width) // 2
        y = 1130

        draw.text((x, y), name, font=font, fill='black')
        output_image = f'{output_dir}/{name}.png'
        image.save(output_image)
        print(f"Certificates generated successfully! {output_image}")
        return output_image


def send_mail(mail_id, output_image):
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = mail_id
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    image_path = output_image
    with open(image_path, 'rb') as img:
        img_attachment = MIMEImage(img.read(), name=image_path.split('/')[-1])
        msg.attach(img_attachment)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, app_password)
            server.send_message(msg)
        print(f"Email sent successfully! {mail_id}")
    except Exception as e:
        print(f"Failed to send email: {e}")

for name, email in name_email_dict.items():
    output_image = generate_certificates(name)
    send_mail(email, output_image)

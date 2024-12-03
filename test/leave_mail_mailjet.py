from mailjet_rest import Client
import os
api_key = '3f8a6c6bd0afe4e056c370605c23273e'
api_secret = 'f27d9d14a1945b506db35089ffa5c7cc'
mailjet = Client(auth=(api_key, api_secret), version='v3.1')
data = {
  'Messages': [
    {
      "From": {
        "Email": "sanath.shetty@aumanimation.com",
        "Name": "Sanath Shetty"
      },
      "To": [
        {
          "Email": "sanaths645@gmail.com",
          "Name": "Sanath Shetty"
        }
      ],
      "Subject": "Sent from Mailjet.",
      "TextPart": "Mailjet test email",
      "HTMLPart": "<h3>Success!</h3><br />May the delivery force be with you!",
      "CustomID": "TestMail"
    }
  ]
}
result = mailjet.send.create(data=data)
print (result.status_code)
print (result.json())


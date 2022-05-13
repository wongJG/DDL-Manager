import smtplib, ssl, email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sentCode(receiver_email, confirmation_code):

    sender_email = "amandapaulson2021@gmail.com"
    password = "rogdoz-xurris-vySzi8"

    #Create MIMEMultipart object
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "DDL-Manager: Confirm your Registration"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    # filename = "document.pdf"

    #HTML Message Part
    html = """
    <html>
    <body>
        <p>Hi,<br>
        Welcome to DDL-Manager<br>
        Your verification code is %s. Have fun!
        </p>
    </body>
    </html>
    """ % (confirmation_code)

    part = MIMEText(html, "html")
    msg.attach(part)

    # Create secure SMTP connection and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, msg.as_string()
        )
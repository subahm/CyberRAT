import smtplib, ssl

from email.encoders import encode_base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

import pdfkit

import os


class EmailService:
    __instance = None

    server = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if EmailService.__instance == None:
            EmailService()
        return EmailService.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if EmailService.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            EmailService.__instance = self

        port = 465  # For SSL
        password = "Tj~M8%M^kH"

        # Create a secure SSL context
        context = ssl.create_default_context()
        self.server = smtplib.SMTP_SSL("smtp.gmail.com", port, context=context)
        self.server.login("cyberratresults@gmail.com", password)

    def __del__(self):
        self.server.quit()

    def send_results(self, request, uuid, email_address, site_html):
        sender_email = "cyberratresults@gmail.com"
        receiver_email = email_address

        message = MIMEMultipart("alternative")
        message["Subject"] = "CyberRAT Results"
        message["From"] = sender_email
        message["To"] = receiver_email

        # add text to email
        text = """\
        Hello,
        Here are the results from scan with CyberRAT
        """

        site_url = request.build_absolute_uri('/results/')
        site_url = site_url + uuid
        text = text + site_url

        part1 = MIMEText(text, "plain")
        message.attach(part1)

        # add pdf to email
        # must install from https://wkhtmltopdf.org/downloads.html for respective os to generate pdfs
        pdf_location = "Resources/EmailHub/cyber_rat_results-" + uuid + ".pdf"

        pdfkit.from_string(site_html, pdf_location)



        with open(pdf_location, "rb") as opened:
            openedfile = opened.read()
        attachedfile = MIMEApplication(openedfile, _subtype="pdf", _encoder=encode_base64)
        attachedfile.add_header('content-disposition', 'attachment', filename="cyber_rat_results.pdf")
        message.attach(attachedfile)

        self.server.sendmail(sender_email, receiver_email, message.as_string())
        os.remove(pdf_location)
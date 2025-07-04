import smtplib
import sys
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.template.loader import render_to_string
from core.user.models import User

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings


def send_email():
    try:
        mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        print(mailServer.ehlo())
        mailServer.starttls()
        print(mailServer.ehlo())
        mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        print("Conexión exitosa")

        email_to = "bramose@fcpn.edu.bo"
        # Construimos el mensaje simple
        mensaje = MIMEMultipart()
        mensaje["From"] = settings.EMAIL_HOST_USER
        mensaje["To"] = email_to
        mensaje["Subject"] = "Prueba de envío de correo"
        content = render_to_string("send_email.html", {"user": User.objects.get(pk=1)})
        mensaje.attach(MIMEText(content, "html"))
        mailServer.sendmail(settings.EMAIL_HOST_USER, email_to, mensaje.as_string())
        print("Correo enviado exitosamente")
    except Exception as e:
        print(e)


send_email()

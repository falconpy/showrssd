# Importamos smtplib
import smtplib
 
# Importamos los modulos necesarios
from email.mime.text import MIMEText

def send_mail(user, pwd, to_who, subjet, message):
    # Creamos el mensaje
    msg = MIMEText(message)
 
    # Conexion con el server
    msg['Subject'] = subjet
    msg['From'] = user
    msg['To'] = to_who
 
    # Autenticamos
    mailServer = smtplib.SMTP('smtp.gmail.com',587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(user,pwd)
 
    # Enviamos

    mailServer.sendmail(user, to_who, msg.as_string())
 
    # Cerramos conexion
    mailServer.close()

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(smtp_server, smtp_port, sender_email, sender_password, receiver_email, subject, body, use_ssl):
    try:
        # Création du message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        # Ajout du corps du message
        message.attach(MIMEText(body, "plain"))

        # Choix de la classe SMTP en fonction de l'utilisation de SSL
        if use_ssl:
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)  # Utilisation de SMTP_SSL pour une connexion SSL
        else:
            server = smtplib.SMTP(smtp_server, smtp_port)

        # Connexion au serveur SMTP
        server.starttls()  # Démarrage de la connexion TLS
        server.login(sender_email, sender_password)  # Connexion au serveur avec les identifiants

        # Envoi du message
        server.sendmail(sender_email, receiver_email, message.as_string())

        # Fermeture de la connexion SMTP
        server.quit()
        print("L'e-mail a été envoyé avec succès !")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")

# Informations SMTP
smtp_server = "mail.example.bj"  # Modifier avec votre serveur SMTP par défaut
smtp_port = 587  # Modifier avec votre port SMTP par défaut
sender_email = "admin@example.bj"  # Modifier avec votre adresse e-mail par défaut
sender_password = "s3curpassw0rd"  # Modifier avec votre mot de passe par défaut
receiver_email = "receveirfortest@gmail.com"  # Modifier avec l'adresse e-mail du destinataire par défaut
use_ssl = True  # Modifier à True si votre serveur SMTP nécessite SSL

# Contenu de l'e-mail
subject = "Sujet de test 1"
body = "je suis en train de faire un test"

# Vérification des valeurs par défaut
if smtp_server == "your_smtp_server" or sender_email == "your_email@example.com" or sender_password == "your_password" or receiver_email == "recipient@example.com":
    # Demander à l'utilisateur de fournir les informations manquantes
    smtp_server = input("Entrez le serveur SMTP : ")
    smtp_port = int(input("Entrez le port SMTP (par défaut : 587) : ") or 587)
    sender_email = input("Entrez votre adresse e-mail : ")
    sender_password = input("Entrez votre mot de passe : ")
    receiver_email = input("Entrez l'adresse e-mail du destinataire : ")
    subject = input("Entrez le sujet du message : ")
    body = input("Entrez le corps du message : ")
    use_ssl = input("Utiliser SSL (True/False) : ").lower() == "true"

# Envoi de l'e-mail
send_email(smtp_server, smtp_port, sender_email, sender_password, receiver_email, subject, body, use_ssl)

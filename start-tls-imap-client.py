import imaplib
import email
from email.header import decode_header
import getpass

# Détails de connexion à entrer par l'utilisateur
IMAP_SERVER = 'mail.example.com'
IMAP_PORT = 143

def connect_to_imap_server(email_account, password):
    try:
        mail = imaplib.IMAP4(IMAP_SERVER, IMAP_PORT)
        mail.starttls()
        mail.login(email_account, password)
        print("Connexion réussie au serveur IMAP.")
        return mail
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return None

def list_mailboxes(mail):
    status, mailboxes = mail.list()
    if status == 'OK':
        print("Boîtes aux lettres disponibles :")
        for mailbox in mailboxes:
            print(mailbox.decode())
    else:
        print("Impossible de lister les boîtes aux lettres.")

def fetch_emails(mail, mailbox="inbox"):
    mail.select(mailbox)
    status, messages = mail.search(None, "ALL")

    if status != "OK":
        print("Erreur lors de la recherche d'emails.")
        return []

    email_ids = messages[0].split()
    emails = []

    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        if status != "OK":
            print(f"Erreur lors de la récupération de l'email ID {email_id}.")
            continue

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                emails.append((email_id, subject, msg))
    
    return emails

def print_email(email_data):
    email_id, subject, msg = email_data
    print(f"Sujet: {subject}")
    print("De:", msg.get("From"))
    print("À:", msg.get("To"))

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            try:
                body = part.get_payload(decode=True).decode()
            except:
                pass

            if content_type == "text/plain" and "attachment" not in content_disposition:
                print("Corps du message:")
                print(body)
                break
    else:
        content_type = msg.get_content_type()
        body = msg.get_payload(decode=True).decode()
        if content_type == "text/plain":
            print("Corps du message:")
            print(body)
    print("="*50)

def main_menu(mail):
    while True:
        print("\nMenu Principal:")
        print("1. Lister les boîtes aux lettres")
        print("2. Lister les emails dans la boîte de réception")
        print("3. Lire un email")
        print("4. Quitter")

        choice = input("Entrez votre choix: ")
        if choice == '1':
            list_mailboxes(mail)
        elif choice == '2':
            emails = fetch_emails(mail)
            for idx, (email_id, subject, msg) in enumerate(emails):
                print(f"{idx+1}. {subject}")
        elif choice == '3':
            email_index = int(input("Entrez le numéro de l'email à lire: ")) - 1
            emails = fetch_emails(mail)
            if 0 <= email_index < len(emails):
                print_email(emails[email_index])
            else:
                print("Numéro d'email invalide.")
        elif choice == '4':
            print("Déconnexion et sortie...")
            mail.logout()
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    email_account = input("Entrez votre adresse email: ")
    password = getpass.getpass("Entrez votre mot de passe: ")

    mail = connect_to_imap_server(email_account, password)
    if mail:
        main_menu(mail)

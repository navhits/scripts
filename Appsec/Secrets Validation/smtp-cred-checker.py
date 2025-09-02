import os
import smtplib
import ssl
import socket
from getpass import getpass

def test_smtp_connection(smtp_server, smtp_port, username, password, use_ssl):
    try:
        if use_ssl:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
                server.login(username, password)
                print("SMTP SSL connection successful. Credentials are valid.")
        else:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.ehlo()
                server.starttls(context=ssl.create_default_context())
                server.ehlo()
                server.login(username, password)
                print("SMTP TLS connection successful. Credentials are valid.")
    except smtplib.SMTPAuthenticationError:
        print("Authentication failed: Invalid username or password.")
    except smtplib.SMTPConnectError:
        print(f"Connection failed: Unable to connect to {smtp_server} on port {smtp_port}.")
    except smtplib.SMTPServerDisconnected:
        print("Connection lost: The server unexpectedly disconnected.")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except socket.gaierror:
        print("Network error: Unable to resolve the SMTP server address.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    smtp_server = input("Enter SMTP server address (e.g., smtp.gmail.com): ")

    try:
        smtp_port = int(input("Enter SMTP port (e.g., 587 for TLS or 465 for SSL): "))
        if smtp_port not in range(1, 65536):
            raise ValueError
    except ValueError:
        print("Invalid port number. Please enter a number between 1 and 65535.")
        return

    username = input("Enter your email username (e.g., your_email@example.com): ")

    # Retrieve password from environment variable or prompt the user securely
    password = os.getenv('EMAIL_PASSWORD') or getpass("Enter your email password: ")

    use_ssl = smtp_port == 465

    # Optional: Enable debugging output
    debug = input("Enable debug output? (yes/no): ").strip().lower() == 'yes'
    if debug:
        smtplib.SMTP.debuglevel = 1

    test_smtp_connection(smtp_server, smtp_port, username, password, use_ssl)

if __name__ == "__main__":
    main()

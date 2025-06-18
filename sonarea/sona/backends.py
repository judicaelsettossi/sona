from django.core.mail.backends.smtp import EmailBackend as SMTPBackend
from django.conf import settings
import ssl
import smtplib
import time
import logging
from socket import error as socket_error
from smtplib import SMTPException, SMTPAuthenticationError

logger = logging.getLogger('sona')

class CustomEmailBackend(SMTPBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        self.max_retries = getattr(settings, 'EMAIL_CONNECTION_RETRIES', 3)
        self.retry_delay = getattr(settings, 'EMAIL_RETRY_DELAY', 2)
        self.keep_alive = getattr(settings, 'EMAIL_KEEP_ALIVE', True)
        self.connection_timeout = getattr(settings, 'EMAIL_CONNECTION_TIMEOUT', 10)

    def open(self):
        if self.connection:
            try:
                # Vérifier si la connexion est toujours active
                status = self.connection.noop()[0]
                if status == 250:
                    return False
            except (smtplib.SMTPServerDisconnected, socket_error):
                self.connection = None

        for attempt in range(self.max_retries):
            try:
                connection_class = smtplib.SMTP_SSL if self.use_ssl else smtplib.SMTP
                kwargs = {
                    'timeout': self.connection_timeout,
                    'context': self.ssl_context
                }

                self.connection = connection_class(
                    self.host,
                    self.port,
                    **kwargs
                )

                if self.use_tls:
                    self.connection.starttls(context=self.ssl_context)

                if self.username and self.password:
                    self.connection.login(self.username, self.password)

                logger.info(f"Connexion SMTP établie avec succès (tentative {attempt + 1})")
                return True

            except (SMTPException, socket_error, ssl.SSLError) as e:
                logger.warning(f"Tentative {attempt + 1}/{self.max_retries} échouée : {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))  # Délai exponentiel
                    continue
                if not self.fail_silently:
                    raise
                return False

    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        new_conn_created = self.open()
        if not self.connection:
            return 0

        num_sent = 0
        for message in email_messages:
            try:
                sent = self._send(message)
                if sent:
                    num_sent += 1
            except Exception as e:
                logger.error(f"Erreur lors de l'envoi du message : {str(e)}")
                if not self.fail_silently:
                    raise
                continue

        if new_conn_created and not self.keep_alive:
            self.close()

        return num_sent

    def _send(self, email_message):
        try:
            # Utiliser send_message qui gère tous les types de messages
            return self.connection.send_message(email_message.message())
        except (SMTPException, socket_error) as e:
            logger.error(f"Erreur lors de l'envoi : {str(e)}")
            self.connection = None  # Forcer une nouvelle connexion
            raise

    def close(self):
        if self.connection:
            try:
                self.connection.quit()
            except (SMTPException, socket_error):
                self.connection.close()
            finally:
                self.connection = None 
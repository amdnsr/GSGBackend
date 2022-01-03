from datetime import datetime, timedelta
import logging
import os
import pathlib
import smtplib
from typing import Any, Dict, List, Optional

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import email
import email.mime.application
from email.headerregistry import Address

from jose import jwt

from app.config.configurations import AppConfig
from app.settings.app_settings import EmailSettings, Settings
from app.utils.helpers import prompt
# from app.core.config import settings

# https://www.dev2qa.com/python-send-plain-text-html-content-attached-files-embedded-images-email-example/


def send_email(to_email: str, subject: str = "", body: str = "", is_text: bool = False, attachment_file_paths: List = []) -> None:
    # assert EmailSettings.EMAILS_ENABLED, "no provided configuration for email variables"
    smtp_options = {"host": EmailSettings.SMTP_HOST,
                    "port": EmailSettings.SMTP_PORT,
                    "from_email": EmailSettings.EMAILS_FROM_EMAIL}
    if EmailSettings.SMTP_TLS:
        smtp_options["tls"] = True
    if EmailSettings.SMTP_USER:
        smtp_options["smtp_user"] = EmailSettings.SMTP_USER

    if is_text:
        # msg = MIMEMultipart('mixed', 'plain', 'utf-8')
        msg = MIMEText(body, 'plain', 'utf-8')
        # Contents = MIMEText(body, 'text', 'plain', 'utf-8')
    else:
        # The MIME types for text/html
        msg = MIMEMultipart('alternative')
        Contents = MIMEText(body, 'html')

    msg['Subject'] = subject

    msg['From'] = smtp_options["from_email"]
    msg['To'] = to_email

    # Adding file attachments
    attachments = []
    for filepath in attachment_file_paths:
        file_extension = pathlib.Path(filepath).suffix
        filename = pathlib.Path(filepath).name
        file_object = open(filepath, 'rb')
        attachment = email.mime.application.MIMEApplication(
            file_object.read(), _subtype=file_extension)
        attachment.add_header('Content-Disposition',
                              'attachment', filename=filename)
        attachments.append(attachment)
        file_object.close()

    # Attachment and HTML to body message.
    if len(attachments) > 0:
        for attachment in attachments:
            msg.attach(attachment)
    if not is_text:
        msg.attach(Contents)

    # creates SMTP session
    server = smtplib.SMTP(smtp_options["host"], smtp_options["port"])

    # start with ehlo (encrypted hello?) https://docs.python.org/3/library/smtplib.html#smtplib.SMTP.ehlo
    server.ehlo()

    # start TLS for security
    resp, reply = server.starttls()
    if resp != 220:
        # exit the function and return the response of starttls()
        return resp, reply

    # print(f"TLS RESPONSE {resp, reply}")

    if not Settings.ENVIRONMENT in ["DEV", "PYTEST"]:
        password = EmailSettings.SMTP_PASSWORD
        # password = prompt("password")
    else:
        password = EmailSettings.SMTP_PASSWORD

    # Authentication
    try:
        server.login(smtp_options["smtp_user"], password)
    except Exception as e:
        # log the error with traceback
        print(e)
        return False

    # sending the mail
    final_message = msg.as_string()
    # logging the email temporarily for testing
    # with open("result.html", "w") as f:
    #     f.write(str(final_message))
    result = None
    try:
        senderrs = server.sendmail(
            smtp_options["from_email"], to_email, final_message)
        result = True
    except smtplib.SMTPRecipientsRefused as e:
        result = False
        print(e)
    # if len(senderrs) != 0:
    #     # log the email addresses where the mail could not be sent
    #     print(senderrs)

    # terminating the session
    server.quit()
    return result


def send_test_email(to_email: str) -> None:
    project_name = AppConfig.TITLE
    public_url = AppConfig.PUBLIC_URL
    subject = f"{project_name} - Test email"
    home_link = f"{public_url}"
    body = f"Hello World! {home_link}"
    return send_email(to_email, subject, body, is_text=True)


def send_reset_password_email(to_email: str, email: str, username: str, token: str, attachment_file_paths: List = []) -> None:
    project_name = AppConfig.TITLE
    public_url = AppConfig.PUBLIC_URL
    subject = f"{project_name} - Password recovery for user {email}"
    reset_password_link = f"{public_url}/reset-password?token={token}"
    salutation = f"Team {project_name}"
    jinja_environment = EmailSettings.JINJA_ENVIRONMENT

    environment = {
        "project_name": project_name,
        "username": username,
        "email": email,
        "link": reset_password_link,
        "salutation": salutation
    }

    html_template = jinja_environment.get_template("new_account_email.html")
    # assuming html_template to be a jinja template
    html = html_template.render(**environment)
    return send_email(to_email, subject, html, attachment_file_paths)


def send_new_account_email(to_email: str, username: str, token: str, attachment_file_paths: List = []) -> None:

    project_name = AppConfig.TITLE
    public_url = AppConfig.PUBLIC_URL
    subject = f"{project_name} - New account for user {username}"
    account_confirmation_link = f"{public_url}/confirm-account-creation?token={token}"
    salutation = f"Team {project_name}"
    jinja_environment = EmailSettings.JINJA_ENVIRONMENT
    environment = {
        "project_name": project_name,
        "username": username,
        "email": to_email,
        "link": account_confirmation_link,
        # "salutation": salutation
    }

    html_template = jinja_environment.get_template("new_account_email.html")
    # assuming html_template to be a jinja template
    html = html_template.render(**environment)
    return send_email(to_email, subject, html, attachment_file_paths)


def generate_new_account_token(email: str) -> str:
    delta = timedelta(
        hours=EmailSettings.EMAIL_CREATE_ACCOUNT_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": str(email)}, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM,
    )
    return encoded_jwt


def verify_new_account_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(
            token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
        return decoded_token["sub"]
    except jwt.JWTError:
        return jwt.JWTError


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=EmailSettings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": str(email)}, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM,
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(
            token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
        return decoded_token["sub"]
    except jwt.JWTError:
        return jwt.JWTError

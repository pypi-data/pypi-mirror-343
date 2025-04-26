import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from os.path import basename

class EmailError(Exception):
    """Base class for all email-related exceptions."""
    
    def __init__(self, message:str="", *args, **kwargs) -> None:
        Exception.__init__(self, message, *args, **kwargs)
        
class EmailSendError(EmailError):
    """Exception raised when sending an email fails."""
    
    def __init__(self, message:str="", *args, **kwargs) -> None:
        EmailError.__init__(self, message, *args, **kwargs)
class EmailLoginError(EmailError):
    """Exception raised when login to the email server fails."""
    
    def __init__(self, message:str="", *args, **kwargs) -> None:
        EmailError.__init__(self, message, *args, **kwargs)

class EmailSMTPError(EmailError):
    """Exception raised for SMTP-related errors."""
    
    def __init__(self, message:str="", *args, **kwargs) -> None:
        EmailError.__init__(self, message, *args, **kwargs)
class EmailAttachmentError(EmailError):
    """Exception raised when there is an error with email attachments."""
    
    def __init__(self, message:str="", *args, **kwargs) -> None:
        EmailError.__init__(self, message, *args, **kwargs)

class EmailUnknownError(EmailError):
    """Exception raised for unknown errors."""
    
    def __init__(self, message:str="", *args, **kwargs) -> None:
        EmailError.__init__(self, message, *args, **kwargs)
class EmailCreationError(EmailError):
    """Exception raised when there is an error creating the email."""
    
    def __init__(self, message:str="", *args, **kwargs) -> None:
        EmailError.__init__(self, message, *args, **kwargs)

def send_email(subject:str, body:str, username:str, passwd:str, to:str, cc:str="", bcc:str="", sent_from:str=None, files:list[str]=None, server:str='smtp.outlook.com') -> None:
    """Sends an email via smtp authentication """

    port = '587'

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sent_from if sent_from else username
        msg['To'] = to
        msg['CC'] = cc
        msg['BCC'] = bcc
        msg.attach(MIMEText(body, 'html'))
    except Exception as e:
        raise EmailCreationError(f"Failed to create email from function arguments: {e}")

    try:
        for f in files or []:
            with open(f, "rb") as file:
                part = MIMEApplication(file.read(), Name=basename(f))
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)
    except Exception as e:
        raise EmailAttachmentError(f"Failed to get attachment(s): {e}")

    with smtplib.SMTP(server, port) as smtp:
        try:
            smtp.starttls()
            smtp.ehlo()
        except Exception as e:
            raise EmailSMTPError(f"Python SMTP failed to start {e}")           

        try: 
            smtp.login(username, passwd)
        except Exception as e: 
            raise EmailLoginError(f"Email login failure: {e}")
        
        try: 
            smtp.sendmail(username, to, msg.as_string())
        except Exception as e:
            raise EmailSendError(f"Failed to send email: {e}")
        
        try:
            smtp.quit()
        except Exception as e:
            raise EmailSMTPError(f"Failed to quit Python SMTP session: {e}")
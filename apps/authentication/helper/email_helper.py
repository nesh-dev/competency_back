import logging 
from django.core.mail import send_mail

def send_email(*args, **kwargs):
    """
    handle sending of mails to users
    Args:
        args (list): a list of possible arguements
        kwargs (dict): key worded arguements
    Return:
        None
    """
    try:
        send_mail(**kwargs)
    except Exception as e:
        logging.warning(e)


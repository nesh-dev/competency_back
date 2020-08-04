from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_signup_email(from_name,to_name,username, password,receiver):
    # Creating message subject and sender
    subject = 'Your account has been created.'
    sender = 'moringacompetency@gmail.com'

    #passing in the context vairables
    text_content = render_to_string('login-details.txt',{"from_name": from_name, "to_name":to_name, "username": username, "password":password})
    html_content = render_to_string('login-details.html',{"from_name": from_name, "to_name":to_name, "username": username, "password":password})

    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()



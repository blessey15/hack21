from django.utils.safestring import mark_safe
import threading
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError, EmailMessage

class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recepient_list):
        self.subject = subject
        self.recepient_list = recepient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(
            self.subject, #Email Subject
            self.html_content, #Email HTML Content
            'hack@mg.ieeemace.org', #From 
            self.recepient_list #To 
            )
        msg.content_subtype = 'html'
        try:
            msg.send()
            print("Email send: " + self.recepient_list[0])
        except BadHeaderError:
            print("Invalid header found")

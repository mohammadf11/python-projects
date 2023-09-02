from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings


def send_email(name, email, review):
    email_subject = 'send review email'
    email_body = f'hello {name} \n your review is : \n {review}'
    email = EmailMessage(email_subject, email_body,
                         settings.DEFAULT_FROM_EMAIL, [email, ],
                        )

    return email.send(fail_silently=False)


@shared_task
def send_email_task(name, email, review):
    
    return send_email(name, email, review)

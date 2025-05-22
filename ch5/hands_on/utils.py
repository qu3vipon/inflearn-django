from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.core.cache import cache

def send_str_email(email_to):
    send_mail(
        '새로운 이메일이 도착했습니다.',
        '안녕하세요. Django에서 보낸 이메일입니다.',
        settings.EMAIL_HOST_USER,
        [email_to],
    )


def send_html_email(email_to):
    email_html_cache_key = "email_html"

    if not (html := cache.get(key=email_html_cache_key)):
        print("새로운 html 파일을 읽는 중...")
        html = render_to_string("email.html")  # 오래 걸리는 작업
        cache.set(key=email_html_cache_key, value=html)

    message = EmailMessage(
        "새로운 이메일이 도착했습니다.",
        html,
        settings.EMAIL_HOST_USER,
        [email_to],
    )
    message.content_subtype = "html"
    message.send()

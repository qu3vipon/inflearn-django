from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.cache import cache


def send_str_email(email_to):
    send_mail(
        '새로운 이메일이 도착했습니다.',  # 이메일 제목
        '안녕하세요. Django에서 보낸 이메일입니다.',  # 이메일 본문
        settings.EMAIL_HOST_USER,  # 발신 이메일
        [email_to],  # 수신자 이메일 리스트
    )


def load_html():
    print("Load New Template…")
    return render_to_string("email.html")


def send_html_email(email_to):
    if not (html := cache.get("email_html")):
        html = load_html()
        cache.set("email_html", html)

    subject = "새로운 이메일이 도착했습니다."
    message = EmailMessage(
        subject, html, settings.EMAIL_HOST_USER, [email_to]  # 이메일 받을 계정
    )
    message.content_subtype = "html"
    message.send()

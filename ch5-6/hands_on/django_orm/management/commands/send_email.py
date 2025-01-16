from django.core.management.base import BaseCommand, CommandError
from utils import send_str_email, send_html_email


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("format", type=str)
        parser.add_argument("email_to", type=str)

    def handle(self, *args, **kwargs):
        # email format 검증
        if kwargs["format"] == "str":
            email_handler = send_str_email
        elif kwargs["format"] == "html":
            email_handler = send_html_email
        else:
            raise CommandError('Invalid format. Must be "str" or "html"')

        # email 주소 확인
        email_handler(email_to=kwargs["email_to"])

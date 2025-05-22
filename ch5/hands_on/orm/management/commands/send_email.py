from django.core.management import BaseCommand, CommandError

from utils import send_str_email, send_html_email


# python manage.py send_email str recipient@example.com
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("format", type=str)
        parser.add_argument("email_to", type=str)

    def handle(self, *args, **options):
        match options["format"]:
            case "str":
                send_str_email(email_to=options["email_to"])
            case "html":
                send_html_email(email_to=options["email_to"])
            case _:
                raise CommandError("잘못된 포맷입니다. 'str' 또는 'html'만 허용합니다.")

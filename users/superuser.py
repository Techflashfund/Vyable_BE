from django.contrib.auth.management.commands.createsuperuser import Command as BaseCommand

class Command(BaseCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--phone', dest='phone', default=None, help='Phone number for superuser')

    def handle(self, *args, **options):
        phone = options.get('phone')
        if not phone:
            phone = input('Phone number: ')
            options['phone'] = phone
        super().handle(*args, **options)
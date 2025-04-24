from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Example command for djmigrator.'

    def handle(self, *args, **kwargs):
        self.stdout.write("✅ djmigrator is working! This is your custom command.")

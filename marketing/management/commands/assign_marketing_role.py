# filepath: d:\completed\shelter.com\marketing\management\commands\assign_marketing_role.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from marketing.models import MarketingRole

User = get_user_model()

class Command(BaseCommand):
    help = 'Assign Marketing role to a user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the user')
        parser.add_argument('role', type=str, choices=['admin', 'manager', 'employee'], help='Role to assign')

    def handle(self, *args, **options):
        username = options['username']
        role = options['role']
        
        try:
            user = User.objects.get(username=username)
            marketing_role, created = MarketingRole.objects.get_or_create(user=user)
            marketing_role.role = role
            marketing_role.save()
            
            action = 'Created' if created else 'Updated'
            self.stdout.write(
                self.style.SUCCESS(f'{action} Marketing role for user "{username}" with role "{role}"')
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{username}" does not exist')
            )
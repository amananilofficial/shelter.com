# filepath: d:\completed\shelter.com\crm\management\commands\assign_crm_role.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from crm.models import CRMRole

User = get_user_model()

class Command(BaseCommand):
    help = 'Assign CRM role to a user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the user')
        parser.add_argument('role', type=str, choices=['admin', 'manager', 'employee'], help='Role to assign')

    def handle(self, *args, **options):
        username = options['username']
        role = options['role']
        
        try:
            user = User.objects.get(username=username)
            crm_role, created = CRMRole.objects.get_or_create(user=user)
            crm_role.role = role
            crm_role.save()
            
            action = 'Created' if created else 'Updated'
            self.stdout.write(
                self.style.SUCCESS(f'{action} CRM role for user "{username}" with role "{role}"')
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{username}" does not exist')
            )
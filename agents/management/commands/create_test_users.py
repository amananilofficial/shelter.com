from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from agents.models import AgentRole
from team.models import TeamRole
from crm.models import CRMRole

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample users with different roles for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--app',
            type=str,
            help='Specify app (agents, team, crm, marketing) or "all" for all apps',
            default='all'
        )

    def handle(self, *args, **options):
        app = options['app']
        
        if app in ['agents', 'all']:
            self.create_agent_users()
        
        if app in ['team', 'all']:
            self.create_team_users()
        
        if app in ['crm', 'all']:
            self.create_crm_users()
        
        if app in ['marketing', 'all']:
            self.create_marketing_users()

    def create_agent_users(self):
        self.stdout.write('Creating Agent users...')
        
        # Agent Admin
        user, created = User.objects.get_or_create(
            username='agent_admin',
            defaults={
                'email': 'agent_admin@example.com',
                'first_name': 'Agent',
                'last_name': 'Admin',
                'is_staff': True
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            AgentRole.objects.create(user=user, role='admin')
            self.stdout.write(f'Created Agent Admin: {user.username}')
        
        # Agent Manager
        user, created = User.objects.get_or_create(
            username='agent_manager',
            defaults={
                'email': 'agent_manager@example.com',
                'first_name': 'Agent',
                'last_name': 'Manager',
                'is_staff': True
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            AgentRole.objects.create(user=user, role='manager')
            self.stdout.write(f'Created Agent Manager: {user.username}')
        
        # Agent Employee
        user, created = User.objects.get_or_create(
            username='agent_employee',
            defaults={
                'email': 'agent_employee@example.com',
                'first_name': 'Agent',
                'last_name': 'Employee',
                'is_staff': True
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            AgentRole.objects.create(user=user, role='agent')
            self.stdout.write(f'Created Agent Employee: {user.username}')

    def create_team_users(self):
        self.stdout.write('Creating Team users...')
        
        # Team Admin
        user, created = User.objects.get_or_create(
            username='team_admin',
            defaults={
                'email': 'team_admin@example.com',
                'first_name': 'Team',
                'last_name': 'Admin',
                'is_staff': True
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            TeamRole.objects.create(user=user, role='admin')
            self.stdout.write(f'Created Team Admin: {user.username}')
        
        # Team Manager
        user, created = User.objects.get_or_create(
            username='team_manager',
            defaults={
                'email': 'team_manager@example.com',
                'first_name': 'Team',
                'last_name': 'Manager',
                'is_staff': True
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            TeamRole.objects.create(user=user, role='manager')
            self.stdout.write(f'Created Team Manager: {user.username}')
        
        # Team Member
        user, created = User.objects.get_or_create(
            username='team_member',
            defaults={
                'email': 'team_member@example.com',
                'first_name': 'Team',
                'last_name': 'Member',
                'is_staff': True
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            TeamRole.objects.create(user=user, role='member')
            self.stdout.write(f'Created Team Member: {user.username}')

    def create_crm_users(self):
        self.stdout.write('Creating CRM users...')
        
        # CRM Admin
        user, created = User.objects.get_or_create(
            username='crm_admin',
            defaults={
                'email': 'crm_admin@example.com',
                'first_name': 'CRM',
                'last_name': 'Admin',
                'is_staff': True
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            CRMRole.objects.create(user=user, role='admin')
            self.stdout.write(f'Created CRM Admin: {user.username}')
        
        # CRM Manager
        user, created = User.objects.get_or_create(
            username='crm_manager',
            defaults={
                'email': 'crm_manager@example.com',
                'first_name': 'CRM',
                'last_name': 'Manager',
                'is_staff': True
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            CRMRole.objects.create(user=user, role='manager')
            self.stdout.write(f'Created CRM Manager: {user.username}')
        
        # CRM Employee
        user, created = User.objects.get_or_create(
            username='crm_employee',
            defaults={
                'email': 'crm_employee@example.com',
                'first_name': 'CRM',
                'last_name': 'Employee',
                'is_staff': True
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            CRMRole.objects.create(user=user, role='employee')
            self.stdout.write(f'Created CRM Employee: {user.username}')

    def create_marketing_users(self):
        self.stdout.write('Creating Marketing users...')
        
        try:
            from marketing.models import MarketingRole
            
            # Marketing Admin
            user, created = User.objects.get_or_create(
                username='marketing_admin',
                defaults={
                    'email': 'marketing_admin@example.com',
                    'first_name': 'Marketing',
                    'last_name': 'Admin',
                    'is_staff': True
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                MarketingRole.objects.create(user=user, role='admin')
                self.stdout.write(f'Created Marketing Admin: {user.username}')
            
            # Marketing Manager
            user, created = User.objects.get_or_create(
                username='marketing_manager',
                defaults={
                    'email': 'marketing_manager@example.com',
                    'first_name': 'Marketing',
                    'last_name': 'Manager',
                    'is_staff': True
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                MarketingRole.objects.create(user=user, role='manager')
                self.stdout.write(f'Created Marketing Manager: {user.username}')
            
            # Marketing Employee
            user, created = User.objects.get_or_create(
                username='marketing_employee',
                defaults={
                    'email': 'marketing_employee@example.com',
                    'first_name': 'Marketing',
                    'last_name': 'Employee',
                    'is_staff': True
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                MarketingRole.objects.create(user=user, role='employee')
                self.stdout.write(f'Created Marketing Employee: {user.username}')
                
        except ImportError:
            self.stdout.write('Marketing app not available, skipping marketing users')

        self.stdout.write(self.style.SUCCESS('Successfully created sample users!'))
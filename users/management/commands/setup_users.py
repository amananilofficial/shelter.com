from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify
from datetime import datetime, timedelta
from decimal import Decimal
import random
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Setup automated users with roles and sample data for all apps'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset all data before creating new users',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting automated user setup...'))
        
        if options['reset']:
            self.stdout.write(self.style.WARNING('Resetting existing data...'))
            self.reset_data()

        with transaction.atomic():
            # Create superuser first
            self.create_superuser()
            
            # Create users for each app
            self.create_shelter_users()
            self.create_agents_users()
            self.create_team_users()
            self.create_crm_users()
            self.create_marketing_users()
            
            # Generate sample data
            self.generate_sample_data()
            
            # Print user credentials
            self.print_user_credentials()

        self.stdout.write(self.style.SUCCESS('User setup completed successfully!'))

    def reset_data(self):
        """Reset all user data except superusers"""
        User.objects.filter(is_superuser=False).delete()
        
        # Reset app-specific data
        try:
            from agents.models import Agent, AgentRole, AgentContact, WorkNote
            Agent.objects.all().delete()
            AgentRole.objects.all().delete()
            AgentContact.objects.all().delete()
            WorkNote.objects.all().delete()
        except ImportError:
            pass
            
        try:
            from team.models import Team, TeamRole, TeamContactMessage
            Team.objects.all().delete()
            TeamRole.objects.all().delete()
            TeamContactMessage.objects.all().delete()
        except ImportError:
            pass
            
        try:
            from crm.models import Customer, CRMRole, CustomerInteraction, DataTransfer
            Customer.objects.all().delete()
            CRMRole.objects.all().delete()
            CustomerInteraction.objects.all().delete()
            DataTransfer.objects.all().delete()
        except ImportError:
            pass

    def create_superuser(self):
        """Create main superuser"""
        if not User.objects.filter(username='admin').exists():
            user = User.objects.create_user(
                username='admin',
                email='admin@shelter.com',
                password='admin123',
                first_name='System',
                last_name='Administrator',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(f'Created superuser: {user.username}')

    def create_shelter_users(self):
        """Create users for main shelter app"""
        users_data = [
            {
                'username': 'shelter_manager',
                'email': 'manager@shelter.com',
                'password': 'shelter123',
                'first_name': 'John',
                'last_name': 'Manager',
                'is_staff': True,
                'role': 'manager'
            },
            {
                'username': 'shelter_employee',
                'email': 'employee@shelter.com',
                'password': 'shelter123',
                'first_name': 'Jane',
                'last_name': 'Employee',
                'is_staff': True,
                'role': 'employee'
            }
        ]
        
        for user_data in users_data:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    is_staff=user_data['is_staff']
                )
                self.stdout.write(f'Created shelter user: {user.username}')

    def create_agents_users(self):
        """Create users for agents app"""
        try:
            from agents.models import Agent, AgentRole
            
            users_data = [
                {
                    'username': 'agent_admin',
                    'email': 'admin@agents.com',
                    'password': 'agent123',
                    'first_name': 'Michael',
                    'last_name': 'Agent Admin',
                    'role': 'admin'
                },
                {
                    'username': 'agent_manager',
                    'email': 'manager@agents.com',
                    'password': 'agent123',
                    'first_name': 'Sarah',
                    'last_name': 'Agent Manager',
                    'role': 'manager'
                },
                {
                    'username': 'agent_1',
                    'email': 'agent1@agents.com',
                    'password': 'agent123',
                    'first_name': 'David',
                    'last_name': 'Smith',
                    'role': 'agent'
                },
                {
                    'username': 'agent_2',
                    'email': 'agent2@agents.com',
                    'password': 'agent123',
                    'first_name': 'Emily',
                    'last_name': 'Johnson',
                    'role': 'agent'
                }
            ]
            
            for user_data in users_data:
                if not User.objects.filter(username=user_data['username']).exists():
                    user = User.objects.create_user(
                        username=user_data['username'],
                        email=user_data['email'],
                        password=user_data['password'],
                        first_name=user_data['first_name'],
                        last_name=user_data['last_name'],
                        is_staff=True
                    )
                    
                    # Create AgentRole
                    AgentRole.objects.create(
                        user=user,
                        role=user_data['role']
                    )
                      # Create Agent profile
                    Agent.objects.create(
                        user=user,
                        name=f"{user_data['first_name']} {user_data['last_name']}",
                        title='Real Estate Agent',
                        email=user_data['email'],
                        phone=f"+1{random.randint(1000000000, 9999999999)}",
                        whatsapp=f"+1{random.randint(1000000000, 9999999999)}",
                        instagram=f"@{user_data['username']}",
                        linkedin=f"linkedin.com/in/{user_data['username']}",
                        description=f"Experienced real estate agent specializing in residential properties.",
                        work_experience="5 years in real estate|100+ successful transactions|Client satisfaction specialist",
                        hire_date=timezone.now() - timedelta(days=random.randint(30, 1000))
                    )
                    
                    self.stdout.write(f'Created agent user: {user.username}')
                    
        except ImportError:
            self.stdout.write(self.style.WARNING('Agents app not found, skipping...'))

    def create_team_users(self):
        """Create users for team app"""
        try:
            from team.models import Team, TeamRole
            
            users_data = [
                {
                    'username': 'team_admin',
                    'email': 'admin@team.com',
                    'password': 'team123',
                    'first_name': 'Robert',
                    'last_name': 'Team Admin',
                    'role': 'admin',
                    'position': 'Team Lead'
                },
                {
                    'username': 'team_manager',
                    'email': 'manager@team.com',
                    'password': 'team123',
                    'first_name': 'Lisa',
                    'last_name': 'Team Manager',
                    'role': 'manager',
                    'position': 'Project Manager'
                },
                {
                    'username': 'team_member_1',
                    'email': 'member1@team.com',
                    'password': 'team123',
                    'first_name': 'Alex',
                    'last_name': 'Wilson',
                    'role': 'member',
                    'position': 'Developer'
                },
                {
                    'username': 'team_member_2',
                    'email': 'member2@team.com',
                    'password': 'team123',
                    'first_name': 'Jessica',
                    'last_name': 'Brown',
                    'role': 'member',                    'position': 'Designer'
                }
            ]
            
            for user_data in users_data:
                if not User.objects.filter(username=user_data['username']).exists():
                    user = User.objects.create_user(
                        username=user_data['username'],
                        email=user_data['email'],
                        password=user_data['password'],
                        first_name=user_data['first_name'],
                        last_name=user_data['last_name'],
                        is_staff=True
                    )
                    
                    # Create TeamRole
                    TeamRole.objects.create(
                        user=user,
                        role=user_data['role']
                    )
                      # Create Team profile
                    Team.objects.create(
                        name=f"{user_data['first_name']} {user_data['last_name']}",
                        title=user_data['position'],
                        description=f"Professional {user_data['position'].lower()} with extensive experience.",
                        email=user_data['email'],
                        phone=f"+1{random.randint(1000000000, 9999999999)}",
                        whatsapp=f"+1{random.randint(1000000000, 9999999999)}",
                        instagram=f"@{user_data['username']}",
                        linkedin=f"linkedin.com/in/{user_data['username']}",
                        role=user_data['role'],
                        user=user,
                        hire_date=timezone.now().date() - timedelta(days=random.randint(30, 800)),
                        work_experience=f"3+ years in {user_data['position'].lower()}|Team collaboration expert|Problem solver",
                        is_published=True
                    )
                    
                    self.stdout.write(f'Created team user: {user.username}')
                    
        except ImportError:
            self.stdout.write(self.style.WARNING('Team app not found, skipping...'))

    def create_crm_users(self):
        """Create users for CRM app"""
        try:
            from crm.models import CRMRole
            
            users_data = [
                {
                    'username': 'crm_admin',
                    'email': 'admin@crm.com',
                    'password': 'crm123',
                    'first_name': 'Thomas',
                    'last_name': 'CRM Admin',
                    'role': 'admin'
                },
                {
                    'username': 'crm_manager',
                    'email': 'manager@crm.com',
                    'password': 'crm123',
                    'first_name': 'Maria',
                    'last_name': 'CRM Manager',
                    'role': 'manager'
                },
                {
                    'username': 'crm_employee_1',
                    'email': 'employee1@crm.com',
                    'password': 'crm123',
                    'first_name': 'James',
                    'last_name': 'Taylor',
                    'role': 'employee'
                },
                {
                    'username': 'crm_employee_2',
                    'email': 'employee2@crm.com',
                    'password': 'crm123',
                    'first_name': 'Anna',
                    'last_name': 'Davis',
                    'role': 'employee'
                }
            ]
            
            for user_data in users_data:
                if not User.objects.filter(username=user_data['username']).exists():
                    user = User.objects.create_user(
                        username=user_data['username'],
                        email=user_data['email'],
                        password=user_data['password'],
                        first_name=user_data['first_name'],
                        last_name=user_data['last_name'],
                        is_staff=True
                    )
                    
                    # Create CRMRole
                    CRMRole.objects.create(
                        user=user,
                        role=user_data['role']
                    )
                    
                    self.stdout.write(f'Created CRM user: {user.username}')
                    
        except ImportError:
            self.stdout.write(self.style.WARNING('CRM app not found, skipping...'))

    def create_marketing_users(self):
        """Create users for marketing app"""
        try:
            from marketing.models import MarketingRole
            
            users_data = [
                {
                    'username': 'marketing_admin',
                    'email': 'admin@marketing.com',
                    'password': 'marketing123',
                    'first_name': 'Jennifer',
                    'last_name': 'Marketing Admin',
                    'role': 'admin'
                },
                {
                    'username': 'marketing_manager',
                    'email': 'manager@marketing.com',
                    'password': 'marketing123',
                    'first_name': 'Kevin',
                    'last_name': 'Marketing Manager',
                    'role': 'manager'
                },
                {
                    'username': 'marketing_employee',
                    'email': 'employee@marketing.com',
                    'password': 'marketing123',
                    'first_name': 'Rachel',
                    'last_name': 'Green',
                    'role': 'employee'
                }
            ]
            
            for user_data in users_data:
                if not User.objects.filter(username=user_data['username']).exists():
                    user = User.objects.create_user(
                        username=user_data['username'],
                        email=user_data['email'],
                        password=user_data['password'],
                        first_name=user_data['first_name'],
                        last_name=user_data['last_name'],
                        is_staff=True
                    )
                    
                    # Create MarketingRole
                    MarketingRole.objects.create(
                        user=user,
                        role=user_data['role']
                    )
                    
                    self.stdout.write(f'Created marketing user: {user.username}')
                    
        except ImportError:
            self.stdout.write(self.style.WARNING('Marketing app not found, skipping...'))

    def generate_sample_data(self):
        """Generate sample data for all apps"""
        self.stdout.write('Generating sample data...')
        
        # Generate shelter data
        self.generate_shelter_data()
        
        # Generate agents data
        self.generate_agents_data()
        
        # Generate team data
        self.generate_team_data()
          # Generate CRM data
        self.generate_crm_data()

    def generate_shelter_data(self):
        """Generate sample data for shelter app"""
        try:
            from shelter.models import Listening, Contact, Newsletter
            from agents.models import Agent
            
            # Get agents for listings
            agents = Agent.objects.all()
            if not agents:
                return
                  # Sample listings
            listings_data = [
                {
                    'title': 'Luxury Villa in Downtown',
                    'location': 'Downtown',
                    'price': 850000,
                    'bedrooms': 4,
                    'bathrooms': 3,
                    'area': 2500,
                    'status': 'sale',
                    'description': 'Beautiful luxury villa with modern amenities.',
                    'kitchen': 2,
                    'garage': 2,
                    'is_featured': True
                },
                {
                    'title': 'Modern Apartment for Rent',
                    'location': 'City Center',
                    'price': 2500,
                    'bedrooms': 2,
                    'bathrooms': 2,
                    'area': 1200,
                    'status': 'rent',
                    'description': 'Modern apartment with city views.',
                    'kitchen': 1,
                    'garage': 0,
                    'is_featured': False
                },
                {
                    'title': 'Family House with Garden',
                    'location': 'Suburbs',
                    'price': 450000,
                    'bedrooms': 3,
                    'bathrooms': 2,
                    'area': 1800,
                    'status': 'sale',
                    'description': 'Perfect family home with large garden.',
                    'kitchen': 1,
                    'garage': 1,
                    'is_featured': True
                }
            ]
              # Generate unique slugs to avoid UNIQUE constraint errors
            used_slugs = set()
            
            for i in range(50):
                listing_data = random.choice(listings_data).copy()  # Use copy to avoid modifying original
                
                # Generate unique title and slug
                listing_data['title'] = f"{listing_data['title']} #{i+1}"
                listing_data['slug'] = slugify(listing_data['title'])
                
                # Ensure unique slug
                base_slug = listing_data['slug']
                slug = base_slug
                counter = 1
                while slug in used_slugs:
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                listing_data['slug'] = slug
                used_slugs.add(slug)
                
                Listening.objects.create(
                    agent=random.choice(agents),
                    **listing_data
                )
            
            # Sample contacts
            contacts_data = [
                {
                    'name': 'John Doe',
                    'email': 'john.doe@example.com',
                    'phone': '+1234567890',
                    'message': 'Interested in luxury villa listings.'
                },
                {
                    'name': 'Jane Smith',
                    'email': 'jane.smith@example.com',
                    'phone': '+1234567891',
                    'message': 'Looking for rental apartments in city center.'
                }
            ]
            
            for contact_data in contacts_data:
                if not Contact.objects.filter(email=contact_data['email']).exists():
                    Contact.objects.create(**contact_data)
            
            # Sample newsletter subscribers
            newsletter_data = [
                {
                    'name': 'Alice Johnson',
                    'email': 'alice@example.com',
                    'phone': '+1234567892',
                    'whatsapp_updates': True
                },
                {
                    'name': 'Bob Wilson',
                    'email': 'bob@example.com',
                    'phone': '+1234567893',
                    'whatsapp_updates': False
                }            ]
            
            for newsletter in newsletter_data:
                if not Newsletter.objects.filter(email=newsletter['email']).exists():
                    Newsletter.objects.create(**newsletter)
                    
        except ImportError:
            pass
                    
        except ImportError:
            pass

    def generate_agents_data(self):
        """Generate sample data for agents app"""
        try:
            from agents.models import AgentContact, WorkNote
            from django.contrib.auth import get_user_model
            
            User = get_user_model()
            agents = User.objects.filter(agent_role__isnull=False)
            
            # Sample agent contacts
            contacts_data = [
                {
                    'agentname': 'David Smith',
                    'user_name': 'Mike Johnson',
                    'user_email': 'mike.j@example.com',
                    'user_phone': '+1234567894',
                    'user_subject': 'Property inquiry for downtown area'
                },
                {
                    'agentname': 'Emily Johnson',
                    'user_name': 'Sarah Davis',
                    'user_email': 'sarah.d@example.com',
                    'user_phone': '+1234567895',
                    'user_subject': 'Looking for investment properties'
                }
            ]
            
            for contact_data in contacts_data:
                AgentContact.objects.create(**contact_data)
            
            # Sample work notes
            for agent in agents[:2]:
                WorkNote.objects.create(
                    user=agent,
                    title=f'Follow up with client - {agent.first_name}',
                    description=f'Need to follow up with potential buyers for downtown properties.',
                    related_customer_id=random.randint(1, 10)
                )
                
        except ImportError:
            pass

    def generate_team_data(self):
        """Generate sample data for team app"""
        try:
            from team.models import TeamContactMessage, Team
            
            teams = Team.objects.all()
            
            # Sample team contact messages
            messages_data = [
                {
                    'name': 'Client A',
                    'email': 'clienta@example.com',
                    'phone': '+1234567896',
                    'message': 'Interested in your services for property management.'
                },
                {
                    'name': 'Client B',
                    'email': 'clientb@example.com',
                    'phone': '+1234567897',
                    'message': 'Need consultation for real estate investment.'
                }
            ]
            
            for team in teams[:2]:
                for i, msg_data in enumerate(messages_data):
                    TeamContactMessage.objects.create(
                        team=team,
                        name=f"{msg_data['name']} {i+1}",
                        email=msg_data['email'].replace('@', f'{i+1}@'),
                        phone=msg_data['phone'],
                        message=msg_data['message']
                    )
                    
        except ImportError:
            pass

    def generate_crm_data(self):
        """Generate sample data for CRM app"""
        try:
            from crm.models import Customer, CustomerInteraction
            from django.contrib.auth import get_user_model
            
            User = get_user_model()
            crm_users = User.objects.filter(crm_role__isnull=False)
            
            # Sample customers
            customers_data = [
                {
                    'first_name': 'John',
                    'last_name': 'Anderson',
                    'email': 'john.anderson@example.com',
                    'phone': '+1234567898',
                    'address': '123 Main St',
                    'city': 'New York',
                    'status': 'lead',
                    'priority': 'high',
                    'source': 'Website',
                    'notes': 'Interested in luxury properties'
                },
                {
                    'first_name': 'Emma',
                    'last_name': 'Thompson',
                    'email': 'emma.thompson@example.com',
                    'phone': '+1234567899',
                    'address': '456 Oak Ave',
                    'city': 'Los Angeles',
                    'status': 'prospect',
                    'priority': 'medium',
                    'source': 'Referral',
                    'notes': 'Looking for rental properties'
                },
                {
                    'first_name': 'Michael',
                    'last_name': 'Rodriguez',
                    'email': 'michael.rodriguez@example.com',
                    'phone': '+1234567800',
                    'address': '789 Pine St',
                    'city': 'Chicago',
                    'status': 'customer',
                    'priority': 'high',
                    'source': 'Advertisement',
                    'notes': 'Repeat customer, purchased 2 properties'
                }
            ]
            
            created_customers = []
            for customer_data in customers_data:
                if not Customer.objects.filter(email=customer_data['email']).exists():
                    customer_data['assigned_to'] = random.choice(crm_users) if crm_users else None
                    customer_data['created_by'] = random.choice(crm_users) if crm_users else None
                    customer = Customer.objects.create(**customer_data)
                    created_customers.append(customer)
            
            # Sample customer interactions
            interaction_types = ['call', 'email', 'meeting', 'whatsapp']
            for customer in created_customers:
                for i in range(random.randint(1, 3)):
                    CustomerInteraction.objects.create(
                        customer=customer,
                        interaction_type=random.choice(interaction_types),
                        subject=f'Follow up call #{i+1}',
                        description=f'Discussed property requirements and budget with {customer.first_name}.',
                        created_by=customer.assigned_to or crm_users[0] if crm_users else None
                    )
                    
        except ImportError:
            pass

    def print_user_credentials(self):
        """Print all user credentials"""
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('USER CREDENTIALS'))
        self.stdout.write(self.style.SUCCESS('='*60))
        
        # Superuser
        self.stdout.write(self.style.WARNING('\nSUPERUSER:'))
        self.stdout.write(f'Username: admin')
        self.stdout.write(f'Password: admin123')
        self.stdout.write(f'Email: admin@shelter.com')
        
        # Shelter users
        self.stdout.write(self.style.WARNING('\nSHELTER APP USERS:'))
        shelter_users = [
            ('shelter_manager', 'shelter123', 'manager@shelter.com'),
            ('shelter_employee', 'shelter123', 'employee@shelter.com')
        ]
        for username, password, email in shelter_users:
            self.stdout.write(f'Username: {username} | Password: {password} | Email: {email}')
        
        # Agents users
        self.stdout.write(self.style.WARNING('\nAGENTS APP USERS:'))
        agents_users = [
            ('agent_admin', 'agent123', 'admin@agents.com', 'Admin'),
            ('agent_manager', 'agent123', 'manager@agents.com', 'Manager'),
            ('agent_1', 'agent123', 'agent1@agents.com', 'Agent'),
            ('agent_2', 'agent123', 'agent2@agents.com', 'Agent')
        ]
        for username, password, email, role in agents_users:
            self.stdout.write(f'Username: {username} | Password: {password} | Email: {email} | Role: {role}')
        
        # Team users
        self.stdout.write(self.style.WARNING('\nTEAM APP USERS:'))
        team_users = [
            ('team_admin', 'team123', 'admin@team.com', 'Admin'),
            ('team_manager', 'team123', 'manager@team.com', 'Manager'),
            ('team_member_1', 'team123', 'member1@team.com', 'Member'),
            ('team_member_2', 'team123', 'member2@team.com', 'Member')
        ]
        for username, password, email, role in team_users:
            self.stdout.write(f'Username: {username} | Password: {password} | Email: {email} | Role: {role}')
        
        # CRM users
        self.stdout.write(self.style.WARNING('\nCRM APP USERS:'))
        crm_users = [
            ('crm_admin', 'crm123', 'admin@crm.com', 'Admin'),
            ('crm_manager', 'crm123', 'manager@crm.com', 'Manager'),
            ('crm_employee_1', 'crm123', 'employee1@crm.com', 'Employee'),
            ('crm_employee_2', 'crm123', 'employee2@crm.com', 'Employee')
        ]
        for username, password, email, role in crm_users:
            self.stdout.write(f'Username: {username} | Password: {password} | Email: {email} | Role: {role}')
        
        # Marketing users
        self.stdout.write(self.style.WARNING('\nMARKETING APP USERS:'))
        marketing_users = [
            ('marketing_admin', 'marketing123', 'admin@marketing.com', 'Admin'),
            ('marketing_manager', 'marketing123', 'manager@marketing.com', 'Manager'),
            ('marketing_employee', 'marketing123', 'employee@marketing.com', 'Employee')
        ]
        for username, password, email, role in marketing_users:
            self.stdout.write(f'Username: {username} | Password: {password} | Email: {email} | Role: {role}')
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('To run this command:'))
        self.stdout.write(self.style.SUCCESS('python manage.py setup_users'))
        self.stdout.write(self.style.SUCCESS('python manage.py setup_users --reset (to reset all data)'))
        self.stdout.write(self.style.SUCCESS('='*60))
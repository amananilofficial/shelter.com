from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from team.models import Team, TeamRole
import logging

User = get_user_model()
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Sync team data with other apps (agents, crm, marketing)'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--reverse', 
            action='store_true',
            help='Sync data from other apps to team app'
        )
        parser.add_argument(
            '--app',
            type=str,
            choices=['agents', 'crm', 'marketing', 'all'],
            default='all',
            help='Specify which app to sync with'
        )
    
    def handle(self, *args, **options):
        if options['reverse']:
            self.sync_from_other_apps(options['app'])
        else:
            self.sync_to_other_apps(options['app'])
    
    def sync_to_other_apps(self, target_app):
        """Sync team data to other apps"""
        self.stdout.write(self.style.SUCCESS(f'Starting sync to {target_app} app(s)...'))
        
        team_members = Team.objects.filter(role__in=['manager', 'admin'])
        synced_count = 0
        
        for team in team_members:
            try:
                if target_app in ['agents', 'all']:
                    self.sync_to_agents(team)
                
                if target_app in ['crm', 'all']:
                    self.sync_to_crm(team)
                
                if target_app in ['marketing', 'all']:
                    self.sync_to_marketing(team)
                
                synced_count += 1
                self.stdout.write(f'Synced: {team.name}')
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error syncing {team.name}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully synced {synced_count} team members')
        )
    
    def sync_from_other_apps(self, source_app):
        """Sync data from other apps to team"""
        self.stdout.write(self.style.SUCCESS(f'Starting reverse sync from {source_app} app(s)...'))
        
        synced_count = 0
        
        if source_app in ['agents', 'all']:
            synced_count += self.sync_from_agents()
        
        if source_app in ['crm', 'all']:
            synced_count += self.sync_from_crm()
        
        if source_app in ['marketing', 'all']:
            synced_count += self.sync_from_marketing()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully reverse synced {synced_count} records')
        )
    
    def sync_to_agents(self, team):
        """Sync team member to agents app"""
        try:
            from agents.models import Agent, AgentRole
            
            if team.user:
                # Create/update AgentRole
                agent_role, created = AgentRole.objects.get_or_create(
                    user=team.user,
                    defaults={'role': 'admin' if team.role == 'admin' else 'agent'}
                )
                if not created:
                    agent_role.role = 'admin' if team.role == 'admin' else 'agent'
                    agent_role.save()
            
            # Create/update Agent
            agent, created = Agent.objects.get_or_create(
                email=team.email,
                defaults={
                    'name': team.name,
                    'title': team.title or 'Team Member',
                    'phone': team.phone,
                    'description': team.description,
                    'whatsapp': team.whatsapp,
                    'instagram': team.instagram,
                    'linkedin': team.linkedin,
                    'work_experience': team.work_experience
                }
            )
            if not created:
                agent.name = team.name
                agent.title = team.title or agent.title
                agent.phone = team.phone
                agent.description = team.description
                agent.whatsapp = team.whatsapp
                agent.instagram = team.instagram
                agent.linkedin = team.linkedin
                agent.work_experience = team.work_experience
                agent.save()
                
        except ImportError:
            self.stdout.write(self.style.WARNING('Agents app not available'))
    
    def sync_to_crm(self, team):
        """Sync team member to CRM app"""
        try:
            from crm.models import CRMRole
            
            if team.user:
                crm_role, created = CRMRole.objects.get_or_create(
                    user=team.user,
                    defaults={'role': 'admin' if team.role == 'admin' else 'manager'}
                )
                if not created:
                    crm_role.role = 'admin' if team.role == 'admin' else 'manager'
                    crm_role.save()
                    
        except ImportError:
            self.stdout.write(self.style.WARNING('CRM app not available'))
    
    def sync_to_marketing(self, team):
        """Sync team member to marketing app"""
        try:
            from marketing.models import MarketingRole
            
            if team.user:
                marketing_role, created = MarketingRole.objects.get_or_create(
                    user=team.user,
                    defaults={'role': 'admin' if team.role == 'admin' else 'manager'}
                )
                if not created:
                    marketing_role.role = 'admin' if team.role == 'admin' else 'manager'
                    marketing_role.save()
                    
        except ImportError:
            self.stdout.write(self.style.WARNING('Marketing app not available'))
    
    def sync_from_agents(self):
        """Sync from agents app to team"""
        try:
            from agents.models import Agent, AgentRole
            
            synced = 0
            for agent in Agent.objects.all():
                team, created = Team.objects.get_or_create(
                    email=agent.email,
                    defaults={
                        'name': agent.name,
                        'title': agent.title,
                        'description': agent.description,
                        'phone': agent.phone,
                        'whatsapp': agent.whatsapp,
                        'instagram': agent.instagram,
                        'linkedin': agent.linkedin,
                        'work_experience': agent.work_experience,
                        'role': 'manager',
                        'hire_date': agent.hire_date,
                        'is_published': True
                    }
                )
                if not created:
                    team.name = agent.name
                    team.title = agent.title
                    team.description = agent.description
                    team.phone = agent.phone
                    team.whatsapp = agent.whatsapp
                    team.instagram = agent.instagram
                    team.linkedin = agent.linkedin
                    team.work_experience = agent.work_experience
                    team.save()
                
                synced += 1
                self.stdout.write(f'Synced from agents: {agent.name}')
            
            return synced
            
        except ImportError:
            self.stdout.write(self.style.WARNING('Agents app not available'))
            return 0
    
    def sync_from_crm(self):
        """Sync from CRM app to team"""
        try:
            from crm.models import CRMRole
            
            synced = 0
            for crm_role in CRMRole.objects.all():
                if crm_role.user:
                    team, created = Team.objects.get_or_create(
                        user=crm_role.user,
                        defaults={
                            'name': f"{crm_role.user.first_name} {crm_role.user.last_name}".strip() or crm_role.user.username,
                            'title': f"CRM {crm_role.role.title()}",
                            'description': f"CRM system {crm_role.role}",
                            'email': crm_role.user.email,
                            'phone': "",
                            'role': 'admin' if crm_role.role == 'admin' else 'manager',
                            'is_published': True
                        }
                    )
                    if not created:
                        team.role = 'admin' if crm_role.role == 'admin' else 'manager'
                        team.save()
                    
                    synced += 1
                    self.stdout.write(f'Synced from CRM: {team.name}')
            
            return synced
            
        except ImportError:
            self.stdout.write(self.style.WARNING('CRM app not available'))
            return 0
    
    def sync_from_marketing(self):
        """Sync from marketing app to team"""
        try:
            from marketing.models import MarketingRole
            
            synced = 0
            for marketing_role in MarketingRole.objects.all():
                if marketing_role.user:
                    team, created = Team.objects.get_or_create(
                        user=marketing_role.user,
                        defaults={
                            'name': f"{marketing_role.user.first_name} {marketing_role.user.last_name}".strip() or marketing_role.user.username,
                            'title': f"Marketing {marketing_role.role.title()}",
                            'description': f"Marketing system {marketing_role.role}",
                            'email': marketing_role.user.email,
                            'phone': "",
                            'role': 'admin' if marketing_role.role == 'admin' else 'manager',
                            'is_published': True
                        }
                    )
                    if not created:
                        team.role = 'admin' if marketing_role.role == 'admin' else 'manager'
                        team.save()
                    
                    synced += 1
                    self.stdout.write(f'Synced from Marketing: {team.name}')
            
            return synced
            
        except ImportError:
            self.stdout.write(self.style.WARNING('Marketing app not available'))
            return 0
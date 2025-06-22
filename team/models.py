from django.db import models
from datetime import datetime
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
import logging
import random
import string

User = get_user_model()
logger = logging.getLogger(__name__)

class TeamRole(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('member', 'Member'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='team_role')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Ensure user has staff access to admin
        if self.user and not self.user.is_staff:
            self.user.is_staff = True
            self.user.save()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
    class Meta:
        verbose_name = "Team Role"
        verbose_name_plural = "Team Roles"

# Create your models here.
class Team(models.Model):
    ROLE_CHOICES = [
        ('member', 'Team Member'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
        ('supervisor', 'Supervisor'),
        ('lead', 'Team Lead'),
    ]
    
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    work_experience = models.TextField(
        blank=True,
        help_text="Enter work experience points separated by the '|' character. Each point will be displayed as a separate bullet point on the frontend."
    )
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='member',
        help_text="Role of the team member in organization"
    )
    hire_date = models.DateField(null=True, blank=True)
    user = models.OneToOneField(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="Link to user account if team member has system access"    )
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def work_experience_as_list(self):
        """Returns work_experience as a list of bullet points"""
        return [exp.strip() for exp in self.work_experience.split('|') if exp.strip()]

    def work_experience_as_html(self):
        """Returns work_experience as HTML bullet list"""
        items = self.work_experience_as_list()
        if not items:
            return "-"
        return format_html("<ul>{}</ul>", format_html("".join(f"<li>{item}</li>" for item in items)))

    def create_or_update_user_account(self):
        """Create or update user account based on team member role"""
        if self.role in ['manager', 'admin'] and not self.user:
            try:
                # Generate username from name
                username = self.generate_username()
                
                # Create user account
                user = User.objects.create_user(
                    username=username,
                    email=self.email,
                    first_name=self.name.split()[0] if self.name.split() else self.name,
                    last_name=' '.join(self.name.split()[1:]) if len(self.name.split()) > 1 else '',
                    password=self.generate_temp_password()
                )
                
                # Set user permissions based on role
                if self.role == 'admin':
                    user.is_staff = True
                    user.is_superuser = True
                    admin_group, created = Group.objects.get_or_create(name='Admin')
                    user.groups.add(admin_group)
                elif self.role == 'manager':
                    user.is_staff = True
                    manager_group, created = Group.objects.get_or_create(name='Manager')
                    user.groups.add(manager_group)
                
                user.save()
                self.user = user
                self.save(update_fields=['user'])
                
                # Sync with other apps
                self.sync_with_other_apps()
                
                logger.info(f"Created user account for {self.name} with role {self.role}")
                
            except Exception as e:
                logger.error(f"Error creating user account for {self.name}: {str(e)}")
    
    def generate_username(self):
        """Generate unique username from name"""
        base_username = slugify(self.name.replace(' ', ''))[:20]
        username = base_username
        counter = 1
        
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
            
        return username
    
    def generate_temp_password(self):
        """Generate temporary password"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=12))    
    def sync_with_other_apps(self):
        """Sync team member data with other apps"""
        try:
            # Sync with agents app if exists
            try:
                from agents.models import Agent, AgentRole
                if self.role in ['manager', 'admin'] and self.user:
                    # Create/update AgentRole
                    agent_role, created = AgentRole.objects.get_or_create(
                        user=self.user,
                        defaults={'role': 'admin' if self.role == 'admin' else 'agent'}
                    )
                    if not created:
                        agent_role.role = 'admin' if self.role == 'admin' else 'agent'
                        agent_role.save()
                    
                    # Create/update Agent
                    agent, created = Agent.objects.get_or_create(
                        email=self.email,
                        defaults={
                            'name': self.name,
                            'title': self.title or 'Team Member',
                            'phone': self.phone,
                            'description': self.description,
                            'whatsapp': self.whatsapp,
                            'instagram': self.instagram,
                            'linkedin': self.linkedin,
                            'hire_date': self.hire_date or datetime.now(),
                            'work_experience': self.work_experience
                        }
                    )
                    if not created:
                        # Update existing agent
                        agent.name = self.name
                        agent.title = self.title or agent.title
                        agent.phone = self.phone
                        agent.description = self.description
                        agent.whatsapp = self.whatsapp
                        agent.instagram = self.instagram
                        agent.linkedin = self.linkedin
                        agent.work_experience = self.work_experience
                        agent.save()
                    logger.info(f"Synced {self.name} with agents app")
            except ImportError:
                pass
            
            # Sync with CRM app if exists
            try:
                from crm.models import CRMRole
                if self.role in ['manager', 'admin'] and self.user:
                    crm_role, created = CRMRole.objects.get_or_create(
                        user=self.user,
                        defaults={'role': 'admin' if self.role == 'admin' else 'manager'}
                    )
                    if not created:
                        crm_role.role = 'admin' if self.role == 'admin' else 'manager'
                        crm_role.save()
                    logger.info(f"Synced {self.name} with CRM app")
            except ImportError:
                pass
                
            # Sync with marketing app if exists
            try:
                from marketing.models import MarketingRole
                if self.role in ['manager', 'admin'] and self.user:
                    marketing_role, created = MarketingRole.objects.get_or_create(
                        user=self.user,
                        defaults={'role': 'admin' if self.role == 'admin' else 'manager'}
                    )
                    if not created:
                        marketing_role.role = 'admin' if self.role == 'admin' else 'manager'
                        marketing_role.save()
                    logger.info(f"Synced {self.name} with marketing app")
            except ImportError:
                pass
                
        except Exception as e:
            logger.error(f"Error syncing {self.name} with other apps: {str(e)}")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('team:team_detail', args=[str(self.id)])


class TeamContactMessage(models.Model):
    team = models.ForeignKey(Team, related_name='contact_messages', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} to {self.team.name}"

    class Meta:
        ordering = ['-created_at']


# Signals for bidirectional sync
@receiver(post_save, sender=Team)
def team_post_save(sender, instance, created, **kwargs):
    """Handle team member save to sync with other apps"""
    if instance.role in ['manager', 'admin']:
        instance.create_or_update_user_account()


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    """Handle user save to sync with team app"""
    if not created:  # Only for existing users
        try:
            # Check if user has team record
            team = Team.objects.filter(user=instance).first()
            if team:
                # Update team info from user
                team.name = f"{instance.first_name} {instance.last_name}".strip() or instance.username
                team.email = instance.email
                
                # Update role based on user permissions
                if instance.is_superuser:
                    team.role = 'admin'
                elif instance.is_staff:
                    team.role = 'manager'
                
                team.save()
            else:
                # Create team record for admin/staff users
                if instance.is_staff or instance.is_superuser:
                    role = 'admin' if instance.is_superuser else 'manager'
                    Team.objects.create(
                        name=f"{instance.first_name} {instance.last_name}".strip() or instance.username,
                        title=f"{role.title()}",
                        description=f"System {role}",
                        email=instance.email,
                        phone="",
                        role=role,
                        user=instance,
                        is_published=True
                    )
        except Exception as e:
            logger.error(f"Error syncing user {instance.username} with team: {str(e)}")


# Reverse sync signals from other apps
def sync_from_agents():
    """Sync data from agents app to team"""    
    try:
        from agents.models import Agent
        
        @receiver(post_save, sender=Agent)
        def agent_post_save(sender, instance, created, **kwargs):
            try:
                team, team_created = Team.objects.get_or_create(
                    email=instance.email,
                    defaults={
                        'name': instance.name,
                        'title': 'Real Estate Agent',
                        'description': instance.description,
                        'photo': instance.photo,
                        'phone': instance.phone,
                        'role': 'manager',
                        'user': instance.user,
                        'is_published': True
                    }
                )
                if not team_created:
                    # Update existing team record
                    team.name = instance.name
                    team.description = instance.description
                    team.phone = instance.phone
                    team.role = 'manager'
                    team.user = instance.user
                    team.is_published = True
                    team.save()
                    
            except Exception as e:
                logger.error(f"Error syncing agent {instance.name} to team: {str(e)}")
                
    except ImportError:
        pass


def sync_from_crm():
    """Sync data from CRM app to team"""
    try:
        from crm.models import CRMUser
        
        @receiver(post_save, sender=CRMUser)
        def crm_user_post_save(sender, instance, created, **kwargs):
            try:
                if instance.user:
                    team, team_created = Team.objects.get_or_create(
                        user=instance.user,
                        defaults={
                            'name': f"{instance.user.first_name} {instance.user.last_name}".strip() or instance.user.username,
                            'title': f"CRM {instance.role.title()}",
                            'description': f"CRM system {instance.role}",
                            'email': instance.user.email,
                            'phone': instance.phone or "",
                            'role': 'admin' if instance.role == 'admin' else 'manager',
                            'hire_date': instance.hire_date,
                            'is_published': instance.is_active
                        }
                    )
                    if not team_created:
                        team.title = f"CRM {instance.role.title()}"
                        team.phone = instance.phone or team.phone
                        team.role = 'admin' if instance.role == 'admin' else 'manager'
                        team.hire_date = instance.hire_date
                        team.is_published = instance.is_active
                        team.save()
                        
            except Exception as e:
                logger.error(f"Error syncing CRM user to team: {str(e)}")
                
    except ImportError:
        pass


# Initialize reverse sync
sync_from_agents()
sync_from_crm()

# Add utility function for receiving CRM transfers
def receive_crm_transfer(transfer_data):
    """Receive customer data from CRM and create team lead/contact"""
    try:
        from crm.models import DataTransfer
        
        transfer_id = transfer_data.get('transfer_id')
        customer_data = transfer_data.get('customer_data')
        
        # Create a team contact message or work note based on the transfer
        # This is where the team app would process incoming customer data
        
        # Update transfer status
        if transfer_id:
            transfer = DataTransfer.objects.get(id=transfer_id)
            transfer.status = 'received'
            transfer.save()
            
        return True
        
    except Exception as e:
        logger.error(f"Error receiving CRM transfer: {str(e)}")
        return False

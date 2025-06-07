from django.db import models
from datetime import datetime
from django.utils.html import format_html

# Create your models here.
class Agent(models.Model):
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='agents/%Y/%m/%d')
    title = models.CharField(max_length=100, default='Real Estate Agent')
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    whatsapp = models.CharField(max_length=30)
    instagram = models.CharField(max_length=100)
    linkedin = models.CharField(max_length=100)
    hire_date = models.DateTimeField(default=datetime.now, blank=True)
    work_experience = models.TextField(
        blank=True,
        help_text="Enter work experience points separated by the '|' character. Each point will be displayed as a separate bullet point on the frontend."
    )

    def work_experience_as_list(self):
        """Returns work_experience as a list of bullet points"""
        return [exp.strip() for exp in self.work_experience.split('|') if exp.strip()]

    def work_experience_as_html(self):
        """Returns work_experience as HTML bullet list"""
        items = self.work_experience_as_list()
        if not items:
            return "-"
        return format_html("<ul>{}</ul>", format_html("".join(f"<li>{item}</li>" for item in items)))

    def __str__(self):
        return self.name


class AgentContact(models.Model):
    agentname = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    user_subject = models.TextField(max_length=200)
    user_phone = models.CharField(max_length=20, null=True, blank=True)
    contact_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user_name} - {self.agentname}"

class AgentPropertyContact(models.Model):
    agentname = models.CharField(max_length=100)
    property_title = models.CharField(max_length=200)
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    user_phone = models.CharField(max_length=20)
    user_subject = models.TextField(max_length=200)
    contact_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user_name} - {self.property_title} - {self.agentname}"

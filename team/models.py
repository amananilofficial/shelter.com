from django.db import models
from datetime import datetime
from django.utils.html import format_html
from django.urls import reverse

# Create your models here.
class Team(models.Model):
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
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)

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

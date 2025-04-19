from django.db import models
from django.utils import timezone


class Project(models.Model):
    """
    Model representing a portfolio project
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    video = models.FileField(upload_to='projects/videos/', blank=True, null=True, 
                          help_text="Upload a video showcasing your project")
    tech_stack = models.CharField(max_length=500, help_text="Comma-separated list of technologies used")
    live_link = models.URLField(max_length=300)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def get_tech_stack_list(self):
        """
        Return tech stack as a list
        """
        return [tech.strip() for tech in self.tech_stack.split(',')]

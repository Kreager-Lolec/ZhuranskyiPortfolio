from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'tech_stack', 'live_link')
    search_fields = ('title', 'description', 'tech_stack')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

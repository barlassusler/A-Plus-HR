from django.contrib import admin
from .models import JobApplication, Position, Location

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'education_level', 'created_at')
    list_filter = ('education_level', 'created_at')
    search_fields = ('full_name', 'phone_number')

admin.site.register(Position)
admin.site.register(Location)

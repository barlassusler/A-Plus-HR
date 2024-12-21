from django.contrib import admin
from biko_hr.models import Application, Position, Location

@admin.register(Application)
class JobApplicationAdmin(admin.ModelAdmin):
    # list_display = ('full_name', 'phone_number', 'education_level', 'created_at')
    # list_filter = ('education_level', 'created_at')
    # search_fields = ('full_name', 'phone_number')
    pass

admin.site.register(Position)
admin.site.register(Location)

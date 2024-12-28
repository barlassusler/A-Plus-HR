from django.contrib import admin
from biko_hr.models import Application, Position, Location, Candidate, IncubationJob

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_birth_date', 'resume', 'applied_positions_display', 'desired_locations_display', 'application_date')

    def get_full_name(self, obj):
        if obj.candidate:
            return f"{obj.candidate.name} {obj.candidate.surname}"
        return None
    get_full_name.short_description = 'Full Name'

    def get_birth_date(self, obj):
        return obj.candidate.birth_date if obj.candidate else None
    get_birth_date.short_description = 'Birth Date'

    def applied_positions_display(self, obj):
        if obj.candidate:
            applications = Application.objects.filter(candidate=obj.candidate)
            return ", ".join([app.job.title for app in applications if app.job])  # `job.title` represents the position name
        return None
    applied_positions_display.short_description = 'Applied Positions'

    def desired_locations_display(self, obj):
        if obj.candidate and obj.candidate.desired_locations.exists():
            return ", ".join([location.name for location in obj.candidate.desired_locations.all()])
        return None
    desired_locations_display.short_description = 'Desired Locations'

    def resume(self, obj):
        return obj.uploaded_resume.name if obj.uploaded_resume else "No Resume Uploaded"
    resume.short_description = 'Resume'


# Diğer modelleri kaydetmek
admin.site.register(Position)
admin.site.register(Location)
admin.site.register(Candidate)
# @admin.register(Application)
# class JobApplicationAdmin(admin.ModelAdmin):
#     # list_display = ('full_name', 'phone_number', 'education_level', 'created_at')
#     # list_filter = ('education_level', 'created_at')
#     # search_fields = ('full_name', 'phone_number')
#     pass


# # Diğer modelleri kaydetmek
# admin.site.register(Position)
# admin.site.register(Location)
# # admin.site.register(Candidate)

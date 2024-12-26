from django.contrib import admin
from .models import Application, Position, Location, Candidate

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_birth_date', 'resume', 'applied_positions_display', 'desired_locations_display', 'application_date')

    def get_full_name(self, obj):
        return obj.candidate.full_name if obj.candidate else None
    get_full_name.short_description = 'Full Name'

    def get_birth_date(self, obj):
        return obj.candidate.birth_date if obj.candidate else None
    get_birth_date.short_description = 'Birth Date'

    def applied_positions_display(self, obj):
        return ", ".join([position.name for position in obj.applied_positions.all()])
    applied_positions_display.short_description = 'Applied Positions'

    def desired_locations_display(self, obj):
        return ", ".join([location.name for location in obj.desired_locations.all()])
    desired_locations_display.short_description = 'Desired Locations'

# Diğer modelleri kaydetmek
admin.site.register(Position)
admin.site.register(Location)
admin.site.register(Candidate)

from django.contrib import admin

from .models import Profile, Project, Project_Avaliacao

"""
class AgendaInline(admin.TabularInline):
    model = Agenda


class AnimalAdmin(admin.ModelAdmin):
    inlines = [
        AgendaInline
    ]
"""

admin.site.register(Profile)
admin.site.register(Project)
"""
admin.site.register(Agenda)
admin.site.register(Animal, AnimalAdmin)
"""
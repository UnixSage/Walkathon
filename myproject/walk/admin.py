from myproject.walk.models import *
from django.contrib import admin

class PersonAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'email', 'uuid']
    list_display = ['first_name', 'last_name', 'email', 'uuid']

admin.site.register(Team)
admin.site.register(Person, PersonAdmin)

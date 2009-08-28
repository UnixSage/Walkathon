from walk.models import *
from django.contrib import admin

class PersonAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name', 'email', 'uuid']
    list_display = ['first_name', 'last_name', 'email', 'uuid']

class SponsorAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name']
    list_display = ['walker', 'first_name', 'last_name', 'amount', 'paid']

admin.site.register(Team)
admin.site.register(Person, PersonAdmin)
admin.site.register(Sponsor, SponsorAdmin)

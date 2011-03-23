from django.contrib import admin
from reference.models import Citizenship

class CitizenshipAdmin(admin.ModelAdmin):
    pass

admin.site.register(Citizenship,CitizenshipAdmin)
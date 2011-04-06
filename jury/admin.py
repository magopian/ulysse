#-*- coding: utf-8 -*- 
from django.contrib import admin
from jury.models import Jury

class JuryAdmin(admin.ModelAdmin):
    list_display        = ('id','last_name', 'first_name','email')
    list_display_links  = ('last_name',)
    search_fields       = ['user__last_name','user__first_name','user__email']

def register(site):
    site.register(Jury,JuryAdmin)
    
# Global admin registration
admin.site.register(Jury,JuryAdmin)
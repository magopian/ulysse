#-*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import StackedInline
from django.contrib.admin import TabularInline
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User
from composers.models import Composer
from composers.models import Work
from composers.models import BiographicElement
from composers.models import AdministrativeDocument
from composers.models import Work
from composers.models import MediaType

import competitions

class BiographicElementInline(TabularInline):
    model = BiographicElement
    
class AdministrativeDocumentInline(TabularInline):
    model = AdministrativeDocument


class ComposerAdmin(ModelAdmin):
    list_display        = ('id','nom_','prenom_','birth_date','zipcode','city')
    list_display_links  = ('id','nom_',)    
    search_fields       = ['user__last_name','user__first_name','user__email']
    inlines             = [BiographicElementInline,AdministrativeDocumentInline]
    

    fieldsets = (
        ('Etat-civil', {
            'classes': ('wide',),
            'fields': ('user','birth_date','citizenship')                
        }),        
        ('Adresse postale', {
            'classes': ('wide',),
            'fields': ('address1','address2','zipcode','city','country','phone1','phone2')                
        }),        
    )
    
    class Media:
            js = (
            '/static/js/tiny_mce/tiny_mce.js',
            '/static/js/admin_pages.js'
        )
    

class WorkAdmin(ModelAdmin):
    list_display        = ('composer','title')
    list_display_links  = ('title',)
    list_filter         = ['composer',]
    search_fields       = ['composer__user__last_name','title']


def register(site):
    site.register(Composer,ComposerAdmin)
    site.register(Work,WorkAdmin)

# Global administration registration    
admin.site.register(Composer,ComposerAdmin)
admin.site.register(Work,WorkAdmin)
    


from django.contrib import admin
from compositeurs.models import Composer
from compositeurs.models import BiographicElement
from compositeurs.models import Media

class ComposerAdmin(admin.ModelAdmin):
    list_display       = ('id','last_name', 'first_name','email')
    list_display_links  = ('last_name',)
    search_fields = ['user__last_name','user__first_name','user__email']
    

class BiographicElementAdmin(admin.ModelAdmin):
    pass

class MediaAdmin(admin.ModelAdmin):
    pass


admin.site.register(Composer,ComposerAdmin)
admin.site.register(BiographicElement,BiographicElementAdmin)
admin.site.register(Media,MediaAdmin)
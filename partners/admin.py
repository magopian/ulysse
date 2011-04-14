from django.contrib import admin
from partners.models import Partner

class PartnerAdmin(admin.ModelAdmin):
    list_display  = ['name',]
    search_fields = ["name",]
    
    class Media:
            js = (
            '/static/js/tiny_mce/tiny_mce.js',
            '/static/js/admin_pages.js'
        )
    
# Global admin registration
admin.site.register(Partner,PartnerAdmin)

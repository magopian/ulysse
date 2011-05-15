from django.conf import settings
from django.contrib import admin
from partners.models import Partner

class PartnerAdmin(admin.ModelAdmin):
    list_display  = ['name',]
    search_fields = ["name",]
    
    class Media:
            js = (
            '%sjs/tiny_mce/tiny_mce.js' % settings.STATIC_URL,
            '%sjs/admin_pages.js' % settings.STATIC_URL
        )
    
# Global admin registration
admin.site.register(Partner,PartnerAdmin)

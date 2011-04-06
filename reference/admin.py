from django.contrib import admin
from reference.models import Citizenship
from reference.models import MediaType
from reference.models import BiographicElementType

class CitizenshipAdmin(admin.ModelAdmin):
    pass

class BiographicElementTypeAdmin(admin.ModelAdmin):
    pass

class MediaTypeAdmin(admin.ModelAdmin):
    pass

# Global admin registration
admin.site.register(Citizenship,CitizenshipAdmin)
admin.site.register(BiographicElementType,BiographicElementTypeAdmin)
admin.site.register(MediaType,MediaTypeAdmin)
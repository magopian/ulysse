from django.contrib import admin
from reference.models import Citizenship
from reference.models import MediaType
from reference.models import DocumentType,TextElementType

class CitizenshipAdmin(admin.ModelAdmin):
    pass

class TextElementTypeAdmin(admin.ModelAdmin):
    pass

class DocumentTypeAdmin(admin.ModelAdmin):
    pass

class MediaTypeAdmin(admin.ModelAdmin):
    pass

# Global admin registration
admin.site.register(Citizenship,CitizenshipAdmin)
admin.site.register(DocumentType,DocumentTypeAdmin)
admin.site.register(TextElementType,TextElementTypeAdmin)
admin.site.register(MediaType,MediaTypeAdmin)
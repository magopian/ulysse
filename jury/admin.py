from django.contrib import admin
from jury.models import JuryMember

class JuryMemberAdmin(admin.ModelAdmin):
    list_display        = ('id','last_name', 'first_name','email')
    list_display_links  = ('last_name',)
    search_fields       = ['user__last_name','user__first_name','user__email']


admin.site.register(JuryMember,JuryMemberAdmin)


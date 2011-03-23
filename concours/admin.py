from django.contrib import admin
from concours.models import Partner
from concours.models import ApplicationForm
from concours.models import EvaluationModel
from concours.models import Competition
from concours.models import CompetitionStep
from concours.models import CompetitionNews
from concours.models import Candidate
from concours.models import CandidateGroup
from concours.models import JuryMemberGroup
from concours.models import Evaluation

class PartnerAdmin(admin.ModelAdmin):
    list_display  = ['name',]
    search_fields = ["name",]
    

class ApplicationFormAdmin(admin.ModelAdmin):
    pass

class EvaluationModelAdmin(admin.ModelAdmin):
    pass

class CompetitionAdmin(admin.ModelAdmin):
    search_fields  = ["title"]
    list_display   = ('title','subtitle','partner','opening_date','closing_date','is_published','is_open')
    list_filter    = ["partner",]
    

class CompetitionStepAdmin(admin.ModelAdmin):
    pass

class CompetitionNewsAdmin(admin.ModelAdmin):
    pass

class CandidateAdmin(admin.ModelAdmin):    
    list_display   = ('composer','competition')
    list_filter    = ["competition",]

class CandidateGroupAdmin(admin.ModelAdmin):
    pass

class JuryMemberGroupAdmin(admin.ModelAdmin):
    pass

class EvaluationAdmin(admin.ModelAdmin):
    pass

admin.site.register(JuryMemberGroup,JuryMemberGroupAdmin)
admin.site.register(Partner,PartnerAdmin)
admin.site.register(ApplicationForm,ApplicationFormAdmin)
admin.site.register(EvaluationModel,EvaluationModelAdmin)
admin.site.register(Evaluation,EvaluationAdmin)
admin.site.register(Competition,CompetitionAdmin)
admin.site.register(CompetitionStep,CompetitionStepAdmin)
admin.site.register(CompetitionNews,CompetitionNewsAdmin)
admin.site.register(Candidate,CandidateAdmin)
admin.site.register(CandidateGroup,CandidateGroupAdmin)

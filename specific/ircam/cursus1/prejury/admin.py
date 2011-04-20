from django.contrib import admin
from competitions.admin import CandidateJuryAllocationAdmin
from competitions.admin import CompetitionStepFollowUpAdmin
from competitions.admin import CompetitionStepResultsAdmin

class CandidateJuryAllocationIrcamCursus1PreJuryAdmin(CandidateJuryAllocationAdmin):
    pass

class CompetitionStepResultsIrcamCursus1PreJuryAdmin(CompetitionStepResultsAdmin):
    pass

class CompetitionStepFollowUpIrcamCursus1PreJuryAdmin(CompetitionStepFollowUpAdmin):
    pass

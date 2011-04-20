from django.contrib import admin
from competitions.admin import CandidateJuryAllocationAdmin
from competitions.admin import CompetitionStepFollowUpAdmin
from competitions.admin import CompetitionStepResultsAdmin

class CandidateJuryAllocationIrcamCursus1JuryAdmin(CandidateJuryAllocationAdmin):
    pass

class CompetitionStepResultsIrcamCursus1JuryAdmin(CompetitionStepResultsAdmin):
    pass

class CompetitionStepFollowUpIrcamCursus1JuryAdmin(CompetitionStepFollowUpAdmin):
    pass

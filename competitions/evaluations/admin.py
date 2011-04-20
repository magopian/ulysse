#-*- coding: utf-8 -*-
from django.contrib import admin
from models import EvaluationNote
from models import EvaluationYesNo
from models import EvaluationYesNoAndNote

class EvaluationYesNoAndNoteAdmin(admin.ModelAdmin):
    list_filter  = ['yes','candidate','jury_member']
    list_display  = ('candidate','jury_member','yes','note','comments')

class EvaluationYesNoAdmin(admin.ModelAdmin):
    list_filter  = ['yes','candidate','jury_member']
    list_display  = ('candidate','jury_member','yes','comments')
    
class EvaluationNoteAdmin(admin.ModelAdmin):
    list_filter  = ['note','candidate','jury_member']
    list_display  = ('candidate','jury_member','note','comments')
    

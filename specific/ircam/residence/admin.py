#-*- coding: utf-8 -*-

from django.contrib import admin
from models import EvaluationResidence

class EvaluationResidenceAdmin(admin.ModelAdmin):
    list_filter  = ['note','candidate','jury_member']
    list_display  = ('candidate','jury_member','note','comments')

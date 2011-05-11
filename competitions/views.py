from django.shortcuts import render_to_response
from django.template import RequestContext
from competitions.models import Competition, CompetitionManager

def import_candidates(request):
    params = {}
    return render_to_response('admin/import_candidates.html',params,context_instance=RequestContext(request))
    
def notify_jury_members(request):
    params = {}
    return render_to_response('admin/notify_jury_members.html',params,context_instance=RequestContext(request))
#-*- coding: utf-8 -*-
from session import get_active_competition, get_jury_member
from django.utils.translation import ugettext as _
                    
def in_competition_admin(request):
    return request.path.startswith("/admin")

def ulysse_context_processor(request):        
    results = {}
    results["in_competition_admin"]  = in_competition_admin(request)
    results["is_user_authenticated"] = request.user.is_authenticated()
    competition = get_active_competition(request)
    if competition:
        results["active_competition"]  = competition
        results["admin_title"]         = _("Administrate competition \"%s\"") % competition
        results["nav_buttons"]         = competition.get_menu(request)        
    results["jury_member"] = get_jury_member(request)
    return results

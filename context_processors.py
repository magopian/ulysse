#-*- coding: utf-8 -*- 
from competitions.session import get_active_competition
                    
def ulysse_context_processor(request):    
    competition = get_active_competition(request)
    results = {}
    if competition:        
        results["active_competition"]  = competition
        results["admin_title"]         = "Administration concours \"%s\"" % competition        
        results["nav_buttons"]         = competition.get_menu(request)        
    return results
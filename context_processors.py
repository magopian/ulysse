from concours import get_active_competition

def ulysse_context_processor(request):    
    competition = get_active_competition(request)
    results = {}
    if competition:
        results["active_competition"]  = competition
        results["admin_title"]         = "Administration concours \"%s\"" % competition    
    return results
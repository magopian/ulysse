from competitions.models import Competition

ACTIVE_COMPETITION_KEY = "active_competition"

def get_active_competition(request):    
    if not request.session.__contains__(ACTIVE_COMPETITION_KEY ):
        return None
    active_competition = request.session[ACTIVE_COMPETITION_KEY ]
    if not type(active_competition) is Competition:
        return None
    return active_competition

def set_active_competition(request,id):    
    request.session[ACTIVE_COMPETITION_KEY] = Competition.objects.get(id=id)
    
def clear_active_competition(request):    
    request.session[ACTIVE_COMPETITION_KEY] = None
    
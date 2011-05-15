from competitions.models import Competition

ACTIVE_COMPETITION_KEY = "active_competition"
JURY_MEMBER_KEY = "jury_member"

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
    
def get_jury_member(request):
    return request.session.get(JURY_MEMBER_KEY, False)

def set_jury_member(request):
    request.session[JURY_MEMBER_KEY] = True

def clear_jury_member(request):
    if JURY_MEMBER_KEY in request.session:
        del request.session[JURY_MEMBER_KEY]

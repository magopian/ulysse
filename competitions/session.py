

def get_active_competition(request):
    from competitions.models import Competition
    return Competition.objects.filter(id=1)[0]
    #if not request.session.__contains__("active_competition"):
    #    return None
    #active_competition = request.session["active_competition"]
    #if not type(active_competition) is Competition:
    #    return None
    #return active_competition
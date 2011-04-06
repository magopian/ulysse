

def get_active_competition(request):
    path = request.META["PATH_INFO"]
    tokens = path.split('/')
    competition_url = tokens[2]
    from concours.models  import Competition
    competitions = Competition.objects.filter(url=competition_url)
    if len(competitions)==1:
        return competitions[0]
    else:
        return None        

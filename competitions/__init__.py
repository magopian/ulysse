#-*- coding: utf-8 -*- 
from sites   import CompetitionAdminSite

def get_active_competition(request):
    path = request.META["PATH_INFO"]
    tokens = path.split('/')
    competition_url = tokens[1]
    from models  import Competition
    competitions = Competition.objects.filter(url=competition_url)
    if len(competitions)==1:
        return competitions[0]
    else:
        return None
    
def get_active_step(request):
    path = request.META["PATH_INFO"]
    tokens = path.split('/')
    step = None
    if len(tokens)>=4:
        if tokens[2]=='step':
            from models  import Competition
            from models  import CompetitionStep
            competition_url = tokens[1]        
            step_url        = tokens[3]            
            competition  = Competition.objects.filter(url=competition_url)[0]
            step         = CompetitionStep.objects.filter(competition=competition,url=step_url)[0]            
    return step


# ==============================
#
# Parameters for 'Ircam Residence'
#
# ===============================


ircam_residence_2011 = CompetitionAdminSite(name="ircam_residence_2011")


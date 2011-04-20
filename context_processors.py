#-*- coding: utf-8 -*- 
from competitions import get_active_competition
from competitions import get_active_step
from competitions.sites import REDIRECTIONS

def get_original_path(path):
    # Check whether we are redirected or not. If we are, get original path
    REDIRECTIONS_REVERSE = dict((v,k) for k,v in REDIRECTIONS.iteritems())
    tokens = path.split('/')
    result = path
    if len(tokens)>3:
        search_key = "/".join(tokens[2:])        
        if REDIRECTIONS_REVERSE.has_key(search_key):
            result = "/%s/%s" % (tokens[1],REDIRECTIONS_REVERSE[search_key])    
    return result
    

def get_current_page_infos(request):
    path = request.META["PATH_INFO"]
    path = get_original_path(path)    
    tokens = path.split('/')    
    competition = len(tokens)>=2 and tokens[1] or None
    tab         = len(tokens)>=3 and tokens[2] or None
    param1      = len(tokens)>=4 and tokens[3] or None
    param2      = len(tokens)>=5 and tokens[4] or None
    return (competition,tab,param1,param2)

def get_nav_button_level2(request,url,label):
    (competition,tab,param1,param2) = get_current_page_infos(request)    
    is_selected = (url == ("%s/%s/%s") % (tab,param1,param2))
    return {'url':url,'label':label,'is_selected':is_selected}

def get_nav_button(request,url,label):    
    (competition,tab,param1,param2) = get_current_page_infos(request)    
    if tab=='step':        
        is_selected = (url=="%s/%s" % (tab,param1))
    else:
        is_selected = (url==tab)
    # Is step ? Add children button
    children = []
    if tab == 'step':
        step_name = param1
        children.append(get_nav_button_level2(request,"step/%s/allocations" % step_name,u"Affectations candidats-jury"))
        children.append(get_nav_button_level2(request,"step/%s/evaluations" % step_name,u"Suivi des évaluations"))
        children.append(get_nav_button_level2(request,"step/%s/results" % step_name,u"Suivi des résultats"))
    return {'url':url,'label':label,'is_selected':is_selected,'children':children}

def get_nav_buttons(request,competition):
    nav_buttons = []    
    nav_buttons.append(get_nav_button(request,"infos","Informations"))
    nav_buttons.append(get_nav_button(request,"candidates","Candidats"))
    nav_buttons.append(get_nav_button(request,"jury","Membres du jury"))
    # Add step dynamically
    for step in competition.steps():
        nav_buttons.append(get_nav_button(request,"step/%s" % step.url,"Etape : '%s'" % step.name))        
    return nav_buttons
                       

def ulysse_context_processor(request):    
    competition = get_active_competition(request)
    results = {}
    if competition:        
        results["active_competition"]  = competition
        results["admin_title"]         = "Administration concours \"%s\"" % competition
        nav_buttons                    =  get_nav_buttons(request,competition)
        results["nav_buttons"]  = nav_buttons        
        results["active_step"] = get_active_step(request)
    return results
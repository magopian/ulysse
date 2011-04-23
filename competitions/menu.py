#-*- coding: utf-8 -*- 

def get_current_page_infos(request):
    path = request.META["PATH_INFO"]    
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
        children.append(get_nav_button_level2(request,"step/%s/allocations/" % step_name,u"Affectations candidats-jury"))
        children.append(get_nav_button_level2(request,"step/%s/evaluations/" % step_name,u"Suivi des évaluations"))
        children.append(get_nav_button_level2(request,"step/%s/results/" % step_name,u"Suivi des résultats"))
    return {'url':url,'label':label,'is_selected':is_selected,'children':children}
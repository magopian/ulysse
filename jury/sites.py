from django.contrib.admin.sites import AdminSite

class JuryAdminSite(AdminSite):
    index_template = "jury/index.html"
    login_template = "jury/login.html"
    
    
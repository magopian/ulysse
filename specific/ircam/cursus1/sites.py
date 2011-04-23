from django.conf.urls.defaults import patterns, url, include
from competitions.sites import CompetitionAdminSite
from models import CandidateCursus1
from admin import CandidateCursus1Admin


class Cursus1AdminSite(CompetitionAdminSite):
    
        
    def get_urls(self):
        
        urls = super(Cursus1AdminSite,self).get_urls()           
        
        my_urls = patterns('',                        
            (r'^candidates/', include(self._registry[CandidateCursus1].urls)) ,           
        )
        
        return my_urls + urls
            
    def get_steps(self):
        return ["pre-jury","jury"]
    
    def register_models(self):
        # Call base class (register common models)
        super(Cursus1AdminSite,self).register_models()
        # Register specific models
        self.register(CandidateCursus1,CandidateCursus1Admin)                        




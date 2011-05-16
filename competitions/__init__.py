
from sites import CompetitionAdminSite

admin_site = CompetitionAdminSite(name="competition_admin")
admin_site.register_models()


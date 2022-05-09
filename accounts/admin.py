from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib.auth.models import Group

from sbs.models import ClubRole
from sbs.models.ekabis.Country import Country
from sbs.models.ekabis.City import City
from sbs.models.tvfbf.Branch import Branch
from sbs.models.tvfbf.DocumentName import DocumentName
from sbs.models.tvfbf.SportClubUser import SportClubUser
from sbs.models.tvfbf.Referee import Referee
from sbs.models.tvfbf.Coach import Coach
from sbs.models.ekabis.Person import Person
from sbs.models.ekabis.Menu import Menu

admin.site.site_header = 'Kobiltek Bilisim Kullanici Yönetim Paneli '  # default: "Django Administration"
admin.site.index_title = 'Sistem Yönetimi'  # default: "Site administration"
admin.site.site_title = 'Admin'  # default: "Django site admin"

admin.site.register(SportClubUser)
admin.site.register(Referee)
admin.site.register(Person)
admin.site.register(Coach)
admin.site.register(Menu)
admin.site.register(Branch)
admin.site.register(City)
admin.site.register(Country)
admin.site.register(DocumentName)
admin.site.register(ClubRole)


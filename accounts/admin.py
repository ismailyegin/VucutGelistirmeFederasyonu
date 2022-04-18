from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

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

import traceback

from django.contrib.auth.models import User, Group
from django.db import transaction
from django.db.models import Q
from django.urls import resolve

from sbs.models.ekabis.Permission import Permission
from sbs.models.ekabis.Logs import Logs
from sbs.models.ekabis.ActiveGroup import ActiveGroup
from sbs.models.ekabis.CategoryItem import CategoryItem
from sbs.models.ekabis.City import City
from sbs.models.ekabis.Communication import Communication
from sbs.models.ekabis.Country import Country
from sbs.models.tvfbf.DirectoryCommission import DirectoryCommission
from sbs.models.tvfbf.DirectoryMember import DirectoryMember
from sbs.models.tvfbf.DirectoryMemberRole import DirectoryMemberRole
from sbs.models.ekabis.HelpMenu import HelpMenu
from sbs.models.ekabis.Menu import Menu
from sbs.models.ekabis.PermissionGroup import PermissionGroup
from sbs.models.ekabis.Person import Person
from sbs.models.ekabis.Settings import Settings


def CityService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                filter['isDeleted'] = False
                return City.objects.filter(**filter)
            else:
                return City.objects.filter(filter, isDeleted=False)
        else:
            return City.objects.filter(isDeleted=False)
    except City.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()













def UserService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):

                return User.objects.filter(**filter)
            else:
                return User.objects.filter(filter)
        else:
            return User.objects.all()
    except User.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()
        print(e)
        pass


def GroupService(request, filter):
    try:
        if filter:
            return Group.objects.filter(**filter)
        else:
            return Group.objects.all()
    except Group.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def PersonService(request, filter):
    try:
        if filter:
            filter['isDeleted'] = False
            return Person.objects.filter(**filter)
        else:
            return Person.objects.filter(isDeleted=False)
    # except Person.DoesNotExist:
    #     return None
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def CommunicationService(request, filter):
    try:
        if filter:
            filter['isDeleted'] = False
            return Communication.objects.filter(**filter)
        else:
            return Communication.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def CategoryItemService(request, filter):
    try:
        if filter:
            filter['isDeleted'] = False
            return CategoryItem.objects.filter(**filter)
        else:
            return CategoryItem.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass




def DirectoryMemberService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                filter['isDeleted'] = False
                return DirectoryMember.objects.filter(**filter)
            else:
                return DirectoryMember.objects.filter(filter, isDeleted=False)
        else:
            return DirectoryMember.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def DirectoryCommissionService(request, filter):
    try:
        if filter:
            filter['isDeleted'] = False
            return DirectoryCommission.objects.filter(**filter)
        else:
            return DirectoryCommission.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def DirectoryMemberRoleService(request, filter):
    try:
        with transaction.atomic():

            if filter:
                filter['isDeleted'] = False
                return DirectoryMemberRole.objects.filter(**filter)
            else:
                return DirectoryMemberRole.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()
        print(e)
        pass




def LogsService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                filter['isDeleted'] = False
                return Logs.objects.filter(**filter)
            else:
                return Logs.objects.filter(filter, isDeleted=False)
        else:
            return Logs.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass


def MenuService(request, filter):
    try:
        if filter:
            filter['isDeleted'] = False
            return Menu.objects.filter(**filter)
        else:
            return Menu.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass




def ActiveGroupService(request, filter):
    try:
        if filter:
            filter['isDeleted'] = False
            return ActiveGroup.objects.filter(**filter)
        else:
            return ActiveGroup.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass




def PermissionService(request, filter):
    try:
        if filter:
            filter['isDeleted'] = False
            return Permission.objects.filter(**filter)
        else:
            return Permission.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()

        print(e)
        pass






def PermissionGroupService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                filter['isDeleted'] = False
                return PermissionGroup.objects.filter(**filter)
            else:
                return PermissionGroup.objects.filter(filter, isDeleted=False)
        else:
            return PermissionGroup.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()


def SettingsService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                return Settings.objects.filter(**filter)
            else:
                return Settings.objects.filter(filter)
        else:
            return Settings.objects.all()
    except Exception as e:
        traceback.print_exc()









# get servisler


def UserGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:

                return User.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass






def SettingsGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:

                return Settings.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def PersonGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return Person.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def PermissionGetService(request, filter, isDeleted=False):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return Permission.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def PermissionGroupGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return PermissionGroup.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass




def UserGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return User.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def MenuGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return Menu.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def LogsGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return Logs.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass









def DirectoryCommissionGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return DirectoryCommission.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def DirectoryMemberRoleGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return DirectoryMemberRole.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def DirectoryMemberGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return DirectoryMember.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass








def HelpMenuGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return HelpMenu.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass








def CommunicationGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return Communication.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass








def CountryGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return Country.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def CityGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return City.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def CategoryItemGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return CategoryItem.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass








def ActiveGroupGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return ActiveGroup.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def GroupGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                return Group.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def GroupExcludeService(request, filter):
    try:
        with transaction.atomic():
            if filter:

                return Group.objects.exclude(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()






def last_urls(request):
    try:
        urls = []
        from urllib.parse import urlparse
        from sbs.urls import urlpatterns

        last_url_name = ""
        current_url_name = resolve(request.path_info).url_name
        with transaction.atomic():
            if request.META.get('HTTP_REFERER'):
                urlpath = urlparse(request.META.get('HTTP_REFERER')).path
                hostname = urlparse(request.META.get('HTTP_REFERER')).hostname
                for urlpattern in urlpatterns:

                    if urlpattern.name == resolve(urlparse(request.META.get('HTTP_REFERER')).path).url_name:
                            last_url_name = urlpattern.name
                            break

                urlx = {
                    'last': request.META.get('HTTP_REFERER'),
                    'last_url_name': Permission.objects.get(codename=last_url_name).name,
                    # 'current': request.get_full_path(),
                    # 'current_name': Permission.objects.get(codename=current_url_name).name,
                }
                urls.append(urlx)

            else:
                url = {
                    'last': '',
                    # 'current': request.get_full_path(),
                    # 'current_name': Permission.objects.get(codename=current_url_name).name,
                }
                urls.append(url)

            return urls
    except Exception as e:
        traceback.print_exc()
        pass


def validate_file_extension(value):  # Aday YEKA eklerken sadece kml ve kmz dosyalar??n?? kay??t etmek
    import os
    from django.core.exceptions import ValidationError
    file_size = 0
    if Settings.objects.filter(key='file_size'):
        file_size = Settings.objects.get(key='file_size').value
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.kml', '.kmz']
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            'Sadece .kml ve .kmz uzant??l?? dosya y??kleyebilirsiniz.')
    if value.size > float(file_size) * 1024 * 1024:
        raise ValidationError(
            'Maksimum y??klenmesi gereken dosya boyutu: ' + file_size + ' MB')
def validate_file_size(value):  # dosya boyutu kontrol??
    from django.core.exceptions import ValidationError
    file_size = 0
    if Settings.objects.filter(key='file_size'):
        file_size = Settings.objects.get(key='file_size').value
    if value.size > float(file_size) * 1024 * 1024:
        raise ValidationError('Dosya Boyutu B??y??k.(Maksimum y??klenmesi gereken dosya boyutu: ' + file_size + ' MB')



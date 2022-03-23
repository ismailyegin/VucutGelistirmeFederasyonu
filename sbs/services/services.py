import traceback

from django.contrib.auth.models import User, Group
from django.db import transaction
from django.db.models import Q
from django.urls import resolve

from sbs.models.ekabis.Permission import Permission
from sbs.models.ekabis.Logs import Logs
from sbs.models.ekabis.ActiveGroup import ActiveGroup
from sbs.models.ekabis.AssociateDegreeFile import AssociateDegreeFile
from sbs.models.ekabis.AssociateDegreeFileName import AssociateDegreeFileName
from sbs.models.ekabis.BusinessBlog import BusinessBlog
from sbs.models.ekabis.BusinessBlogParametreType import BusinessBlogParametreType
from sbs.models.ekabis.Calendar import Calendar
from sbs.models.ekabis.CalendarName import CalendarName
from sbs.models.ekabis.CategoryItem import CategoryItem
from sbs.models.ekabis.City import City
from sbs.models.ekabis.Claim import Claim
from sbs.models.ekabis.Communication import Communication
from sbs.models.ekabis.Company import Company
from sbs.models.ekabis.CompanyFileNames import CompanyFileNames
from sbs.models.ekabis.CompanyFiles import CompanyFiles
from sbs.models.ekabis.CompanyUser import CompanyUser
from sbs.models.ekabis.Competition import Competition
from sbs.models.ekabis.CompetitionApplication import CompetitionApplication
from sbs.models.ekabis.CompetitionCompany import CompetitionCompany
from sbs.models.ekabis.ConnectionRegion import ConnectionRegion
from sbs.models.ekabis.ConnectionUnit import ConnectionUnit
from sbs.models.ekabis.Country import Country
from sbs.models.tvfbf.DirectoryCommission import DirectoryCommission
from sbs.models.tvfbf.DirectoryMember import DirectoryMember
from sbs.models.tvfbf.DirectoryMemberRole import DirectoryMemberRole
from sbs.models.ekabis.Employee import Employee
from sbs.models.ekabis.ExtraTime import ExtraTime
from sbs.models.ekabis.ExtraTimeFile import ExtraTimeFile
from sbs.models.ekabis.Factory import Factory
from sbs.models.ekabis.FactoryFile import FactoryFile
from sbs.models.ekabis.FactoryFileName import FactoryFileName
from sbs.models.ekabis.HelpMenu import HelpMenu
from sbs.models.ekabis.HistoryGroup import HistoryGroup
from sbs.models.ekabis.Menu import Menu
from sbs.models.ekabis.Newspaper import Newspaper
from sbs.models.ekabis.Notification import Notification
from sbs.models.ekabis.PermissionGroup import PermissionGroup
from sbs.models.ekabis.Person import Person
from sbs.models.ekabis.Settings import Settings
from sbs.models.ekabis.VacationDay import VacationDay
from sbs.models.ekabis.Yeka import Yeka
from sbs.models.ekabis.YekaApplicationFile import YekaApplicationFile
from sbs.models.ekabis.YekaApplicationFileName import YekaApplicationFileName
from sbs.models.ekabis.YekaBusinessBlog import YekaBusinessBlog
from sbs.models.ekabis.YekaBusinessBlogParemetre import YekaBusinessBlogParemetre
from sbs.models.ekabis.YekaBussiness import YekaBusiness
from sbs.models.ekabis.YekaCompany import YekaCompany
from sbs.models.ekabis.YekaCompanyHistory import YekaCompanyHistory
from sbs.models.ekabis.YekaCompetition import YekaCompetition
from sbs.models.ekabis.YekaCompetitionPerson import YekaCompetitionPerson
from sbs.models.ekabis.YekaConnectionRegion import YekaConnectionRegion
from sbs.models.ekabis.YekaPerson import YekaPerson


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


def YekaCompanyService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                filter['isDeleted'] = False
                return YekaCompany.objects.filter(**filter)
            else:
                return YekaCompany.objects.filter(filter, isDeleted=False)
        else:
            return YekaCompany.objects.filter(isDeleted=False)
    except YekaCompany.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()


def YekaPersonService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                filter['isDeleted'] = False
                return YekaPerson.objects.filter(**filter)
            else:
                return YekaPerson.objects.filter(filter, isDeleted=False)
        else:
            return YekaPerson.objects.filter(isDeleted=False)
    except YekaPerson.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()


def YekaCompetitionService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                filter['isDeleted'] = False
                return YekaCompetition.objects.filter(**filter)
            else:
                return YekaCompetition.objects.filter(filter, isDeleted=False)
        else:
            return YekaCompetition.objects.filter(isDeleted=False)
    except YekaCompetition.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()


def YekaConnectionRegionService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                filter['isDeleted'] = False
                return YekaConnectionRegion.objects.filter(**filter)
            else:
                return YekaConnectionRegion.objects.filter(filter, isDeleted=False)
        else:
            return YekaConnectionRegion.objects.filter(isDeleted=False)
    except YekaConnectionRegion.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()


def ConnectionRegionService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                filter['isDeleted'] = False
                filter['yeka__isDeleted'] = False
                return ConnectionRegion.objects.filter(**filter)
            else:
                return ConnectionRegion.objects.filter(filter, isDeleted=False, yeka__isDeleted=False)
        else:
            return ConnectionRegion.objects.filter(isDeleted=False, yeka__isDeleted=False)
    except ConnectionRegion.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()


def ExtraTimeService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                filter['isDeleted'] = False
                return ExtraTime.objects.filter(**filter)
            else:
                return ExtraTime.objects.filter(filter, isDeleted=False)
        else:
            return ExtraTime.objects.filter(isDeleted=False)
    except ExtraTime.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()


def CalendarNameService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                filter['isDeleted'] = False
                return CalendarName.objects.filter(**filter)
            else:
                return CalendarName.objects.filter(filter, isDeleted=False)
        else:
            return CalendarName.objects.filter(isDeleted=False)
    except CalendarName.DoesNotExist:
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


def CompanyService(request, filter):
    try:
        if filter:
            filter['isDeleted'] = False
            return Company.objects.filter(**filter)

        else:
            return Company.objects.filter(isDeleted=False)
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


def EmployeeService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                filter['isDeleted'] = False
                return Employee.objects.filter(**filter)
            else:
                Employee.objects.filter(filter, isDeleted=False)
        else:
            return Employee.objects.filter(isDeleted=False)
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


def NotificationService(request, filter):
    try:
        if filter:
            filter['isDeleted'] = False
            return Notification.objects.filter(**filter)
        else:
            return Notification.objects.filter(isDeleted=False)
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


def YekaCompetitionPersonService(request, filter):
    try:
        if filter:
            filter['isDeleted'] = False
            return YekaCompetitionPerson.objects.filter(**filter)
        else:
            return YekaCompetitionPerson.objects.filter(isDeleted=False)
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


def CompanyFileNamesService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return CompanyFileNames.objects.filter(**filter)
            else:
                return CompanyFileNames.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()
        pass


def ClaimService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                filter['isDeleted'] = False
                return Claim.objects.filter(**filter)
            else:
                return Claim.objects.filter(filter, isDeleted=False)
        else:
            return Claim.objects.filter(isDeleted=False)
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


def UnitService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return ConnectionUnit.objects.filter(**filter)
            else:
                return ConnectionUnit.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()
        print(e)
        pass


def RegionService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return ConnectionRegion.objects.filter(**filter)
            else:
                return ConnectionRegion.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()
        print(e)
        pass


def ExtraTimeFileService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return ExtraTimeFile.objects.filter(**filter)
            else:
                return ExtraTimeFile.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()
        print(e)
        pass


def YekaService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return Yeka.objects.filter(**filter)
            else:
                return Yeka.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()
        pass


# get servisler
def YekaGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return Yeka.objects.get(**filter)
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


def YekaPersonGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return YekaPerson.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def YekaConnectionRegionGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return YekaConnectionRegion.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def YekaCompanyGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return YekaCompany.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def YekaCompanyHistoryGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return YekaCompanyHistory.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def YekaBusinessGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return YekaBusiness.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def YekaBusinessBlogGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return YekaBusinessBlog.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def YekaBusinessBlogParemetreGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return YekaBusinessBlogParemetre.objects.get(**filter)
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


def NotificationGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return Notification.objects.get(**filter)
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


def HistoryGroupGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return HistoryGroup.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def ExtraTimeFileGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return ExtraTimeFile.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def ExtraTimeGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return ExtraTime.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def EmployeeGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return Employee.objects.get(**filter)
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


def ConnectionUnitGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return ConnectionUnit.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def ConnectionRegionGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return ConnectionRegion.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def CompanyUserGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return CompanyUser.objects.get(**filter)
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


def CompanyFilesGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return CompanyFiles.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def CompanyFileNamesGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return CompanyFileNames.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def CompanyGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return Company.objects.get(**filter)
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


def YekaCompetitionPersonGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return YekaCompetitionPerson.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def YekaCompetitionGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return YekaCompetition.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def ClaimGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return Claim.objects.get(**filter)
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


def CalendarNameGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return CalendarName.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def CalendarGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return Calendar.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def BusinessBlogGetService(request, filter):
    try:
        with transaction.atomic():

            if filter:
                filter['isDeleted'] = False
                return BusinessBlog.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def BusinessBlogParametreTypeGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return BusinessBlogParametreType.objects.get(**filter)
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


def VacationDayGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return VacationDay.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def VacationDayService(request, filter):
    try:
        with transaction.atomic():

            if filter:
                filter['isDeleted'] = False
                return VacationDay.objects.filter(**filter)
            else:
                return VacationDay.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()
        pass


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
                # if hostname == 'kobiltek.com':
                #     url = urlpath.split('/yekabis/yekabis/')[1]
                # else:
                url = urlpath.split('/havasporlari/')[1]
                for urlpattern in urlpatterns:

                    if str("/".join(str(urlpattern.pattern).split("/", 2)[:1])) == str("/".join(str(url).split("/", 2)[:1])):
                            last_url_name = urlpattern.name

                url = {
                    'last': request.META.get('HTTP_REFERER'),
                    'last_url_name': Permission.objects.get(codename=last_url_name).name,
                    # 'current': request.get_full_path(),
                    # 'current_name': Permission.objects.get(codename=current_url_name).name,
                }
                urls.append(url)

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


def NewspaperService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                filter['isDeleted'] = False
                return Newspaper.objects.filter(**filter)
            else:
                return Newspaper.objects.filter(filter, isDeleted=False)
        else:
            return Newspaper.objects.filter(isDeleted=False)
    except ExtraTime.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()


def NewspaperGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return Newspaper.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def YekaApplicationFileNameGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return YekaApplicationFileName.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def YekaApplicationFileNameService(request, filter):
    try:
        if filter:
            filter['isDeleted'] = False
            return YekaApplicationFileName.objects.filter(**filter)
        else:
            return YekaApplicationFileName.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()
        pass


def YekaApplicationGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return CompetitionApplication.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def YekaApplicationService(request, filter):
    try:
        if filter:
            filter['isDeleted'] = False
            return CompetitionApplication.objects.filter(**filter)
        else:
            return CompetitionApplication.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()
        pass


def YekaBusinessService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                filter['isDeleted'] = False
                return YekaBusiness.objects.filter(**filter)
            else:
                return YekaBusiness.objects.filter(filter, isDeleted=False)
        else:
            return City.objects.filter(isDeleted=False)
    except City.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()


def YekaApplicationFileGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return YekaApplicationFile.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def YekaApplicationFileService(request, filter):
    try:
        if filter:
            filter['isDeleted'] = False
            return YekaApplicationFile.objects.filter(**filter)
        else:
            return YekaApplicationFile.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()
        pass


# yarisma

def CompetitionGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return Competition.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def CompetitionService(request, filter):
    try:
        if filter:
            filter['isDeleted'] = False
            return Competition.objects.filter(**filter)
        else:
            return Competition.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()
        pass


def CompetitionCompanyGetService(request, filter):
    try:
        with transaction.atomic():
            if filter:
                filter['isDeleted'] = False
                return CompetitionCompany.objects.get(**filter)
            else:
                return None
    except Exception as e:
        traceback.print_exc()
        pass


def CompetitionCompanyService(request, filter):
    try:
        if filter:
            filter['isDeleted'] = False
            return CompetitionCompany.objects.filter(**filter)
        else:
            return CompetitionCompany.objects.filter(isDeleted=False)
    except Exception as e:
        traceback.print_exc()
        pass


def FactoryFileNameService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                filter['isDeleted'] = False
                return FactoryFileName.objects.filter(**filter)
            else:
                return FactoryFileName.objects.filter(filter, isDeleted=False)
        else:
            return FactoryFileName.objects.filter(isDeleted=False)
    except FactoryFileName.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()


def FactoryFileNameGetService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                filter['isDeleted'] = False
                return FactoryFileName.objects.get(**filter)
            else:
                return FactoryFileName.objects.get(filter, isDeleted=False)
        else:
            return FactoryFileName.objects.get(isDeleted=False)
    except FactoryFileName.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()


def FactoryGetService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                filter['isDeleted'] = False
                return Factory.objects.get(**filter)
            else:
                return Factory.objects.get(filter, isDeleted=False)
        else:
            return Factory.objects.get(isDeleted=False)
    except Factory.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()


def FactoryService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                filter['isDeleted'] = False
                return Factory.objects.filter(**filter)
            else:
                return Factory.objects.filter(filter, isDeleted=False)
        else:
            return Factory.objects.filter(isDeleted=False)
    except Factory.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()


def FactoryFileService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                filter['isDeleted'] = False
                return FactoryFile.objects.filter(**filter)
            else:
                return FactoryFile.objects.filter(filter, isDeleted=False)
        else:
            return FactoryFile.objects.filter(isDeleted=False)
    except FactoryFile.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()


def FactoryFileGetService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                filter['isDeleted'] = False
                return FactoryFile.objects.get(**filter)
            else:
                return FactoryFile.objects.get(filter, isDeleted=False)
        else:
            return FactoryFile.objects.get(isDeleted=False)
    except FactoryFile.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()


def AssociateFileNameService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                filter['isDeleted'] = False
                return AssociateDegreeFileName.objects.filter(**filter)
            else:
                return AssociateDegreeFileName.objects.filter(filter, isDeleted=False)
        else:
            return AssociateDegreeFileName.objects.filter(isDeleted=False)
    except AssociateDegreeFileName.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()


def AssociateFileNameGetService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                filter['isDeleted'] = False
                return AssociateDegreeFileName.objects.get(**filter)
            else:
                return AssociateDegreeFileName.objects.get(filter, isDeleted=False)
        else:
            return AssociateDegreeFileName.objects.get(isDeleted=False)
    except AssociateDegreeFileName.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()


def AssociateFileService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                filter['isDeleted'] = False
                return AssociateDegreeFile.objects.filter(**filter)
            else:
                return AssociateDegreeFile.objects.filter(filter, isDeleted=False)
        else:
            return AssociateDegreeFile.objects.filter(isDeleted=False)
    except AssociateDegreeFile.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()


def AssociateFileGetService(request, filter):
    try:
        if filter:
            if type(filter) != type(Q()):
                filter['isDeleted'] = False
                return AssociateDegreeFile.objects.get(**filter)
            else:
                return AssociateDegreeFile.objects.get(filter, isDeleted=False)
        else:
            return AssociateDegreeFile.objects.get(isDeleted=False)
    except AssociateDegreeFile.DoesNotExist:
        return None
    except Exception as e:
        traceback.print_exc()


def validate_file_extension(value):  # Aday YEKA eklerken sadece kml ve kmz dosyalarını kayıt etmek
    import os
    from django.core.exceptions import ValidationError
    file_size = 0
    if Settings.objects.filter(key='file_size'):
        file_size = Settings.objects.get(key='file_size').value
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.kml', '.kmz']
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            'Sadece .kml ve .kmz uzantılı dosya yükleyebilirsiniz.')
    if value.size > float(file_size) * 1024 * 1024:
        raise ValidationError(
            'Maksimum yüklenmesi gereken dosya boyutu: ' + file_size + ' MB')
def validate_file_size(value):  # dosya boyutu kontrolü
    from django.core.exceptions import ValidationError
    file_size = 0
    if Settings.objects.filter(key='file_size'):
        file_size = Settings.objects.get(key='file_size').value
    if value.size > float(file_size) * 1024 * 1024:
        raise ValidationError('Dosya Boyutu Büyük.(Maksimum yüklenmesi gereken dosya boyutu: ' + file_size + ' MB')

from rest_framework.views import APIView
from rest_framework.response import Response

from sbs.models import Permission
from sbs.models.ekabis.Logs import Logs
from sbs.models.tvfbf.LogAPIObject import LogAPIObject
from sbs.serializers.LogSerializers import LogResponseSerializer
from sbs.serializers.PermissionSerializers import PermissionResponseSerializer
from sbs.services.services import LogsService


class GetLog(APIView):

    def post(self, request, format=None):

        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        count = LogsService(request, None).count()

        all_objects = Logs.objects.filter(isDeleted=False).filter(
            user__first_name__icontains=request.data['search[value]']).filter(
            user__last_name__icontains=request.data['search[value]']).order_by('-id')[
                      int(start):end]

        filteredTotal = Logs.objects.filter(isDeleted=False).filter(
            user__first_name__icontains=request.data['search[value]']).filter(
            user__last_name__icontains=request.data['search[value]']).count()



        serializer_context = {
            'request': request,

        }



class GetPermission(APIView):

    def post(self, request, format=None):

        draw = request.data['draw']
        start = request.data['start']
        length = request.data['length']
        end = int(start) + int(length)

        count = Permission.objects.filter(isDeleted=False).count()

        all_objects = Permission.objects.filter(isDeleted=False).filter(
            name__icontains=request.data['search[value]']).order_by('-creationDate')[
                      int(start):end]

        filteredTotal = Permission.objects.filter(isDeleted=False).filter(
            name__icontains=request.data['search[value]']).count()

        logApiObject = LogAPIObject()
        logApiObject.data = all_objects
        logApiObject.draw = int(request.POST['draw'])
        logApiObject.recordsTotal = int(count)
        logApiObject.recordsFiltered = int(filteredTotal)

        serializer_context = {
            'request': request,
        }
        serializer = PermissionResponseSerializer(logApiObject, context=serializer_context)
        return Response(serializer.data)




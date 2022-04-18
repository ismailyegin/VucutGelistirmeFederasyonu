from rest_framework.views import APIView
from rest_framework.response import Response

from sbs.models.ekabis import Logs
from sbs.serializers.LogSerializers import LogResponseSerializer
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





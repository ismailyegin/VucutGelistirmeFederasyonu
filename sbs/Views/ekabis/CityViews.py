from django.http import JsonResponse
from rest_framework.decorators import api_view


# Fetch county by city id
from sbs.models.ekabis.District import District
from sbs.models.ekabis.Neighborhood import Neighborhood
from sbs.serializers.DistrictSerializer import DistrictSerializer
from sbs.serializers.NeighborhoodSerializer import NeighborhoodSerializer


@api_view(http_method_names=['POST'])
def get_districts(request):
    if request.POST:
        try:

            il_id = request.POST.get('il_id')
            districts = District.objects.filter(city_id=il_id)

            data = DistrictSerializer(districts, many=True)

            responseData = dict()
            responseData['ilceler'] = data.data

            neighborhoods = Neighborhood.objects.filter(district=districts[0].id)

            data_neighborhood = NeighborhoodSerializer(neighborhoods, many=True)

            responseData['neighborhoods'] = data_neighborhood.data

            return JsonResponse(responseData, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})


# Fetch neighborhood by county id
@api_view(http_method_names=['POST'])
def get_neighborhood(request):
    if request.POST:
        try:

            ilce_id = request.POST.get('ilce_id')


            responseData = dict()
            responseData['neighborhoods'] = data.data

            return JsonResponse(responseData, safe=True)

        except Exception as e:

            return JsonResponse({'status': 'Fail', 'msg': e})



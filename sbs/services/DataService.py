import traceback

import pandas
from django.shortcuts import redirect
from sbs.models.ekabis.City import City


def add_city():
    try:

        df = pandas.read_csv('city.csv')
        for value in df.values:

            city_name = value[0].split(';')[1].split('"')[1]
            plateNo = value[0].split(';')[0]
            if not City.objects.filter(name=city_name):
                city = City(name=city_name, plateNo=plateNo)
                city.save()
        print('İller eklendi')
        return redirect('ekabis:initial_data_success_page')

    except Exception as e:
        traceback.print_exc()
        return redirect('ekabis:initial_data_error_page')












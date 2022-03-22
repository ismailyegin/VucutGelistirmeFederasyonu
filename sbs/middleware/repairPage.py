from django.shortcuts import redirect

from sbs.models.ekabis.Settings import Settings



class OnarimSayfasiMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response=None
        if Settings.objects.filter(key='maintenance'):
            if Settings.objects.get(key='maintenance').value == 'True':
                if not '/maintenance-page/' in request.path:
                    return redirect('ekabis:view_repair_page')

        response = self.get_response(request)
        return response




from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render

from sbs.Forms.havaspor.DocumentNameForm import DocumentNameForm
from sbs.models.tvfbf.DocumentName import DocumentName
from sbs.services import general_methods


@login_required
def return_document(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    document_form = DocumentNameForm()

    if request.method == 'POST':

        document_form = DocumentNameForm(request.POST)

        if document_form.is_valid():

            document = DocumentName(name=document_form.cleaned_data['name'])
            document.save()

            return redirect('sbs:return_document')

        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')
    documents = DocumentName.objects.all()
    return render(request, 'TVGFBF/Document/documents.html',
                  {'document_form': document_form, 'documents': documents})


def document_delete(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    try:
        with transaction.atomic():
            if request.method == 'POST' and request.is_ajax():
                uuid = request.POST['uuid']
                obj = DocumentName.objects.get(uuid=uuid)
                obj.delete()

                return JsonResponse({'status': 'Success', 'messages': 'delete successfully'})
            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
    except DocumentName.DoesNotExist:
        return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})


@login_required
def document_update(request, uuid):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    documentItem = DocumentName.objects.get(uuid=uuid)
    document_form = DocumentNameForm(request.POST or None, instance=documentItem)
    if request.method == 'POST':
        if document_form.is_valid():
            document = document_form.save(request, commit=False)
            document.save()
            messages.success(request, 'Başarıyla Güncellendi')
            return redirect('sbs:return_document')
        else:
            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'TVGFBF/Document/update-document.html',
                  {'document_form': document_form})

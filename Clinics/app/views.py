from datetime import datetime
from django.shortcuts import render
from .models import Clinicus,Methods
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView

main = 'Главная'
contact_title = 'Контакты'
quest_title = 'Психотерапевты'
quest_message ='Выбери своего специалиста из списка :'


    #def index(request):
    #    """Страничка с списком терапевтов"""
    #    assert isinstance(request, HttpRequest)

    #    clinics = Clinicus.objects.all()
    #    return render(
    #        request,
    #        'app/index.html',
    #        {
    #        'title': quest_title,
    #        'message': quest_message,
    #        'db': clinics,
    #    })

def by_doctor(request, doctor_id):
    assert isinstance(request, HttpRequest)
    doctor = Clinicus.objects.get(pk=doctor_id)
    methods = doctor.method.all()
    return render(
    request,
    'app/by_doctor.html',context={'doctor':doctor}
)
class IndexView(ListView):
    model = Clinicus
    template_name = 'app/index.html'
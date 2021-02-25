"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from .models import CLINICUS
from django.http import HttpRequest

def home(request):
    """Главная страница сайта"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Страничка для контактов"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Здесь вы узнаете как с нами связаться!',
            'year':datetime.now().year,
        }
    )

def about(request):
    """О клинике"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Мы клиника с мировым именем!',
            'year':datetime.now().year,
        }
    )
def terapefts(request):
    """Страничка с списком терапевтов"""
    assert isinstance(request, HttpRequest)
    dbs = CLINICUS.objects.order_by('-timeLoad')
    return render(
        request,
        'app/terapefts.html',
        {
            'title':'Психотерапевты',
            'message':'Выбери своего специалиста',
            'year':datetime.now().year,
            'database': dbs
        }
    )
def by_doctor(request, doctor_id):
    assert isinstance(request, HttpRequest)
    doctor = CLINICUS.objects.get(pk=doctor_id)
    return render(
    request,
    'app/by_doctor.html',
    {
        'name':"Специалист {}".format(doctor.name),
        'foto_url':doctor.urlsLrgeFoto,
        'methods':doctor.Methods,
        'timepub':doctor.timeLoad,
        'year': datetime.now().year,
    }
)
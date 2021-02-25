"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from .models import CLINICUS
from django.http import HttpRequest
from django.utils.translation import ugettext_lazy as trnsl

main = trnsl('Главная')
contact_title = trnsl('Контакты')
contact_message = trnsl('Здесь вы узнаете как с нами связаться!')
about_title = trnsl('О нас')
about_message= trnsl('Мы клиника с мировым именем!')
quest_title = trnsl('Психотерапевты')
quest_message = trnsl('Выбери своего специалиста из списка :')
spec = trnsl('{}')
def home(request):
    """Главная страница сайта"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':main,
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
            'title':contact_title,
            'message':contact_message,
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
            'title':about_title,
            'message':about_message,
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
            'title':quest_title,
            'message':quest_message,
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
        'name':spec.format(doctor.name),
        'foto_url':doctor.urlsLrgeFoto,
        'methods':doctor.Methods,
        'timepub':doctor.timeLoad,
        'year': datetime.now().year,
    }
)
"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from .models import Clinicus,Methods
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

def index(request):
    """Страничка с списком терапевтов"""
    assert isinstance(request, HttpRequest)
    clinics = Clinicus.objects.all()
    return render(
        request,
        'index.html',
        {
            'title':quest_title,
            'message':quest_message,
            'year':datetime.now().year,
            'clinics': clinics
        }
    )
def by_doctor(request, doctor_id):
    assert isinstance(request, HttpRequest)
    doctor = Clinicus.objects.get(pk=doctor_id)
    return render(
    request,
    'app/by_doctor.html',
    {
        'name':spec.format(doctor.name),
        'foto_url':doctor.urlsLrgeFoto,
        'timepub':doctor.timeLoad,
        'year': datetime.now().year,
    }
)
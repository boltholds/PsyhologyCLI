"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from .models import CLINICUS
from django.http import HttpRequest

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'My contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'There you look about site',
            'year':datetime.now().year,
        }
    )
def terapefts(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    dbs = CLINICUS.objects.order_by('id')
    return render(
        request,
        'app/terapefts.html',
        {
            'title':'Therapefts',
            'message':'These you get a therapyst',
            'year':datetime.now().year,
            'database': dbs
        }
    )

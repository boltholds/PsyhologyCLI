"""
Definition of urls for Therapysts.
"""

from datetime import datetime
from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import RedirectView
from app import forms, views


urlpatterns = [
    path('app/', views.index),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico', permanent=True)),
    path('app/<int:doctor_id>/',views.by_doctor),
    path('login/',
        LoginView.as_view
        (
            template_name='app/login.html',
            authentication_form=forms.BootstrapAuthenticationForm,
            extra_context=
            {
                'title': 'Log in',
                'year' : datetime.now().year,
            }
        ),
        name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]

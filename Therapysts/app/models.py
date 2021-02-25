"""
Definition of models.
"""

from django.db import models
from django.utils.translation import ugettext_lazy as trnsl

class CLINICUS(models.Model):
    idRecords = models.CharField(max_length=20)
    name = models.CharField(max_length=60)
    Methods = models.TextField(null=False,blank=False)
    urlsLrgeFoto = models.URLField()
    urlsSmlFoto = models.URLField()
    timeLoad = models.DateField(auto_now_add=True,db_index=True)
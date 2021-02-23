"""
Definition of models.
"""

from django.db import models

# Create your models here.
class THERAPEFT(models.Model):
    idRecords = models.CharField(max_length=20,primary_key=True)
    nameTherapeft = models.CharField(max_length=60)
    therapyMethods = models.TextField(null=False,blank=False)
    urlsLrgeFoto = models.URLField()
    urlsSmlFoto = models.URLField()
    timeLoadToDB = models.DateField(auto_now_add=True,db_index=True)
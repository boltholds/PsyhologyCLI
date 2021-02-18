import json
import sys
import airtable
import requests
import datetime

#Base ID - appQnV5O4ndpzTcMs
#Api ID - keyncr4pK9gc6bE1r
#NAme table - Psychotherapists

table = airtable.Airtable('appQnV5O4ndpzTcMs','Psychotherapists','keyncr4pK9gc6bE1r')
for records in table.get_all():
    id = records['id']
    data = records['createdTime']
    name = records['fields']['Имя']
    method = ""
    for methods in records['fields']['Методы']:
        method +=(","+ methods)
    foto = records['fields']['Фотография'][0]['thumbnails']
    print(id,name,str(method),foto['full']['url'],data,sep=' - ')
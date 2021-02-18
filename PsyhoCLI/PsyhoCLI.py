import json
import sys,string
import airtable
import requests
import datetime
import psycopg2

#Base ID - appQnV5O4ndpzTcMs
#Api ID - keyncr4pK9gc6bE1r
#NAme table - Psychotherapists
#def removehttp(text) :
#    try:
#        index = text.index("https://")
#    except ValueError:
#        return text
#    else:
#        index = text.index("https://")
#        return text[index:len(text)]
 

try:
    connecton = psycopg2.connect(
      database="postgres", 
      user="postgres", 
      password="9318093180bh", 
      host="127.0.0.1", 
      port="5432"
    )
    print("База данных успешно открыта!")
    curs = connecton.cursor()

    curs.execute('''CREATE TABLE IF NOT EXISTS THERAPEFTS
                    (ID CHAR(42) PRIMARY KEY,
                    NAME TEXT NOT NULL,
                    THERAPY_TEG TEXT NOT NULL,
                    IMG_FUL VARCHAR(255),
                    IMG_SMAL VARCHAR(255),
                    DATA DATE);''')
    connecton.commit()  
    print("База данных успешно создана!")
    table = airtable.Airtable('appQnV5O4ndpzTcMs','Psychotherapists','keyncr4pK9gc6bE1r')
    #Job Airtablets
    for records in table.get_all():
        id = records['id']
        data = records['createdTime']
        name = records['fields']['Имя']
        method = ""
        for methods in records['fields']['Методы']:
            method +=('#'+methods+' ')
        foto = records['fields']['Фотография'][0]['thumbnails']
        
        curs = connecton.cursor()
        curs.execute(
        '''INSERT INTO THERAPEFTS (ID,NAME,THERAPY_TEG,IMG_FUL,IMG_SMAL,DATA) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}')'''.format(
        id,name,method,foto['full']['url'],foto['small']['url'],data))
        #print(id,name,str(method),foto['full']['url'],data,sep=' - ')
        connecton.commit()  
except (Exception, psycopg2.Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connecton:
        curs.close()
        connecton.close()
        print("Соединение с PostgreSQL закрыто")



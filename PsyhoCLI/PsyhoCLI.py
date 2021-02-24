import json
import sys,string
import airtable
import requests
import datetime
import psycopg2


try:
    #Пытаемся установить соединение с БД
    connecton = psycopg2.connect(
        database="test1", 
        user="postgres", 
        password="9318093180bh", 
        host="127.0.0.1", 
        port="5432"
    )
    #Значения для авторизации в Airtable
    baseID = 'appQnV5O4ndpzTcMs'
    apiID = 'keyncr4pK9gc6bE1r'
    airtablename = 'Psychotherapists'
    nametable = "therapyst"

    print("Соединение с PostgreSQL успешно установлено!")
    curs = connecton.cursor()
    #Если такой БД нет создаём её по шаблону
    curs.execute("SELECT to_regclass('{}')".format(nametable))
    if not curs.fetchone()[0]:
        curs.execute('''CREATE TABLE IF NOT EXISTS {} (
                        ID INT PRIMARY KEY,
                        IDRECORD VARCHAR(17) NOT NULL,
                        NAME TEXT NOT NULL,
                        THERAPY_TEG TEXT NOT NULL,
                        IMG_FUL VARCHAR(255),
                        IMG_SMAL VARCHAR(255),
                        DATA DATE);'''.format(nametable))
        connecton.commit()  
        print("База данных успешно создана!")
    else:
        print("Обновление таблицы")
    #Подключаем Airtablet
    table = airtable.Airtable(baseID,airtablename,apiID)
    #Анализируем полученный из таблицы сложный словарь
    ids = set()#Множество куда сохраняем скаченные ключи
    i = 1
    for records in table.get_all():
        idrecord = records['id']
        ids.add(idrecord)
        data = records['createdTime']
        name = records['fields']['Имя']
        #Превращаем перечисленные методы в теги для удобного разедения
        method = ""
        for methods in records['fields']['Методы']:
            method +=('#'+methods+' ')
        foto = records['fields']['Фотография'][0]['thumbnails']
       
        #Вставляем в БД новые значения и фиксируем изменения
        curs = connecton.cursor()
        curs.execute(
        "INSERT INTO {} (ID,IDRECORD,NAME,THERAPY_TEG,IMG_FUL,IMG_SMAL,DATA) VALUES({},'{}' ,'{}','{}' ,'{}' ,'{}' ,'{}') ON CONFLICT(ID) DO NOTHING".format
        (nametable,i,idrecord,name,method,foto['full']['url'],foto['small']['url'],data,))
        connecton.commit() 
        i+=1
    #Поиск значений ключей которые есть в БД ,но нет в Airtable и удаление записей с такими ключами из БД
    curs = connecton.cursor()
    curs.execute('''SELECT ID FROM s%''',(nametable,))
    rows = curs.fetchall()
    comp =set()
    for row in rows:
        comp.add(row[0])
    result = list(comp-ids)#Разность множеств содержащая удалённые из Airtable записи
    if len(result) !=0 :
        #Если список с ключами не пустой, значит есть что удалить!
        for poit in result:
            curs.execute("DELETE FROM %s WHERE ID=%s;",(nametable,poit,))
            print("Удалена запись с ID: ", str(poit))
    else:
        print("Обновление таблицы не требуется!")
    connecton.commit()  

except (Exception, psycopg2.Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connecton:
        curs.close()
        connecton.close()
        print("Соединение с PostgreSQL закрыто")



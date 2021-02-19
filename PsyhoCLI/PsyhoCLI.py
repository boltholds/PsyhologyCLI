import json
import sys,string
import airtable
import requests
import datetime
import psycopg2


try:
    #Пытаемся установить соединение с БД
    connecton = psycopg2.connect(
      database="postgres", 
      user="postgres", 
      password="9318093180bh", 
      host="127.0.0.1", 
      port="5432"
    )
    print("Соединение с PostgreSQL успешно установлено!")
    nametable = 'THERAPEFTS'
    curs = connecton.cursor()
    #Если такой БД нет создаём её по шаблону
    curs.execute("SELECT to_regclass(%s)", (nametable,))
    if not curs.fetchone()[0]:
        curs.execute('''CREATE TABLE IF NOT EXISTS THERAPEFTS
                        (ID VARCHAR(17) PRIMARY KEY,
                        NAME TEXT NOT NULL,
                        THERAPY_TEG TEXT NOT NULL,
                        IMG_FUL VARCHAR(255),
                        IMG_SMAL VARCHAR(255),
                        DATA DATE);''')
        connecton.commit()  
        print("База данных успешно создана!")
    else:
        print("Обновление таблицы...")

    #Значения для авторизации в Airtable
    baseID = 'appQnV5O4ndpzTcMs'
    apiID = 'keyncr4pK9gc6bE1r'
    airtablename = 'Psychotherapists'
 
    #Подключаем Airtablet
    table = airtable.Airtable(baseID,airtablename,apiID)
    #Анализируем полученный из таблицы сложный словарь
    ids = set()#Множество куда сохраняем скаченные ключи
    for records in table.get_all():
        id = records['id']
        ids.add(id)
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
        "INSERT INTO THERAPEFTS (ID,NAME,THERAPY_TEG,IMG_FUL,IMG_SMAL,DATA) VALUES(%s ,%s ,%s ,%s ,%s ,%s) ON CONFLICT(ID) DO NOTHING",
        (id,name,method,foto['full']['url'],foto['small']['url'],data,))
        connecton.commit() 
    #Поиск значений ключей которые есть в БД ,но нет в Airtable и удаление записей с такими ключами из БД
    curs = connecton.cursor()
    curs.execute('''SELECT ID FROM THERAPEFTS''')
    rows = curs.fetchall()
    comp =set()
    for row in rows:
        comp.add(row[0])
    result = list(comp-ids)#Разность множеств содержащая удалённые из Airtable записи
    if len(result) !=0 :
        #Если список с ключами не пустой, значит есть что удалить!
        for poit in result:
            curs.execute("DELETE from THERAPEFTS where ID=%s;",(poit,))
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



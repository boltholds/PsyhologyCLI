import json
import sys,string
import airtable
import requests
import datetime
import psycopg2
import traceback  


#Значения для авторизации в Airtable
baseID = 'appQnV5O4ndpzTcMs'
apiID = 'keyncr4pK9gc6bE1r'
airtablename = 'Psychotherapists'
#Имена таблиц в базе данных
table_therapyst = 'app_clinicus'
table_Method_trapyst = 'app_clinicus_method'
table_method = 'app_methods'

def create_or_update_profi(table_therapyst,idrecord,name,foto,data,methody):
    '''Эта функция создаёт\обновляет запись анкеты психолога в таблице и синхронизирует
    с таблицей методов'''
    curs = connecton.cursor()
    curs.execute(
    '''INSERT INTO {} (idrecord,name,urlslrgefoto,urlssmlfoto,timeload) 
    VALUES('{}' ,'{}' ,'{}' ,'{}' ,'{}') ON CONFLICT(idrecord) 
    DO UPDATE SET (name,urlslrgefoto,urlssmlfoto,timeload) = 
    (EXCLUDED.name,EXCLUDED.urlslrgefoto,EXCLUDED.urlssmlfoto,EXCLUDED.timeload)'''.format
    (table_therapyst,idrecord,name,foto['large']['url'],foto['small']['url'],data))
    connecton.commit() 
    curs = connecton.cursor()
    curs.execute("SELECT id FROM {} WHERE idrecord='{}' ORDER BY id".format(table_therapyst,idrecord))
    idPkTAbleTherapeft = curs.fetchone()[0]
    connecton.commit() 
    #print('методы вставляем в БД')
    curs = connecton.cursor()
    for method in methody:
        #Извлекаем из таблицы значения ID по имени метода
        curs.execute("SELECT id FROM {} WHERE therapy='{}' ORDER BY id".format(table_method,method))
        id_method = curs.fetchone()[0]
        #И записываем ID всех методов этого терапевта
        curs.execute(
        "INSERT INTO {} (clinicus_id,methods_id) VALUES({},{}) ON CONFLICT(clinicus_id,methods_id) DO NOTHING".format
        (table_Method_trapyst,idPkTAbleTherapeft,id_method))
    connecton.commit() 

def delete_terapyst(ids):
    '''Эта функция получает множество ключей анкет психологов которые нужно удалить из таблицы БД, 
    также удаляет свзи в таблице методов'''
    #print('Поиск значений ключей которые есть в БД ,но нет в Airtable и удаление записей с такими ключами из БД')
    curs = connecton.cursor()
    curs.execute('SELECT idrecord FROM {}'.format(table_therapyst))
    rows = curs.fetchall()
    comp =set()
    for row in rows:
        comp.add(row[0])
    result = list(comp-ids)#Разность множеств содержащая удалённые из Airtable записи
    #print(result)
    if len(result) !=0 :
        #Если список с ключами не пустой, значит есть что удалить!
        for poit in result:
            curs.execute("DELETE FROM {} WHERE idrecord='{}' RETURNING id;".format(table_therapyst,poit,))
            id_delete_terapeft = curs.fetchone()[0]
            print("Удалена учётная запись с ID: ", str(poit))
            #А теперь удалим все остальные записи этого терапевта из  таблиц методов
            curs.execute("DELETE FROM {} WHERE clinicus_id='{}';".format(table_Method_trapyst,id_delete_terapeft,))
    else:
        print("Нет полей для удаления: Конец сеанса!")
    connecton.commit()

def search(table,what_search):
    curs = connecton.cursor()
    curs.execute("SELECT id FROM {} WHERE idrecord='{}' ORDER BY id".format(table,row,what_search))
    return curs.fetchone() is None
try:
    #Пытаемся установить соединение с БД
    connecton = psycopg2.connect(
        database="clinics", 
        user="postgres", 
        password="9318093180bh", 
        host="127.0.0.1", 
        port="5432"
    )
    print("Соединение с PostgreSQL успешно установлено!")
    curs = connecton.cursor()
    #Подключаем Airtablet
    table = airtable.Airtable(baseID,airtablename,apiID)
    #print('Заполняем таблицу методов извлекая их из всех записей')
    curs = connecton.cursor()
    for records in table.get_all():
        for terapy in records['fields']['Методы']:
            curs.execute(
            "INSERT INTO {} (therapy) VALUES ('{}') ON CONFLICT (therapy) DO NOTHING".format
            (table_method,terapy))
    connecton.commit() 
    #Анализируем полученный из таблицы сложный словарь
    ids = set()#Множество куда сохраняем скаченные ключи
    for records in table.get_all():
        idrecord = records['id']
        ids.add(idrecord)
        data = records['createdTime']
        name = records['fields']['Имя']
        foto = records['fields']['Фотография'][0]['thumbnails']
        methody = records['fields']['Методы']
        #print('Вводим в таблицу новые значения и фиксируем изменения')
        #Проверяем есть ли такие записи в таблице
        curs = connecton.cursor()
        curs.execute("SELECT id FROM {} WHERE idrecord='{}' ORDER BY id".format(table_therapyst,idrecord))
        create_or_update_profi(table_therapyst,idrecord,name,foto,data,methody)
    delete_terapyst(ids)
  

except (Exception, psycopg2.Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
    print(traceback.format_exc())
finally:
    if connecton:
        curs.close()
        connecton.close()
        print("Соединение с PostgreSQL закрыто")
        

#!utf-8
import json
import sys
import string
from airtable import Airtable
import requests
import datetime
import psycopg2
import traceback
import logging
from dotenv import dotenv_values
import gettext
from locale import getlocale


#Логирование в консоль по умолчанию только для INFO
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(console)

# Значения для авторизации в Airtable
config = dotenv_values(f"air.env")
baseID = config.get("BASE")
apiID = config.get("API_ID")
airtable_name = config.get("AIRTABLE_NAME")
# Имена таблиц в базе данных
table_therapyst = config.get("TABLE_NAME")
table_method_therapyst = config.get("TABLE_METHODS")
table_method = config.get("TABLE_METHODS_NAME")




oslang, enc = getlocale()
oslang = oslang.split("_")[0]


def loc(s):
    return str(s)


if oslang in ["es", "en", "Es", "EN", "En"]:
    gettext.bindtextdomain("en", "/locale")
    gettext.textdomain("en")
    tr = gettext.translation("en", localedir="locale", languages=['en_US'])
    tr.install()
    loc = tr.gettext




def create_or_update_profi(table_name, idrecord, name_doc, foto_profile, data_create, methods_of_therapy):
    """Эта функция создаёт или обновляет запись анкеты психолога в таблице и синхронизирует
    с таблицей методов"""
    con_cursor = connection.cursor()
    command = f'''INSERT INTO {table_name} 
        (
        idrecord,
        name,
        urlslrgefoto,
        urlssmlfoto,
        wightlrgfoto,
        lenghtlrgfoto,
        timeload
        ) 
    VALUES
    (
    '{idrecord}' ,
    '{name_doc}',
    '{foto_profile['large']['url']}',
    '{foto_profile['small']['url']}', 
    '{foto_profile['large']['width']}',
    '{foto_profile['large']['height']}',
    '{data_create}'
    ) 
    ON CONFLICT(idrecord) 
    DO UPDATE SET (name,urlslrgefoto,urlssmlfoto,wightlrgfoto,lenghtlrgfoto,timeload) = 
    (
    EXCLUDED.name,
    EXCLUDED.urlslrgefoto,
    EXCLUDED.urlssmlfoto,
    EXCLUDED.wightlrgfoto,
    EXCLUDED.lenghtlrgfoto,
    EXCLUDED.timeload)'''
    con_cursor.execute(command)
    connection.commit()
    con_cursor = connection.cursor()
    con_cursor.execute(f"SELECT id FROM {table_name} WHERE idrecord='{idrecord}' ORDER BY id")
    id_pk_table_of_therapyst = con_cursor.fetchone()[0]
    connection.commit()
    # Вставляем методы в БД
    con_cursor = connection.cursor()
    for method in methods_of_therapy:
        # Извлекаем из таблицы значения ID по имени метода
        con_cursor.execute(f"SELECT id FROM {table_method} WHERE therapy='{method}' ORDER BY id")
        id_method = con_cursor.fetchone()[0]
        # И записываем ID всех методов этого терапевта
        con_cursor.execute(
            f"INSERT INTO {table_method_therapyst} "
            f"(clinicus_id,methods_id) VALUES({id_pk_table_of_therapyst},{id_method}) "
            f"ON CONFLICT(clinicus_id,methods_id) DO NOTHING"
        )

    logger.info(loc("Запись успешно создана или объявлена!"))
    connection.commit()


def delete_terapyst(index):
    """Эта функция получает множество ключей анкет психологов которые нужно удалить из таблицы БД,
    # также удаляет связи в таблице методов"""
    logger.debug(loc('Поиск значений ключей которые есть в БД,'
                     'но нет в Airtable и удаление записей с такими ключами из БД'))

    cursor = connection.cursor()
    cursor.execute(f'SELECT idrecord FROM {table_therapyst}')
    rows = cursor.fetchall()
    comp = set()
    for row in rows:
        comp.add(row[0])
    result = list(comp - index)  # Разность множеств содержащая удалённые из Airtable записи
    if len(result) != 0:
        # Если список с ключами не пустой, значит есть что удалить!
        for poit in result:
            cursor.execute(f"DELETE FROM {table_therapyst} WHERE idrecord='{poit}' RETURNING id;")
            id_delete_terapeft = cursor.fetchone()[0]
            logger.info(loc(f"Удалена учётная запись с ID:{str(poit)}"))
            # А теперь удалим все остальные записи этого терапевта из таблиц методов
            cursor.execute(f"DELETE FROM {table_method_therapyst} WHERE clinicus_id='{id_delete_terapeft}';")
    else:
        logger.info(loc("Нет полей для удаления: Конец сеанса!"))
    connection.commit()


def search(inner_table, id_what_search):
    cursor = connection.cursor()
    cursor.execute(f"SELECT id FROM {inner_table} WHERE idrecord='{id_what_search}' ORDER BY id;")
    return cursor.fetchone() is None


if __name__ == "__main__":
    try:
        # PostgreSQL
        db = config.get("DB_TABLE_NAME")
        user = config.get("USER_NAME")
        password = config.get("PASSWORD")
        host = config.get("HOST")
        port = config.get("PORT")
        logger.info(f"{db} for {user} on {host}:{port}")
        # Пытаемся установить соединение с БД
        connection = None
        connection = psycopg2.connect(
            database=db,
            user=user,
            password=password,
            host=host,
            port=port
        )
        logger.info(loc("Соединение с PostgreSQL успешно установлено!"))

        cursor = connection.cursor()
        # Подключаем Airtablet
        table = Airtable(baseID, apiID)
        logger.debug(loc('Заполняем таблицу методов извлекая их из всех записей'))
        cursor = connection.cursor()
        for records in table.get(airtable_name)['records']:
            for terapy in records['fields']['Методы']:
                cursor.execute(
                    f"INSERT INTO {table_method} (therapy) VALUES ('{terapy}') ON CONFLICT (therapy) DO NOTHING")
        connection.commit()
        # Анализируем полученный из таблицы сложный словарь
        ids = set()  # Множество куда сохраняем полученные ключи
        for records in table.get(airtable_name)['records']:
            idrecord = records['id']
            ids.add(idrecord)
            data = records['createdTime']
            name = records['fields']['Имя']
            foto = records['fields']['Фотография'][0]['thumbnails']
            psy_methods = records['fields']['Методы']
            logger.debug(loc('Вводим в таблицу новые значения и фиксируем изменения'))
            # Проверяем есть ли такие записи в таблице
            cursor = connection.cursor()
            logger.debug(f"SELECT id FROM {table_therapyst} WHERE idrecord='{idrecord}' ORDER BY id")
            cursor.execute(f"SELECT id FROM {table_therapyst} WHERE idrecord='{idrecord}' ORDER BY id")
            create_or_update_profi(table_therapyst, idrecord, name, foto, data, psy_methods)
        delete_terapyst(ids)

    except (Exception, psycopg2.Error) as error:
        logger.error(loc(error))
        logger.error(traceback.format_exc())
    finally:
        if connection:
            cursor.close()
            connection.close()
            logger.info(loc("Соединение с PostgreSQL закрыто"))

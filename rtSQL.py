#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import MySQLdb, sys

"""
Функция создает подключение к БД и возвращает его в качестве объекта 
вместе с курсором
"""
def Open_DB(DB, Host, Port, User, Passwd):
    if Port == '':
        Port = 3306
    else:
        Port = int(Port)
    try:
        Conection = MySQLdb.connect(host=Host, port=Port, user=User, passwd=Passwd, db=DB, use_unicode=True, charset='utf8')
        Cursor = Conection.cursor()
        
    except MySQLdb.Error:
        print(db.error())
    
    return Conection, Cursor
#=======================================================================
"""
Функция возвращает ID последнего вставленного объекта
"""
def last_insert_ID(Cursor):
    Cursor.execute('SELECT last_insert_id();')            
    ID = Cursor.fetchall()[0][0]
    return ID
#=======================================================================
"""
Функция добавляет новый атрибут в RAckTAbles и возвращает его ID
Если атрибут уже существует, просто возвращается его ID
"""
def rt_new_Attr(ConCur_list, Attr_name, Attr_type):
    Connection, Cursor = ConCur_list
    
    Q = ("SELECT id FROM Attribute WHERE name='%s';")%Attr_name
    Cursor.execute(Q)
    X = Cursor.fetchall()
    if X == ():    
        Query = ("INSERT INTO Attribute (name, type) VALUES ('%s', '%s');")%(Attr_name, Attr_type)
        Cursor.execute(Query)
        Connection.commit()
        ID = last_insert_ID(Cursor)
    else:
        ID = X[0][0]
    
    return ID
#=======================================================================
"""
Функция возвращает ID атрибута по его имени
"""
def rt_Attr_ID_Type(Cursor, Attr_name):
    Query = "SELECT id, type FROM Attribute WHERE name='%s';"%Attr_name
    Cursor.execute(Query)
    X = Cursor.fetchall()[0]
    ID, Type = X
    return ID, Type
#=======================================================================
"""
Функция добавляет новый словарь и возвращает его ID
Если словарь уже существует, просто возвращается его ID
"""
def rt_new_Chapter(ConCur_list, Chapter_name):
    Connection, Cursor = ConCur_list
    Q = ("SELECT id FROM Chapter WHERE name='%s';")%Chapter_name
    Cursor.execute(Q)
    X = Cursor.fetchall()
    if X == (): 
        Query = ("INSERT INTO Chapter (name) VALUES ('%s');")%Chapter_name
        Cursor.execute(Query)
        Connection.commit()
        ID = last_insert_ID(Cursor)
    else:
        ID = X[0][0]
    return ID
#=======================================================================
"""
Функция возвращает ID словаря по его имени
"""
def rt_Chapter_ID(Cursor, Chapter_name):
    Query = "SELECT id FROM Chapter WHERE name='%s';"%Chapter_name
    Cursor.execute(Query)
    ID = Cursor.fetchall()[0][0]
    return ID
#=======================================================================
"""
Функция добавляет новый объект в словарь и возвращает его ID
Если объект уже существует, просто возвращается его ID
"""
def rt_new_Dict_item(ConCur_list, Dict_item_name, Chapter_ID):
    Connection, Cursor = ConCur_list
    Q = ("SELECT dict_key FROM Dictionary WHERE dict_value='%s' AND chapter_id='%s';")%(Dict_item_name, Chapter_ID)
    Cursor.execute(Q)
    X = Cursor.fetchall()
    if X == (): 
        Query = ("INSERT INTO Dictionary (dict_value, chapter_id) VALUES ('%s', '%s');")%(Dict_item_name, Chapter_ID)
        Cursor.execute(Query)
        Connection.commit()
        ID = last_insert_ID(Cursor)
    else:
        ID = X[0][0]
    return ID
#=======================================================================
"""
Функция возвращает ID объекта словаря по его имени
"""
def rt_Dict_item_ID(Cursor, Dict_item_name):
    Query = "SELECT dict_key FROM Dictionary WHERE dict_value='%s';"%Dict_item_name
    Cursor.execute(Query)
    ID = Cursor.fetchall()[0][0]
    return ID
#=======================================================================
"""
Функция добавляет соответствие между типом объекта и его атрибутом
"""
def rt_new_AttrMap(ConCur_list, Objtype_ID, Attr_ID, Chapter_ID):
    Connection, Cursor = ConCur_list
    if Chapter_ID == '':
        Chapter_ID = 'NULL'
    
    Q = (("SELECT objtype_id, attr_id FROM AttributeMap WHERE objtype_id='%s' AND attr_id='%s' AND chapter_id='%s';")%
    (Objtype_ID, Attr_ID, Chapter_ID))
    Cursor.execute(Q)
    X = Cursor.fetchall()
    if X == '()': 
        Query = (("INSERT INTO AttributeMap (objtype_id, attr_id, chapter_id) VALUES ('%s', '%s', '%s');")%
        (Objtype_ID, Attr_ID, Chapter_ID))
        Cursor.execute(Query)
        Connection.commit()
    else:
        pass
#=======================================================================
"""
Фунция добавляет новый объект и возвращает его ID
"""
def rt_addObject(ConCur_list, Name, Obj_type_ID, Comment):
    Connection, Cursor = ConCur_list
    Q = ("SELECT id FROM Object WHERE name='%s' AND objtype_id='%s';")%(Name, Obj_type_ID)
    Cursor.execute(Q)
    X = Cursor.fetchall()
    if X == (): 
        Query = ("INSERT INTO Object (name, objtype_id, comment) VALUES ('%s', '%s', '%s');")%(Name, Obj_type_ID, Comment)
        Cursor.execute(Query)
        Connection.commit()
        ID = last_insert_ID(Cursor)
    else:
        ID = X[0][0]
    return ID
#=======================================================================
"""
Функция соотносит объект с его атрибутами
"""
def rt_addAttr_value(ConCur_list, Obj_ID, Obj_type_ID, Attr_ID, Attr_type, Attr_value):
    Connection, Cursor = ConCur_list
    Q = (("SELECT * FROM AttributeValue WHERE object_id='%s' AND object_tid='%s' AND attr_id='%s' ;")%
    (Obj_ID, Obj_type_ID, Attr_ID))
    Cursor.execute(Q)
    X = Cursor.fetchall()
    if X == ():
        #===============================================================
        if Attr_type == 'string':
            Value_type = 'string_value'
        elif Attr_type in ('uint', 'dict', 'date'):
            Value_type = 'uint_value'
        elif Attr_type == 'float':
            Value_type = 'float_value'
        else:
            print('Что за? 0_o')
        #===============================================================
        Query = (("INSERT INTO AttributeValue (object_id, object_tid, attr_id, %s) VALUES ('%s', '%s', '%s', '%s');")%
        (Value_type, Obj_ID, Obj_type_ID, Attr_ID, Attr_value))
        print(Query)
        Cursor.execute(Query)
        Connection.commit()
        ID = last_insert_ID(Cursor)
    else:
        ID = X[0][0]
    return ID
#=======================================================================

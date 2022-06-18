import pyodbc
from typing import Set
from shared_code.utils import load_yaml
from shared_code.commonClasses import *

try:
    cfg = load_yaml("./creativesFromUrl/config.yaml")
except:
    cfg = load_yaml("../creativesFromUrl/config.yaml")

config = Configuration(cfg)

def open_connection():
    return pyodbc.connect(config.sql["connection_string"])
    
def close_connection(conn):
    conn.close()

def get_resource_by_id(conn, table_name, id):
    cursor = conn.cursor()
    sqlite_select_query = f"""SELECT * FROM {table_name} Where id = '{id}'"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()

    return records

def get_image_by_url(conn, url):
    cursor = conn.cursor()
    sqlite_select_query = f"""SELECT * FROM [dbo].{config.sql["images_table_name"]} Where URL = '{url}'"""
    cursor.execute(sqlite_select_query)
    record = cursor.fetchone()

    return record

def get_image_by_stockId(conn, stockId):
    cursor = conn.cursor()
    sqlite_select_query = f"""SELECT * FROM [dbo].{config.sql["images_table_name"]} Where StockId = '{stockId}'"""
    cursor.execute(sqlite_select_query)
    record = cursor.fetchone()

    return record

def get_image_lisence_by_stockId(stockId):
    conn = open_connection()
    record = get_image_by_stockId(conn, stockId)
    if record == None:
        return None
    close_connection(conn)
    return record[3]

def get_title_by_description(conn, description):
    cursor = conn.cursor()
    nDescription = description.replace("'","''")
    sqlite_select_query = f"""SELECT * FROM [dbo].{config.sql["titles_table_name"]} Where Description = '{nDescription}'"""
    cursor.execute(sqlite_select_query)
    record = cursor.fetchone()

    return record

def get_statistics_by_imageId_titleId(conn, imageId, titleId):
    cursor = conn.cursor()
    sqlite_select_query = f"""SELECT * FROM [dbo].{config.sql["statistics_table_name"]} Where ImageId = '{imageId}' and TitleId = '{titleId}'"""
    cursor.execute(sqlite_select_query)
    record = cursor.fetchone()

    return record

def get_keyword_by_word_imageId_titleId(conn, keyword, imageId, titleId):
    cursor = conn.cursor()
    sqlite_select_query = f"""SELECT * FROM [dbo].{config.sql["keywords_table_name"]} Where Keyword = '{keyword}' and ImageId = '{imageId}' and TitleId = '{titleId}'"""
    cursor.execute(sqlite_select_query)
    record = cursor.fetchone()

    return record

def get_resources(conn, table_name):
    cursor = conn.cursor()
    sqlite_select_query = f'''SELECT * FROM {table_name}'''
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()

    return records

def insert_image(conn, stock, url, stockId=None):
    cursor = conn.cursor()
    existingImg = get_image_by_url(conn, url)

    if existingImg == None and stockId == None:
        cursor.execute(f"""insert INTO [dbo].{config.sql["images_table_name"]} 
                        (Stock, URL) 
                        OUTPUT inserted.id 
                        values (?, ?)""", 
                        (stock, url))
        id = cursor.fetchone()[0]
        cursor.commit()
        return id

    elif existingImg == None and stockId != None:
        cursor.execute(f"""insert INTO [dbo].{config.sql["images_table_name"]} 
                        (StockId, Stock, URL) 
                        OUTPUT inserted.id 
                        values (?, ?, ?)""", 
                        (stockId, stock, url))
        id = cursor.fetchone()[0]
        cursor.commit()
        return id

    else:
        return existingImg[0]
    
def update_lisence(conn, image_id, lisence):
    cursor = conn.cursor()
    query = f"""UPDATE [dbo].{config.sql["images_table_name"]} 
                        SET License = '{lisence}'
                        WHERE StockId = '{image_id}'"""
    cursor.execute(query)
    cursor.commit()

    return

def update_image_lisence(image_id, lisence):
    conn = open_connection()
    update_lisence(conn, image_id, lisence)
    close_connection(conn)
    return 
    
def insert_title(conn, description):
    cursor = conn.cursor()
    existingTitle = get_title_by_description(conn, description)
    
    if existingTitle == None:
        cursor.execute(f"""insert INTO [dbo].{config.sql["titles_table_name"]} 
                        (Description) 
                        OUTPUT inserted.id 
                        values (?)""", 
                        (description))
        id = cursor.fetchone()[0]
        cursor.commit()
        return id
    
    else:
        return existingTitle[0]
    
def insert_keyword(conn, keyword, imageId, titleId):
    cursor = conn.cursor()
    existingKeyword = get_keyword_by_word_imageId_titleId(conn, keyword, imageId, titleId)
    
    if existingKeyword == None:
        cursor.execute(f"""insert INTO [dbo].{config.sql["keywords_table_name"]} 
                        (Keyword, ImageId, TitleId) 
                        OUTPUT inserted.id 
                        values (?, ?, ?)""", 
                        (keyword, imageId, titleId))
        id = cursor.fetchone()[0]
        cursor.commit()
        return id

    else:
        return existingKeyword[0]
    
def insert_trace(conn, message):
    cursor = conn.cursor()
    cursor.execute(f"""insert INTO [dbo].{config.sql["traces_table_name"]} 
                    (Message) 
                    OUTPUT inserted.id 
                    values (?)""", 
                    (message))
    id = cursor.fetchone()[0]
    cursor.commit()

    return id

def insert_statistics(conn, imageId, titleId, ctr, cpm, score):
    cursor = conn.cursor()
    existingStats = get_statistics_by_imageId_titleId(conn, imageId, titleId)

    if existingStats == None:
        query = f"""insert INTO [dbo].{config.sql["statistics_table_name"]} 
                        (ImageId, TitleId, CTR, CPM, Score) 
                        values (?, ?, ?, ?, ?)"""
        cursor.execute(query, (imageId, titleId, ctr, cpm, score))

    else:
        query = f"""UPDATE [dbo].{config.sql["statistics_table_name"]} 
                        SET CTR = {ctr}, CPM = {cpm}, Score = {score}
                        WHERE ImageId = '{imageId}' and TitleId = '{titleId}'"""
        cursor.execute(query)

    cursor.commit()
    return      
    
    
def insert_creative_data(images, titles, keywords: Set):
    imagesIds = []
    titlesIds = []
    
    conn = open_connection()
    
    for image in images:
        imagesIds.append(insert_image(conn, image.stock, image.url, stockId=image.stock_id))

    for title in titles:
        titlesIds.append(insert_title(conn, title.description))

    close_connection(conn)
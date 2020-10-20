'''
SQL Introducción [Python]
Ejercicios de profundización
---------------------------
Autor: Inove Coding School
Version: 1.1

Descripción:
Programa creado para poner a prueba los conocimientos
adquiridos durante la clase.
El enunciado se encuentra en el archivo "ejercicio_profundizacion.md"
'''

__author__ = "Emmanuel O. Torres Molina"
__email__ = "emmaotm@gmail.com"
__version__ = "1.1"


import sqlite3
import csv


def ingresar_titulo_libro ( ):
    title = str(input('Ingrese el Título del Libro y luego Presione Enter: '))
    return title


def create_schema( ):
    
    print('\n\nCreando la Tabla...\n\n')

    # Me Conecto a la DB
    conn = sqlite3.connect('libreria.db')

    # Creo el cursor para realizar las query a la DB
    c = conn.cursor()
    c.execute(""" DROP TABLE IF EXISTS libro;""")
    c.execute("""
                CREATE TABLE libro (
                    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                    [title] TEXT NOT NULL,
                    [pags] INTEGER,
                    [author] TEXT
                );
    """)  

    conn.commit()
    conn.close()


def obtener_datos(archivo):
    # Obtengo los datos como una lista de diccionario.
    with open(archivo, 'r') as csvfile:
        data = list(csv.DictReader(csvfile))

    # Creo el dataset como una lista de tuplas.
    dataset = [(libro.get('titulo'), int(libro.get('cantidad_paginas')), libro.get('autor'))
                for libro in data]

    return dataset


def fill( ):
    archivo = 'libreria.csv'
    dataset = obtener_datos(archivo)

    conn = sqlite3.connect('libreria.db')
    c = conn.cursor()
    c.executemany(""" INSERT INTO libro (title, pags, author)
                    VALUES (?,?,?);""", dataset)

    conn.commit()
    conn.close()


def fetch(id):
    print('Muestro el Contenido de la Tabla...\n\n')

    data= obtener_datos('libreria.csv')

    conn = sqlite3.connect('libreria.db')
    c = conn.cursor()
    
    if id == 0:
        for row in c.execute(""" SELECT * FROM libro; """):
            print(row) 
    elif id > 0:
        if id <= len(data) :
            for row in c.execute(""" SELECT title, pags, author FROM libro WHERE id = ?; """, (id, )):
                print(row)
        else:
            print('Usted Ingresó un Número de Fila Incorrecto.')

    print('\n\n')

    conn.close()


def search_author (book_title):
    author = ()
    conn = sqlite3.connect('libreria.db')
    c = conn.cursor()
    for row in c.execute(""" SELECT author FROM libro WHERE title = ?; """, (book_title,)):
        author = row

    if author == ():
        return None
    else:
        return author[0]

    conn.close()


def update_title(id, new_title_book):
    conn = sqlite3.connect('libreria.db')
    c = conn.cursor()
    rowcount = c.execute(""" UPDATE libro SET title = ? WHERE id = ?; """, (new_title_book, id)).rowcount
    print('Cantidad de Filas Actualizadas: {}\n'.format(rowcount))

    conn.commit()
    conn.close()


def delete_libro (title):
    conn = sqlite3.connect('libreria.db')
    c = conn.cursor()
    rowcount = c.execute(""" DELETE FROM libro WHERE title = ?; """, (title,)).rowcount
    if rowcount == 0:
        print('Ingresó un Libro que No Existe en la Base de Datos.\n\n')
    else:
        print('Cantidad de Filas Eliminadas: {}\n\n'.format(rowcount))
    
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Crear DB:
    create_schema()

    # Completar la DB con el csv:
    fill()
    
    # Leer Filas:
    id = 0
    fetch(id)

    # Buscar Autor:
    book_title = ingresar_titulo_libro( )
    author = search_author(book_title)
    print('\nAutor: {}\n'.format(author))

    # Actualización de Título de Libro:
    new_book_title = ingresar_titulo_libro( )
    update_title(3, new_book_title)
    fetch(id=0)

    # Borrar Libro:
    title_book = ingresar_titulo_libro( )
    delete_libro(title_book)
    fetch(0)
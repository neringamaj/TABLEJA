import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()
dotenv_values(".env")
passw = os.getenv("POSTGRESQL_PASSWORD")

def insert_restaurant(id, title):
    db_params = {
        'dbname': 'hgqzogzv',
        'user': 'hgqzogzv',
        'password': passw,
        'host': 'isabelle.db.elephantsql.com',
        'port': '5432',
    }


    new_restaurant = {
        'id': id,
        'title': title,
    }

    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(**db_params)

        cursor = connection.cursor()

        insert_query = sql.SQL("INSERT INTO restaurants ({}) VALUES ({}) RETURNING *").format(
            sql.SQL(', ').join(map(sql.Identifier, new_restaurant.keys())),
            sql.SQL(', ').join(map(sql.Placeholder, new_restaurant.keys()))
        )

        cursor.execute(insert_query, new_restaurant)

        connection.commit()

        inserted_record = cursor.fetchone()
        print("Inserted Record:", inserted_record)

    except psycopg2.Error as e:
        print("Error:", e)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
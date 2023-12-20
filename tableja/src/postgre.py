import psycopg2
from psycopg2 import sql, extras
from dotenv import load_dotenv, dotenv_values
import os
from psycopg2.extensions import AsIs
load_dotenv()
password = os.getenv("POSTGRESQL_PASSWORD")

db_params = {
    'dbname': 'hgqzogzv',
    'user': 'hgqzogzv',
    'password': password,
    'host': 'isabelle.db.elephantsql.com',
    'port': '5432',
}
connection = None
cursor = None

def get_restaurant(id):
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        select_query = "SELECT * FROM restaurants WHERE id = %s"
        cursor.execute(select_query, (id,))

        restaurant = cursor.fetchone()
        print("Restaurant:", restaurant[2])

    except psycopg2.Error as e:
        print("Error:", e)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    return restaurant
    
def insert_restaurant(id, title, img_url):
    new_restaurant = {
        'id': id,
        'title': title,
        'img_url': img_url,
    }

    try:
        connection = psycopg2.connect(**db_params)
        
        extras.register_uuid()

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
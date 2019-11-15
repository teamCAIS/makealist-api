import psycopg2, traceback
from psycopg2.extras import RealDictCursor
import os

def raw(query, many):
    try:
        connection = psycopg2.connect(
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            host="127.0.0.1",
            port="5432",
            database="makealist",
        )
        curr = connection.cursor(cursor_factory=RealDictCursor)
        curr.execute(query)
        connection.commit()
        if curr.rowcount > 0:
            if many is False:
                response = curr.fetchone()
            elif many is True:
                response = curr.fetchall()
            else:
                response = {}
            return response

    except (Exception, psycopg2.Error) as error:
        traceback.print_exc()
        return jsonify(error)

    finally:
        if connection:
            curr.close()
            connection.close()

def get_item(table, id):
  return raw(f"select * from {table} where id={id}", False)
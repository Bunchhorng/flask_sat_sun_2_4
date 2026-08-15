import pymysql

def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        port=3309,
        database="sat_sun_2_5_flask_crud_db",
        cursorclass=pymysql.cursors.DictCursor
    )

conn = connect_db()
if conn:
    print("Connect database success!")

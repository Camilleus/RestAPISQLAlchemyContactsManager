import mysql.connector


def import_data_to_mysql():
    DATABASE_URL = "mysql+mysqlconnector://Camilleus:fghg1234@localhost/konigcontacts"
    
    mysql_conn = mysql.connector.connect(
        host="localhost",
        user="Camilleus",
        password="fghg1234",
        database="konigcontacts"
    )
    

    cursor = mysql_conn.cursor()


    try:
        with open("data_for_db.sql", "r") as sql_file:
            sql_commands = sql_file.read().split(';')

            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)


        mysql_conn.commit()
        print("Dane zostały zaimportowane do bazy MySQL.")
    except Exception as e:
        print(f"Błąd podczas importowania danych: {e}")
    finally:
        cursor.close()
        mysql_conn.close()

if __name__ == "__main__":
    import_data_to_mysql()

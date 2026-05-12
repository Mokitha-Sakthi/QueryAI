import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_mysql_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DATABASE", "test"),
            connection_timeout=5
        )
        return connection
    except Exception as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def get_mysql_schema():
    conn = get_mysql_connection()
    if not conn:
        return {"_error": "Could not connect to MySQL. Check credentials in .env file."}

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        schema = {}
        for table_dict in tables:
            table_name = list(table_dict.values())[0]
            cursor.execute(f"DESCRIBE `{table_name}`")
            columns = cursor.fetchall()
            schema[table_name] = [
                {"field": col["Field"], "type": col["Type"], "key": col["Key"]}
                for col in columns
            ]

        return schema
    except Exception as e:
        print(f"Error fetching MySQL schema: {e}")
        return {"_error": str(e)}
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

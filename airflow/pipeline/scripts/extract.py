import json
from mysql.connector import connect, Error, errorcode

JSON_FILE = "./data.json"

MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_DATABASE = "localdb"

def extract_data(json_file):
    with open(json_file, 'r') as file:
        return json.load(file) 

def transform_data(data):
    valid_messages = []
    error_logs = []

    for record in data:
        if "idMessage" in record:
            valid_messages.append((record["idMessage"],))
        elif "statusCode" in record:
            error_logs.append((
                record.get("statusCode"),
                record.get("timestamp"),
                record.get("path"),
                record.get("message"),
            ))
    
    return valid_messages, error_logs

def load_data_to_mysql(valid_messages, error_logs):
    try:
        connection = connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
        )
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS valid_messages (
            idMessage VARCHAR(255) PRIMARY KEY
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS error_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            statusCode INT,
            timestamp VARCHAR(255),
            path TEXT,
            message TEXT
        )
        """)

        if valid_messages:
            insert_valid_query = "INSERT IGNORE INTO valid_messages (idMessage) VALUES (%s)"
            cursor.executemany(insert_valid_query, valid_messages)

        if error_logs:
            insert_error_query = """
            INSERT INTO error_logs (statusCode, timestamp, path, message) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.executemany(insert_error_query, error_logs)

        connection.commit()

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def main():
    data = extract_data(JSON_FILE)
    valid_messages, error_logs = transform_data(data)
    load_data_to_mysql(valid_messages, error_logs)

if __name__ == "__main__":
    main()

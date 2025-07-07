import mysql.connector
from config import DB_CONFIG

def setup_database():
    try:
        # Koneksi tanpa database
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        
        # Baca file schema
        with open('models/schema.sql', 'r') as file:
            schema = file.read()
        
        # Eksekusi perintah SQL
        for statement in schema.split(';'):
            if statement.strip():
                cursor.execute(statement)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("Database berhasil disetup!")
        
    except Exception as e:
        print(f"Error setting up database: {str(e)}")

if __name__ == "__main__":
    setup_database() 
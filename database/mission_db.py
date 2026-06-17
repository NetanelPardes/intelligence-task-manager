import mysql.connector

class DBconnection:
    def __init__(self):
        self.host="localhost"
        self.port = 3306
        self.user="root"
        self.password="1234" 
        self.database = "Intelligence_db"
    
    def get_connection(self):
        return mysql.connector.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            password = self.password,
            database = self.database
        )
    def create_database(self):
        mydb = self.get_connection()
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS Intelligence_db")
    

if __name__ == "__main__":
    db = DBconnection()
    db.create_database()
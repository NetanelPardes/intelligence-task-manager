import mysql.connector

class DBconnection:
    def __init__(self):
        self.host="localhost"
        self.port = 3306
        self.user="root"
        self.password="1234" 
        self.database = "Intelligence_db"
    
    def get_connection(self):
        mysql.connector.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            password = self.password,
            database = self.database
        )
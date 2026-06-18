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
        mydb.close()
        mycursor.close()

    def create_tables(self):
        mydb = self.get_connection()
        mycursor = mydb.cursor()
        mycursor.execute("""
                        CREATE TABLE IF NOT EXISTS agents 
                        (id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(50) NOT NULL,
                        specialty VARCHAR(50) NOT NULL,
                        is_active BOOLEAN DEFAULT TRUE,
                        completed_missions INT DEFAULT 0,
                        failed_missions INT DEFAULT 0,
                        agent_rank ENUM('Junior' , 'Senior' , 'Commander') NOT NULL
                        )
                        """
                        )
        mydb.commit() 
        mycursor.execute("""
                        CREATE TABLE IF NOT EXISTS missions
                        (id INT AUTO_INCREMENT PRIMARY KEY,
                        title VARCHAR(50) NOT NULL,
                        description TEXT NOT NULL,
                        location VARCHAR(100) NOT NULL,
                        difficulty INT CHECK(difficulty BETWEEN 1 AND 10),
                        importance INT CHECK(importance BETWEEN 1 AND 10),
                        status ENUM('NEW','ASSIGNED','IN_PROGRESS','COMPLETED','FAILED','CANCELLED') DEFAULT 'NEW',
                        risk_level VARCHAR(50) NOT NULL,
                        assigned_agent_id INT NULL
                        )
                        """
                        )
        mydb.commit() 
        mycursor.close()
        mydb.close()
        

if __name__ == "__main__":
    db = DBconnection()
    db.create_database()
    db.create_tables()
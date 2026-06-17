from db_connection import DBconnection
import mysql.connector

class MissionDB:
    def __init__(self, conn: DBconnection):
        self.connection = conn
    
    def create_mission(self,data):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""INSERT INTO missions (title,description,location,difficulty,importance,risk_level) VALUES (%s,%s,%s,%s,%s,%s)""" ,
                        (data['title'],data['description'],data['location'],data['difficulty'],data['importance'],(data['difficulty']*2)+data['importance']))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        cursor.close()
        return self.get_mission_by_id(new_id)
    
    def get_all_missions(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM missions")
        missions = cursor.fetchall()
        conn.close()
        cursor.close()
        return missions
    
    def get_mission_by_id(self,id):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM missions WHERE id = %s" ,(id,))
        mission = cursor.fetchone()
        conn.close()
        cursor.close()
        return mission
    
    def assign_mission(self,m_id, a_id):
        pass
    
    def update_mission_status(self,id, status):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("UPDATE missions SET status = %s WHERE id = %s" ,(status,id))
        conn.commit()
        changed = cursor.rowcount > 0
        conn.close()
        cursor.close()
        return changed
    
    def get_open_missions_by_agent(self,id):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM missions WHERE assigned_agent_id = %s AND status = 'ASSIGNED' OR status = 'IN_PROGRESS'  " ,(id,))
        mission = cursor.fetchall()
        conn.close()
        cursor.close()
        return mission

    def count_all_missions(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT count(*) as missions_count FROM missions")
        mission = cursor.fetchone()
        conn.close()
        cursor.close()
        return mission
    
    def count_by_status(self,status):
        pass
    def count_open_missions(self,):
        pass
    def count_critical_missions(self,):
        pass
    def defget_top_agent(self,):
        pass

if __name__ == "__main__":
    connection = DBconnection()
    mission = MissionDB(connection)
    #print(mission.create_mission({"title":"dangerous","description": "Eliminate Khamenei","location":"Tehran, Iran","difficulty":6,"importance":8}))
    #print(mission.update_mission_status(2,"IN_PROGRESS"))
    #print(mission.get_open_missions_by_agent(2))
    print(mission.count_all_missions())

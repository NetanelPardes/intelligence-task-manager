from database.db_connection import DBconnection
import mysql.connector

conn = DBconnection()

class MissionDB:
    def __init__(self):
        self.connection = conn
    
    def create_mission(self,data):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""INSERT INTO missions (title,description,location,difficulty,importance,risk_level) VALUES (%s,%s,%s,%s,%s,%s)""" ,
                        (data['title'],data['description'],data['location'],data['difficulty'],data['importance'],(data['risk_level'])))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        
        return self.get_mission_by_id(new_id)
    
    def get_all_missions(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM missions")
        missions = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return missions
    
    def get_mission_by_id(self,id):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM missions WHERE id = %s" ,(id,))
        mission = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return mission
    
    def assign_mission(self,m_id, a_id):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("UPDATE missions SET assigned_agent_id = %s , status = 'ASSIGNED' WHERE id = %s" ,(a_id,m_id))
        conn.commit()
        changed = cursor.rowcount > 0
        cursor.close()
        conn.close()
        
        return changed
    
    def update_mission_status(self,id, status):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("UPDATE missions SET status = %s WHERE id = %s" ,(status,id))
        conn.commit()
        changed = cursor.rowcount > 0
        cursor.close()
        conn.close()
        
        return changed
    
    def get_open_missions_by_agent(self,id):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM missions WHERE assigned_agent_id = %s AND status = 'ASSIGNED' OR status = 'IN_PROGRESS'  " ,(id,))
        mission = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return mission

    def count_all_missions(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT count(*) as missions_count FROM missions")
        mission = cursor.fetchone()
        cursor.close()
        conn.close()
       
        return mission
    
    def count_by_status(self,status):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT count(*) as missions_count FROM missions WHERE status = %s" ,(status,))
        missions = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return missions
    
    def count_open_missions(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT count(*) as open_missions_count FROM missions WHERE status = 'NEW' OR status = 'ASSIGNED' OR status = 'IN_PROGRESS'")
        missions = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return missions

    def count_critical_missions(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT count(*) as critical_missions FROM missions WHERE risk_level = %s" ,('CRITICAL',))
        critical_missions = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return critical_missions

    def defget_top_agent(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT assigned_agent_id ,count(*) as completed_missions FROM missions WHERE status = 'completed' GROUP BY assigned_agent_id ORDER BY completed_missions DESC LIMIT 1")
        critical_missions = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return critical_missions
    
    def too_much_open_misshins(self,agent_id):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT count(*) as open_missions FROM missions WHERE assigned_agent_id = %s AND status IN ('ASSIGNED','IN_PROGRESS')",(agent_id,))
        oprn_missions = cursor.fetchone()
        cursor.close()
        conn.close()
        return oprn_missions['open_missions']

    
    def check_importance_and_difficulty (self,importance, difficulty ):
        if (1 <= importance <= 10) and (1 <= difficulty <= 10):
            return True
        return False


    

    


if __name__ == "__main__":
    connection = DBconnection()
    mission = MissionDB(connection)
    # print(mission.create_mission({"title":"dangerous","description": "Eliminate Khamenei","location":"Tehran, Iran","difficulty":1,"importance":1,'risk_level' : "LOW"}))
    # print(mission.create_mission({"title":"dangerous","description": "Eliminate Khamenei","location":"Tehran, Iran","difficulty":4,"importance":3,'risk_level' : "MEDIUM"}))
    #print(mission.update_mission_status(5,"COMPLETED"))
    #print(mission.get_open_missions_by_agent(2))
    #print(mission.count_all_missions())
    # print(mission.count_by_status('NEW'))
    # print(mission.count_by_status('ASSIGNED'))
    #print(mission.count_critical_missions())
    #print(mission.defget_top_agent())
    #print(mission.count_open_missions())
    #print(mission.assign_mission(1,2))
    print(mission.too_much_open_misshins(1))
    # print(mission.check_importance_and_difficulty(1,2))
    # print(mission.check_importance_and_difficulty(0,2))
    # print(mission.check_importance_and_difficulty(11,2))
    # print(mission.check_importance_and_difficulty(1,0))
    # print(mission.check_importance_and_difficulty(1,12))
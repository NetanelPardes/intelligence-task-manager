from db_connection import DBconnection
import mysql.connector

class AgentDB:
    def __init__(self, conn: DBconnection):
        self.connection = conn

    def create_agent(self,data):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("INSERT INTO agents (name, specialty, agent_rank) VALUES (%s,%s,%s)",(data['name'],data['specialty'],data['agent_rank']))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        cursor.close()
        return self.get_agent_by_id(new_id)

    def get_all_agents(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM agents")
        agents = cursor.fetchall()
        conn.close()
        cursor.close()
        return agents

    def get_agent_by_id(self,id):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM agents WHERE id = %s" ,(id,))
        agent = cursor.fetchone()
        conn.close()
        cursor.close()
        return agent

    def update_agent(self,id, data):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        all_keys = [f"{key} = %s" for key in data.keys()]
        set_close = " ,".join(all_keys)
        sql = f"UPDATE agents SET {set_close} WHERE id = %s"
        values = list(data.values()) + [id]
        cursor.execute(sql,values)
        conn.commit()
        changed = cursor.rowcount > 0
        conn.close()
        cursor.close()
        return changed

    def deactivate_agent(self,id):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("UPDATE agents SET is_active = FALSE WHERE id = %s" ,(id,))
        conn.commit()
        changed = cursor.rowcount > 0
        conn.close()
        cursor.close()
        return changed
    
    def increment_completed(self,id):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("UPDATE agents SET completed_missions = completed_missions + 1 WHERE id = %s" ,(id,))
        conn.commit()
        changed = cursor.rowcount > 0
        conn.close()
        cursor.close()
        return changed

    def increment_failed(self,id):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("UPDATE agents SET failed_missions = failed_missions + 1 WHERE id = %s" ,(id,))
        conn.commit()
        changed = cursor.rowcount > 0
        conn.close()
        cursor.close()
        return changed

    def get_agent_performance(self,id):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT completed_missions as completed , failed_missions as failed ,completed_missions + failed_missions as total, (completed_missions /(completed_missions + failed_missions))*100 as Success_percent FROM agents WHERE id = %s" ,(id,))
        missions = cursor.fetchall()
        conn.close()
        cursor.close()
        return missions

    def count_active_agents(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT count(*) as active_agents from agents WHERE is_active = TRUE" )
        active_agent = cursor.fetchone()
        conn.close()
        cursor.close()
        return active_agent

if __name__ == "__main__":
    connection = DBconnection()
    agent = AgentDB(connection)
    # agent.create_agent({'name':"Netanel" , 'specialty' : "Terrorists" , 'agent_rank' : "Junior"})
    #agent.update_agent(3,{'specialty' : "women"})
    #agent.deactivate_agent(4)
    # agent.increment_completed(4)
    print(agent.get_agent_performance(3))
    #print(agent.count_active_agents())

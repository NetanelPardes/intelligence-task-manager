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
        pass

    def get_agent_by_id(self,id):
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM agents WHERE id = %s" ,(id,))
        agent = cursor.fetchone()
        conn.close()
        cursor.close()
        return agent

    def update_agent(self,id, data):
        pass

    def deactivate_agent(self,id):
        pass
    
    def increment_completed(self,id):
        pass

    def increment_failed(self,id):
        pass

    def get_agent_performance(self,id):
        pass

    def count_active_agents(self):
        pass

if __name__ == "__main__":
    connection = DBconnection()
    agent = AgentDB(connection)
    # agent.create_agent({'name':"Netanel" , 'specialty' : "Terrorists" , 'agent_rank' : "Junior"})
    #agent.update_agent(3,{'specialty' : "women"})
    #agent.deactivate_agent(4)
    # agent.increment_completed(4)

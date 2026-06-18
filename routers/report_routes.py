from fastapi import APIRouter,HTTPException
from database.agent_db import AgentDB
from database.mission_db import MissionDB

my_agent = AgentDB()
my_mission = MissionDB()

router = APIRouter()

@router.get("/summary/reports")
def report():
    return{"active_agents_count" : my_agent.count_active_agents()["active_agents"],
           "total_missions": my_mission.count_all_missions()["missions_count"],
            "open_missions": my_mission.count_open_missions()["open_missions_count"],
            "completed_missions": my_mission.count_by_status('COMPLETED')["missions_count"],
            "failed_missions": my_mission.count_by_status('FAILED')["missions_count"],
            "critical_missions": my_mission.count_critical_missions()["critical_missions"]
           }

@router.get("/reports/missions-by-status")
def missions_by_status():
    return{"open":my_mission.count_by_status('ASSIGNED')["missions_count"],
            "in_progress": my_mission.count_by_status('IN_PROGRESS')["missions_count"],
            "completed": my_mission.count_by_status('COMPLETED')["missions_count"],
            "failed": my_mission.count_by_status('FAILED')["missions_count"],
            "canceled": my_mission.count_by_status('CANCELLED')["missions_count"]}

@router.get("/reports/top-agent")
def the_best_agent():
    return {"the best agent": my_mission.defget_top_agent()["assigned_agent_id"]}
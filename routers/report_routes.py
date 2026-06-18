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

# @router.get("/reports/missions-by-status")
# @router.get("/reports/top-agent - Outstanding Agent")
from fastapi import APIRouter,HTTPException
from database.agent_db import AgentDB
from database.mission_db import MissionDB

my_agent = AgentDB()
my_mission = MissionDB()

router = APIRouter()

@router.post("/missions",status_code=201) 
def add_new_mission(new_mission:dict):
    if  'title' in new_mission and new_mission['title']:
        if  'description' in new_mission and new_mission['description']:
            if 'location' in new_mission and new_mission['location']:
                if 'difficulty' in new_mission and new_mission['difficulty']:
                    if  'importance' in new_mission and new_mission['importance'] :
                        if my_mission.check_importance_and_difficulty(new_mission['importance'] ,new_mission['difficulty']):
                            risk = new_mission['difficulty'] * 2 + new_mission['importance']
                            if 0 < risk < 10:
                                risk_level = "LOW"
                            elif risk < 18:
                                risk_level = "MEDIUM" 
                            elif risk < 25:
                                risk_level = "HIGH"
                            else:
                                risk_level = "CRITICAL"
                            new_mission['risk_level'] = risk_level
                            return {"data" : my_mission.create_mission(new_mission)}
                        else:
                            raise HTTPException(status_code=400,detail="Importance and difficulty should be between 1 and 10.")
                    else:
                        raise HTTPException(status_code=422,detail="The creation is missing a importance object.")
                else:
                    raise HTTPException(status_code=422,detail="The creation is missing a difficulty object.")
            else:
                raise HTTPException(status_code=422,detail="The creation is missing a location object.")
        else:
            raise HTTPException(status_code=422,detail="The creation is missing a description object.")
    else:
        raise HTTPException(status_code=422,detail="The creation is missing a title object.")
                        

@router.get("/missions")
def get_all_missions():
    return {"data":my_mission.get_all_missions()}

@router.get("/missions/{id}")
def mission_by_id(id):
    mission = my_mission.get_mission_by_id(id)
    if not mission:
        raise HTTPException(status_code=404, detail="The mission does not exist in the system.")
    return {"data":mission}

@router.put("/missions/{id}/assign/{agent_id}")
def Assign_mission_agent(id, agent_id):
    if my_agent.get_agent_by_id(agent_id):
        if my_mission.get_mission_by_id(id):
            if my_mission.get_mission_by_id(id)['status'] == 'NEW':
                if my_agent.check_is_active(agent_id):
                    if my_mission.too_much_open_misshins(agent_id) <= 3:
                        if my_mission.get_mission_by_id(id)['risk_level'] == 'CRITICAL' and my_agent.get_agent_by_id(agent_id)['agent_rank'] == 'Commander':
                            my_mission.assign_mission(id, agent_id)
                            return {"message" : f"mission {id} assign to agent {agent_id}"}
                        else:
                            raise HTTPException(status_code=400,detail="The mission is critical and only a commander can carry it out.")
                    else:
                        raise HTTPException(status_code=400,detail="The agent has more than 3 active tasks.")
                else:
                    raise HTTPException(status_code=400,detail="The agent is inactive.")
            else:
                raise HTTPException(status_code=400,detail="Cannot assign a task with a status other than NEW.")
        else:
            raise HTTPException(status_code=404,detail="The task does not exist in the system.")
    else:
        raise HTTPException(status_code=404,detail="The agent does not exist in the system.")


@router.put("/missions/{id}/start")
def staet_mission(id):
    mission = my_mission.get_mission_by_id(id)
    if not mission:
        raise HTTPException(status_code=404, detail="The mission does not exist in the system.")
    if mission['status'] == 'ASSIGNED':
        my_mission.update_mission_status(id,'IN_PROGRESS')
    else:
        raise HTTPException(status_code=400,detail="A task cannot start if it is not in the ASSIGNED status.")


# @router.put("/missions/{id}/complete") # - Complete a mission successfully
# @router.put("/missions/{id}/fail") # - Complete a mission with failure
# @router.put("/missions/{id}/cancel") # - Cancel a mission
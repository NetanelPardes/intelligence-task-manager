from fastapi import APIRouter,HTTPException
from database.agent_db import AgentDB
from database.mission_db import MissionDB
import logging
logger = logging.getLogger(__name__)

my_agent = AgentDB()
my_mission = MissionDB()

router = APIRouter()

@router.post("/missions",status_code=201) 
def add_new_mission(new_mission:dict):
    logger.info("A request to add a new task has been received.")
    if not 'title' in new_mission or not new_mission['title']:
        logger.error("The creation is missing a title object.")
        raise HTTPException(status_code=422,detail="The creation is missing a title object.")
    if not 'description' in new_mission or not new_mission['description']:
        logger.error("The creation is missing a description object.")
        raise HTTPException(status_code=422,detail="The creation is missing a description object.")
    if not 'location' in new_mission or not new_mission['location']:
        logger.error("The creation is missing a location object.")
        raise HTTPException(status_code=422,detail="The creation is missing a location object.")
    if not 'difficulty' in new_mission or not new_mission['difficulty']:
        logger.error("The creation is missing a difficulty object.")
        raise HTTPException(status_code=422,detail="The creation is missing a difficulty object.")
    if not 'importance' in new_mission or not new_mission['importance'] :
        logger.error("The creation is missing a importance object.")
        raise HTTPException(status_code=422,detail="The creation is missing a importance object.")
    if not my_mission.check_importance_and_difficulty(new_mission['importance'] ,new_mission['difficulty']):
        logger.error("Importance and difficulty should be between 1 and 10.")
        raise HTTPException(status_code=400,detail="Importance and difficulty should be between 1 and 10.")
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
    logger.info("New task added successfully.")
    return {"data" : my_mission.create_mission(new_mission)}
                             

@router.get("/missions")
def get_all_missions():
    logger.info("A request to view all tasks has been received.")
    logger.info("All tasks were successfully submitted.")
    return {"data":my_mission.get_all_missions()}

@router.get("/missions/{id}")
def mission_by_id(id:int):
    logger.info("A request to display a task by id has been received.")
    mission = my_mission.get_mission_by_id(id)
    if not mission:
        logger.error("The mission does not exist in the system.")
        raise HTTPException(status_code=404, detail="The mission does not exist in the system.")
    logger.info("Task by id successfully displayed")
    return {"data":mission}

@router.put("/missions/{id}/assign/{agent_id}")
def Assign_mission_agent(id:int, agent_id:int):
    logger.info("A request to assign a task to an agent has been received.")
    if not my_agent.get_agent_by_id(agent_id):
        logger.error("The agent does not exist in the system.")
        raise HTTPException(status_code=404,detail="The agent does not exist in the system.")
    if my_mission.get_mission_by_id(id):
        logger.error("The task does not exist in the system.")
        raise HTTPException(status_code=404,detail="The task does not exist in the system.")
    if my_mission.get_mission_by_id(id)['status'] == 'NEW':
        logger.error("Cannot assign a task with a status other than NEW.")
        raise HTTPException(status_code=400,detail="Cannot assign a task with a status other than NEW.")
    if my_agent.check_is_active(agent_id):
        logger.error("The agent is inactive.")
        raise HTTPException(status_code=400,detail="The agent is inactive.")
    if my_mission.too_much_open_misshins(agent_id) < 3:
        logger.error("The agent has more than 3 active tasks.")
        raise HTTPException(status_code=400,detail="The agent has more than 3 active tasks.")
    if my_mission.get_mission_by_id(id)['risk_level'] == 'CRITICAL': 
        if my_agent.get_agent_by_id(agent_id)['agent_rank'] != 'Commander':
            logger.error("The mission is critical and only a commander can carry it out.")
            raise HTTPException(status_code=400,detail="The mission is critical and only a commander can carry it out.")
    changed = my_mission.assign_mission(id, agent_id)
    if not changed:
        raise HTTPException(status_code=400,detail="Something is not working.")
    logger.info("The task was successfully assigned to the agent.")
    return {"message" : f"mission {id} assign to agent {agent_id}"}
        


@router.put("/missions/{id}/start")
def staet_mission(id:int):
    logger.info("A request to start a task has been received.")
    mission = my_mission.get_mission_by_id(id)
    if not mission:
        logger.error("The mission does not exist in the system.")
        raise HTTPException(status_code=404, detail="The mission does not exist in the system.")
    if mission['status'] == 'ASSIGNED':
        my_mission.update_mission_status(id,'IN_PROGRESS')
        logger.info("Mission started")
        return {"message": f"mission {id} Started"}
    else:
        logger.error("A task cannot start if it is not in the ASSIGNED status.")
        raise HTTPException(status_code=400,detail="A task cannot start if it is not in the ASSIGNED status.")


@router.put("/missions/{id}/complete") 
def complete_mission(id:int):
    logger.info("A request to complete a task was successfully received.")
    mission = my_mission.get_mission_by_id(id)
    if not mission:
        logger.error("The mission does not exist in the system.")
        raise HTTPException(status_code=404, detail="The mission does not exist in the system.")
    if mission['status'] == 'IN_PROGRESS':
        my_mission.update_mission_status(id,'COMPLETED')
        logger.info("Task completed successfully")
        return {"message": f"mission {id} Successfully completed"}
    else:
        logger.error("A task cannot start if it is not in the IN_PROGRESS status.")
        raise HTTPException(status_code=400,detail="A task cannot start if it is not in the IN_PROGRESS status.")
    
@router.put("/missions/{id}/fail")
def fail_mission(id:int):
    logger.info("A request to end a task has been received with failure.")
    mission = my_mission.get_mission_by_id(id)
    if not mission:
        logger.error("The mission does not exist in the system.")
        raise HTTPException(status_code=404, detail="The mission does not exist in the system.")
    if mission['status'] == 'IN_PROGRESS':
        my_mission.update_mission_status(id,'FAILED')
        logger.info("Mission failed")
        return {"message": f"mission {id} Ended in failure"}
    else:
        logger.error("A task cannot start if it is not in the IN_PROGRESS status.")
        raise HTTPException(status_code=400,detail="A task cannot start if it is not in the IN_PROGRESS status.")
    
@router.put("/missions/{id}/cancel") 
def cancel_mission(id:int):
    logger.info("A request to cancel a task has been received.")
    mission = my_mission.get_mission_by_id(id)
    if not mission:
        logger.error("The mission does not exist in the system.")
        raise HTTPException(status_code=404, detail="The mission does not exist in the system.")
    if mission['status'] == 'NEW' or mission['status'] =='ASSIGNED':
        my_mission.update_mission_status(id,'CANCELLED')
        logger.info("Task successfully canceled")
        return {"message": f"mission {id} canceled"}
    else:
        logger.error("A task cannot start if it is not in the IN_PROGRESS status.")
        raise HTTPException(status_code=400,detail="A task cannot start if it is not in the IN_PROGRESS status.")
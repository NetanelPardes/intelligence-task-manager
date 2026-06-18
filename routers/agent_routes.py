from fastapi import APIRouter,HTTPException
from database.agent_db import AgentDB
import logging
from logging_config import logger

logger = logging.getLogger(__name__)

my_agent = AgentDB()

router = APIRouter()



@router.post("/agents",status_code=201)
def add_new_agents(new_agent:dict):
    logger.info("Request to add an agent has been received.")
    if not 'name' in new_agent or not new_agent['name']:
        logger.error("There is no name")
        raise HTTPException(status_code=422,detail="There is no name.")
    if not 'agent_rank' in new_agent or not new_agent['agent_rank']:
        logger.error("There is no agent_rank")
        raise HTTPException(status_code=422,detail="There is no agent_rank.")
    if not 'specialty' in new_agent or not new_agent['specialty']:
        logger.error("There is no specialty")
        raise HTTPException(status_code=422,detail="There is no specialty.")
    if new_agent['agent_rank'] not in ('Junior' , 'Senior' , 'Commander'):
        logger.error("Invalid agent rank")
        raise HTTPException(status_code=400,detail="Invalid agent rank.")
    logger.info("Agent added successfully")
    return {"data": my_agent.create_agent(new_agent)}
    
    
@router.get("/agents",status_code=200)
def all_agents():
    logger.info("A request to display all agents has been received.")
    logger.info("All agents were successfully introduced.")
    return {"data":my_agent.get_all_agents()}

@router.get("/agents/{id}",status_code=200)
def agent_by_id(id:int):
        logger.info("A request to display an agent by id has been received.")
        agent = my_agent.get_agent_by_id(id)
        if not agent:
            logger.error("The agent does not exist in the system.")
            raise HTTPException(status_code=404, detail="The agent does not exist in the system.")
        logger.info("Agent by id successfully displayed")
        return {"data":agent}
        
    
@router.put("/agents/{id}",status_code=200)
def update_agents(id:int,new_data:dict):
    logger.info("A request to update an agent has been received.")
    agent = my_agent.get_agent_by_id(id)
    if not agent:
        logger.error("The agent does not exist in the system.")
        raise HTTPException(status_code=404, detail="The agent does not exist in the system.")
    if not new_data:
        logger.error("No data to update")
        raise HTTPException(status_code=422 , detail="No data to update")
    my_agent.update_agent(id,new_data)
    logger.info("Agent updated successfully")
    return {"message": f"agent {id} update successfully"}
    

@router.put ("/agents/{id}/deactivate",status_code=200)
def make_agent(id:int):
    logger.info("A request to deactivate an agent has been received.")
    agent = my_agent.get_agent_by_id(id)
    if not agent:
        logger.error("The agent does not exist in the system.")
        raise HTTPException(status_code=404, detail="The agent does not exist in the system.")
    my_agent.deactivate_agent(id)
    logger.info("Inactive agent")
    return {"message": f"agent {id} deactivate"}

@router.get ("/agents/{id}/performance",status_code=200)
def get_performance(id:int):
    logger.info("A request has been received to display the agent with the most completed tasks.")
    agent = my_agent.get_agent_by_id(id)
    if not agent:
        logger.error("The agent does not exist in the system.")
        raise HTTPException(status_code=404, detail="The agent does not exist in the system.")
    logger.info("Agent with the most completed tasks successfully introduced")
    return {"data" : my_agent.get_agent_performance(id)}


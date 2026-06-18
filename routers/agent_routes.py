from fastapi import APIRouter,HTTPException
from database.agent_db import AgentDB

my_agent = AgentDB()

router = APIRouter()



@router.post("/agents",status_code=201)
def add_new_agents(new_agent:dict):
    if new_agent['name'] and 'name' in new_agent:
        if new_agent['agent_rank'] and 'agent_rank' in new_agent:
            if new_agent['specialty']and 'specialty' in new_agent:
                if new_agent['agent_rank'] in ('Junior' , 'Senior' , 'Commander'):
                    return {"data": my_agent.create_agent(new_agent)}
                else:
                    raise HTTPException(status_code=400,detail="Invalid agent rank.")
            else:
                raise HTTPException(status_code=422,detail="There is no specialty.")
        else:
            raise HTTPException(status_code=422,detail="There is no agent_rank.")
    else:
        raise HTTPException(status_code=422,detail="There is no name.")
    
    
@router.get("/agents",status_code=200)
def all_agents():
    return {"data":my_agent.get_all_agents()}

@router.get("/agents/{id}",status_code=200)
def agent_by_id(id):
        # if not isinstance(id,('int',)):
        #     raise HTTPException(status_code=422, detail="That's not a number.")
        agent = my_agent.get_agent_by_id(id)
        if not agent:
            raise HTTPException(status_code=404, detail="The agent does not exist in the system.")
        return {"data":agent}
        
    
@router.put("/agents/{id}")
def update_agents(id,new_data:dict):
#     if id != int:
#         raise HTTPException(status_code=422, detail="That's not a number.")
    agent = my_agent.get_agent_by_id(id)
    if not agent:
        raise HTTPException(status_code=404, detail="The agent does not exist in the system.")
    if not new_data:
        raise HTTPException(status_code=422 , detail="No data to update")
    my_agent.update_agent(id,new_data)
    return {"message": f"agent {id} update successfully"}
    

@router.put ("/agents/{id}/deactivate")
def make_agent(id):
    agent = my_agent.get_agent_by_id(id)
    if not agent:
        raise HTTPException(status_code=404, detail="The agent does not exist in the system.")
    my_agent.deactivate_agent(id)
    return {"message": f"agent {id} deactivate"}

@router.get ("/agents/{id}/performance")
def get_performance(id):
    agent = my_agent.get_agent_by_id(id)
    if not agent:
        raise HTTPException(status_code=404, detail="The agent does not exist in the system.")
    return {"data" : my_agent.get_agent_performance(id)}

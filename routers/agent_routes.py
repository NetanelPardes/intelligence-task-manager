from fastapi import APIRouter,HTTPException
from database.agent_db import AgentDB

agent = AgentDB()

router = APIRouter()



@router.post("/agents",status_code=201)
def add_new_agents(new_agent:dict):
    if new_agent['agent_rank'] in ('Junior' , 'Senior' , 'Commander'):
        if new_agent['name']:
            if new_agent['agent_rank']:
                if new_agent['specialty']:
                    return {"message": agent.create_agent(new_agent)}
                else:
                    raise HTTPException(status_code=422,detail="There is no specialty.")
            else:
                raise HTTPException(status_code=422,detail="There is no agent_rank.")
        else:
            raise HTTPException(status_code=422,detail="There is no name.")
    else:
        raise HTTPException(status_code=400,detail="Invalid agent rank.")
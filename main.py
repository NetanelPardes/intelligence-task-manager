from fastapi import FastAPI
from routers.agent_routes import router as ag_router
from routers.mission_routes import router as miss_router
from routers.report_routes import router as rep_router
import uvicorn

app = FastAPI()

app.include_router(ag_router)
app.include_router(miss_router)
app.include_router(rep_router)

@app.get("/")
def server_work():
    return{"server":"work"}

if __name__ == "__main__":
    uvicorn.run("main:app" ,reload=True)
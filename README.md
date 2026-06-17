# intelligence task manager
## System description
The system manages communication between tasks and agents
The goal of the project is to create and manage data of tasks and agents and communicate between them
## Folder structure
```
intelligence-task-manager/
├── database/
│   ├── db_connection.py
│   ├── agent_db.py
│   └── mission_db.py
├── README.md
├── requirements.txt
└── .gitignore
```
## Table structure

### Agents table

| field | type | Notes |
|-------|------|-------|
| id | INT | Unique key | 
| name | VARCHAR(50) | Agent name | 
| specialty | VARCHAR(50) | Field of specialization |
| is_active | BOOLEAN | Default: TRUE |
| completed_missions | INT | Default: 0 |
| failed_missions | INT | Default: 0 |
|agent_rank | ENUM / VARCHAR | Junior / Senior / Commander only |

### Mission table

| field | type | Notes |
|-------|------|-------|
| id | INT | Unique Key |  
| title | VARCHAR(50) | Task Title |
| description | TEXT | Detailed Description |
| location | VARCHAR(100) | Location |
| difficulty | INT | 1–10 Only |
| importance | INT | 1–10 Only |
| status | VARCHAR(20) | Default: NEW |
| risk_level | VARCHAR(20) | Auto-calculated |
| assigned_agent_id | INT | NULL until associated |

## Explanation about departments

### db_connection
The class defines our connection to the MYSQL server.
#### Methods
```
get_connection() - Connecting to the NYSQL server
create_database() - Creating a database
create_tables() - Creating the tables
```

### AgentDB
The class defines the agent, and the agent database requests.
#### Methods
```
create_agent(data) - Creates a new agent and returns the agent object
get_all_agents() - Returns a list of all agents
get_agent_by_id(id) - Returns one agent by ID, or None
update_agent(id, data) - UPDATE the entire row
deactivate_agent(id) - Sets agent status to inactive
increment_completed(id) - Updates the number of completed tasks
increment_failed(id) - Updates the number of failed tasks
get_agent_performance(id) - Returns a dictionary with these keys completed, failed, total, success_rate
count_active_agents() - Returns the number of active agents
```

### MissionDB 
The department defines the tasks, and the requests to the task database.
#### Methods
```
create_mission(data) -Creates a new task and returns the entire object
get_all_missions() - Returns all tasks
get_mission_by_id(id) - Returns one task by ID, or None
assign_mission(m_id, a_id) - Assigns a task to an agent
update_mission_status(id, status) - Used for any status change
get_open_missions_by_agent(id) - Returns ASSIGNED/IN_PROGRESS tasks of an agent
count_all_missions() Return total tasks
count_by_status(status) - Return counts by a specific status
count_open_missions() - Return counts open tasks
count_critical_missions() Return counts CRITICAL tasks
get_top_agent() - Return agent with the highest completed_missions
```
## System rules
```
1 rank must be Junior / Senior / Commander — any other value throws an error.
2 difficulty and importance must be between 1 and 10 — otherwise an error.
3 risk_level is calculated automatically when creating a task — the user does not submit it.
4 An agent with is_active=False cannot accept tasks.
5 An agent cannot have more than 3 open tasks (ASSIGNED / IN_PROGRESS) at the same time.
6 If risk_level=CRITICAL — only an agent with the Commander rank can accept the task.
7 Only a task with the status NEW can be assigned. After assignment: status=ASSIGNED.
8 Only a task with the status ASSIGNED can be started. After: status=IN_PROGRESS.
9 Only a task with the status IN_PROGRESS can be finished and changed to failed or completed.
10 Only a task with the status NEW or ASSIGNED can be canceled — otherwise an error.
```

## Running instructions
Step One - Running the MYSQL Server
```powershell
docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0
```

Step Two - Install the add-ons for this project
```powershell
pip freeze > requirements.txt
```
```powershell
pip install requirements.txt
``` 
Step Three - Run the Main File
```powershell
python main.py
```
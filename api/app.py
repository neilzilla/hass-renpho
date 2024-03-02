from fastapi import FastAPI, Request, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os

from .api_renpho import RenphoWeight

# Initialize FastAPI and Jinja2
app = FastAPI(docs_url="/docs", redoc_url=None)

current_directory = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(current_directory, "templates"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBasic()


async def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    try:
        return RenphoWeight(credentials.username, credentials.password)
    except Exception as e:
        # Log the error here if you want
        raise HTTPException(
            status_code=401, detail="MarketWatch validation failed"
        ) from e


@app.get("/")
def read_root(request: Request):
    return "Renpho API"

@app.get("/auth")
async def auth(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        await renpho.auth()
        return {"status": "success", "message": "Authentication successful."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/info")
async def get_info(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        await renpho.get_info()
        return {"status": "success", "message": "Fetched user info."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/users")
async def get_scale_users(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        users = await renpho.get_scale_users()
        return {"status": "success", "message": "Fetched scale users.", "data": users}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/measurements")
async def get_measurements(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        measurements = await renpho.get_measurements()
        return {"status": "success", "message": "Fetched measurements.", "data": measurements}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/weight")
async def get_weight(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        weight = await renpho.get_weight()
        return {"status": "success", "message": "Fetched weight.", "data": weight[0]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/specific_metric")
async def get_specific_metric(request: Request, metric: str, metric_id: str, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        specific_metric = await renpho.get_specific_metric(metric, metric_id)
        return {"status": "success", "message": f"Fetched specific metric: {specific_metric}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/device_info")
async def get_device_info(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        device_info = await renpho.get_device_info()
        return {"status": "success", "message": "Fetched device info.", "data": device_info}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/latest_model")
async def list_latest_model(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        latest_model = await renpho.list_latest_model()
        return {"status": "success", "message": "Fetched latest model.", "data": latest_model}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/girth_info")
async def list_girth(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        girth_info = await renpho.list_girth()
        return {"status": "success", "message": "Fetched girth info.", "data": girth_info}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/girth_goal")
async def list_girth_goal(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        girth_goal = await renpho.list_girth_goal()
        return {"status": "success", "message": "Fetched girth goal.", "data": girth_goal}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/growth_record")
async def list_growth_record(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        growth_record = await renpho.list_growth_record()
        return {"status": "success", "message": "Fetched growth record.", "data": growth_record}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/message_list")
async def message_list(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        messages = await renpho.message_list()
        return {"status": "success", "message": "Fetched message list.", "data": messages}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/reach_goal")
async def reach_goal(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        reach_goal = await renpho.reach_goal()
        return {"status": "success", "message": "Fetched reach_goal.", "data": reach_goal}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/request_user")
async def request_user(request: Request, renpho: RenphoWeight = Depends(get_current_user)):
    try:
        request_user = await renpho.request_user()
        return {"status": "success", "message": "Fetched request user.", "data": request_user}
    except Exception as e:
        return {"status": "error", "message": str(e)}

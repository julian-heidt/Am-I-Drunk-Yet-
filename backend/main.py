import logging
from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from prometheus_fastapi_instrumentator import Instrumentator
from pythonjsonlogger import jsonlogger
from calculator import calculate_drinks_to_target_bac, calculate_time_to_sober
from fastapi.middleware.cors import CORSMiddleware

# --- Structured Logging Setup ---
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    fmt='%(asctime)s %(levelname)s %(name)s %(message)s'
)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

# --- FastAPI Application Initialization ---
app = FastAPI(
    title="Are You Drunk Yet API",
    description="An API to calculate alcohol levels.",
    version="1.0.0"
)

# --- Add CORS Middleware for Local Development ---
# This allows the frontend (running on localhost:5001) to communicate with the backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:5001"],  # Allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# --- Prometheus Metrics Integration ---
Instrumentator().instrument(app).expose(app)
logger.info("Metrics exposed at /metrics endpoint.")

# --- Pydantic Data Models ---
class CalculationRequest(BaseModel):
    weight: float = Field(..., gt=0)
    gender: str
    current_drinks: int = Field(..., ge=0)

# --- API Endpoint ---
@app.post("/api/calculate")
async def calculate_api(request: CalculationRequest):
    try:
        logger.info("Received calculation request", extra={'data': request.dict()})
        drinks_to_target = calculate_drinks_to_target_bac(
            request.weight, request.gender, request.current_drinks
        )
        time_to_sober = calculate_time_to_sober(
            request.current_drinks, request.weight, request.gender
        )
        response_data = {
            'drinks_to_reach_target': drinks_to_target,
            'time_to_sober': time_to_sober
        }
        logger.info("Calculation successful", extra={'result': response_data})
        return response_data
    except Exception as e:
        logger.error("An error occurred during calculation", exc_info=True)
        return {"error": "An internal server error occurred."}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
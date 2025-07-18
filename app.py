import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from prometheus_fastapi_instrumentator import Instrumentator
from pythonjsonlogger import jsonlogger
from calculator import calculate_drinks_to_target_bac, calculate_time_to_sober

# --- Structured Logging Setup ---
# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Use a JSON formatter for structured logs
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    fmt='%(asctime)s %(levelname)s %(name)s %(message)s'
)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

# --- FastAPI Application Initialization ---
app = FastAPI(
    title="Are You Drunk Yet API",
    description="An API to calculate alcohol levels, now with more performance and observability!",
    version="1.0.0"
)

# --- Prometheus Metrics Integration ---
# Instrument and expose a /metrics endpoint
Instrumentator().instrument(app).expose(app)
logger.info("Metrics exposed at /metrics endpoint.")

# --- Static Files and Templates ---
# Mount the 'static' directory to serve CSS, JS, etc.
app.mount("/static", StaticFiles(directory="static"), name="static")
# Initialize Jinja2 for HTML templates
templates = Jinja2Templates(directory="templates")

# --- Pydantic Data Models for Request Validation ---
class CalculationRequest(BaseModel):
    weight: float = Field(..., gt=0, description="Weight in kg, must be positive")
    gender: str
    current_drinks: int = Field(..., ge=0, description="Number of current drinks, cannot be negative")

# --- API Endpoints ---
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serves the main index.html page."""
    logger.info("Serving index page", extra={'client_host': request.client.host})
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/calculate")
async def calculate_api(request: CalculationRequest):
    """
    Calculates the number of drinks to reach a target BAC and the time to sober up.
    """
    try:
        logger.info(
            "Received calculation request",
            extra={
                'weight': request.weight,
                'gender': request.gender,
                'current_drinks': request.current_drinks
            }
        )

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
        # In a real app, you might have more specific error handling
        # and return appropriate HTTP status codes.
        return {"error": "An internal server error occurred."}

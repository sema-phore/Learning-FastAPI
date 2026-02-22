from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.api import routes_auth, routes_predict
from app.middleware.logging_middleware import LoggingMiddleware
from app.core.exceptions import register_exception_handlers
from app.core.config import settings
from app.db.database import init_db

app = FastAPI(title="Car Price Prediction API")

# Initialise SQLite DB on startup
@app.on_event("startup")
def on_startup():
    init_db()

# Middleware
app.add_middleware(LoggingMiddleware)

# Routes
app.include_router(routes_auth.router, tags=["Authorization"])
app.include_router(routes_predict.router, tags=["Prediction"])

# Monitoring
if settings.ENV != "test":
    Instrumentator().instrument(app).expose(app)

# Exception handlers
register_exception_handlers(app)
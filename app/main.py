from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.api import routes_auth, routes_predict
from app.middleware.logging_middleware import LoggingMiddleware
from app.core.exceptions import register_exception_handlers
from app.core.config import settings


app = FastAPI(title='Car Price Prediction API') # Custom Title to app

# Link middleware
app.add_middleware(LoggingMiddleware)

# Link routes/ endpoints
app.include_router(routes_auth.router, tags=['Authorization'])
app.include_router(routes_predict.router, tags=['Prediction'])

# Monitoring using prometheus
if settings.ENV != 'test':
    Instrumentator().instrument(app).expose(app) # Metrix

# Custom Exception Handler
register_exception_handlers(app)

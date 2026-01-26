from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

def register_exception_handlers(app: FastAPI):
    # First access to app
    @app.add_exception_handler(Exception)
    # Then handle the exception 
    async def unhandeled_excp_handler(request: Request, excp: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'detail': str(excp)}
        )
    
"""
content={'detail': str(excp)}
- Exposes internal error details
- Can leak file paths, secrets, logic
- Helps attackers

So use:
cntent={"detail": "Internal Server Error"}
"""

"""
The nested function pattern is used to register exception handlers on a specific FastAPI application instance while keeping startup configuration clean and modular. And it can be scalable later.
"""
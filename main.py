import sys
import traceback

import uvicorn
from fastapi import FastAPI, Security, HTTPException, status
from fastapi.security import APIKeyHeader
from fastapi.openapi.utils import get_openapi

# Import Run config
import app.config.run_config as cfg

# Import router files
from app.core import Restaurant, Dish
from app.database.configuration import engine
# Import local files
from app.models import models


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

api_key_header = APIKeyHeader(name="Olla-API-Key")
api_keys = ["my_api_key"]

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Olla Api",
        description="Olla App",
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema


# DB Specific endpoints
app.include_router(Restaurant.router)
app.include_router(Dish.router)

def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in api_keys:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


if __name__ == '__main__':
    print(f"Starting Olla API --> {cfg.api['host']}:{cfg.api['port']}\n")

    try:
        uvicorn.run(
            "main:app",
            host=cfg.api['host'],
            port=cfg.api['port'],
            workers=int(cfg.api['workers']),
            log_level=cfg.api['log_level'],
            reload=bool(cfg.api['reload']),
            # debug=bool(cfg.api['debug'])   # Only for development
        )
    except KeyboardInterrupt:
        print("Stopping Olla API")
    except Exception as e:
        print(f"Start Failed\n{'#'*100}")
        traceback.print_exc(file=sys.stdout)
        print(e)
        print(f"Exiting\n{'#'*100}")
    print("\n\n")
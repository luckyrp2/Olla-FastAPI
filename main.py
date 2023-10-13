import sys
import traceback

import uvicorn
from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

# Import Run config
import app.config.run_config as cfg

# Import router files
from app.core import Restaurant
from app.database.configuration import engine
# Import local files
from app.models import models


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Nauclerus Logbook API",
        description="Aviation logbook API for all pilots.",
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema


# DB Specific endpoints
app.include_router(Restaurant.router)


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
            debug=bool(cfg.api['debug'])
        )
    except KeyboardInterrupt:
        print("Stopping Nauclerus API")
    except Exception as e:
        print(f"Start Failed\n{'#'*100}")
        traceback.print_exc(file=sys.stdout)
        print(e)
        print(f"Exiting\n{'#'*100}")
    print("\n\n")
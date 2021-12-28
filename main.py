from typing import Set
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api_v1.endpoints import common_endpoints, users_endpoints
from app.config.configurations import AppConfig
from app.settings.app_settings import Settings

# print(Settings.print())
# print(AppConfig.print())
TITLE = AppConfig.TITLE
VERSION = AppConfig.VERSION
DESCRIPTION = AppConfig.DESCRIPTION

HOST = AppConfig.HOST
PORT = AppConfig.PORT
RELOAD = AppConfig.RELOAD
DEBUG = AppConfig.DEBUG

tags_details = [
    {
        "name": "users",
        "description": "Contains endpoints related to user operations"
    },
    {
        "name": "common",
        "description": "Contains common endpoints, accessible to all"
    }
]

origins = Settings.get_cors_list()
app = FastAPI(title=TITLE, version=VERSION,
              description=DESCRIPTION, openapi_tags=tags_details)

app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(users_endpoints.router, prefix="")
app.include_router(common_endpoints.router, prefix="")


if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=RELOAD, debug=DEBUG)

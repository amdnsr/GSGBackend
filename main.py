from typing import Set
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api_v1.endpoints import common_endpoints, users_endpoints
from app.config.configurations import AppConfig
from app.settings.app_settings import Settings

title = AppConfig.title
version = AppConfig.version
description = AppConfig.description

host = AppConfig.host
port = AppConfig.port
reload = AppConfig.reload
debug = AppConfig.debug

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
app = FastAPI(title=title, version=version,
              description=description, openapi_tags=tags_details)

app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(users_endpoints.router, prefix="")
# app.include_router(common_endpoints.router, prefix="")


if __name__ == "__main__":
    uvicorn.run("main:app", host=host, port=port, reload=reload, debug=debug)

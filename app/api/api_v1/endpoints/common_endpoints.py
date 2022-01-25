from app.config.configurations import AppConfig
import os
from fastapi import Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi_utils.inferring_router import InferringRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates

from app.models.request_response_models import CreateAccountRequest, CreateAccountResponse, LoginRequest, LoginResponse, UserProfileResponse
from app.core import security
from app.utils.helpers import FlaskJinjaSession


router = InferringRouter(tags=["common"])
template_dir_path = os.path.join(AppConfig.app_root_dir, "templates")
templates = Jinja2Templates(directory=template_dir_path)


@router.get("/")
def get_home():
    return "Hello there! Welcome to GetSeatGo!"


@router.get("/about", response_class=HTMLResponse)
def get_about(request: Request):
    # I need to create a session class, as layout.html is expecting a session.user_id variable (this variable is available in flask, without needing to pass it to the template)

    return templates.TemplateResponse("about.html", {"request": request, "session": FlaskJinjaSession()})
    return "GetSeatGo is a bus ticket booking system!"

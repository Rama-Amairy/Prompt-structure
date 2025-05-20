import os
import sys


from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR


FILE_LOCATION = os.path.join(os.path.dirname(__file__), "hello.py")

# Add root dir and handle potential import errors
try:
    MAIN_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    sys.path.append(MAIN_DIR)

    from logs import log_error, log_info
    from helper import get_settings, Settings

except ImportError as import_err:
    raise ImportError(
        f"Import Error in: {FILE_LOCATION}, Error: {import_err}"
    ) from import_err


hello_route = APIRouter()


@hello_route.get("/hello")
async def hello(settings: Settings = Depends(get_settings)) -> JSONResponse:
    """
    Returns hello message with application settings.

    Args:
        settings: Application settings injected via FastAPI dependency

    Returns:
        JSONResponse: Either successful response with settings or fallback response
    """
    try:
        app_name = settings.APP_NAME
        app_version = settings.APP_VERSION  # Removed unnecessary tuple
        chatbot_name = settings.CHATBOT_NAME

        log_info("Successfully retrieved app settings")

        response_content = {
            "APP Name": app_name,
            "APP Version": app_version,
            "Chatbot Name": chatbot_name,
            "Prompt Version": "",
            "Message": "Hello from API",
        }

        return JSONResponse(
            content=response_content,
            status_code=HTTP_200_OK,
        )

    except (ValueError, TypeError) as value_error:
        log_error(f"Failed to get settings from env file: {value_error}")

        fallback_content = {
            "APP Name": "NULL",
            "APP Version": "0",
            "Chatbot Name": "NULL",
            "Prompt Version": "0",
            "Message": "Hello from API",
        }

        return JSONResponse(
            content=fallback_content,
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

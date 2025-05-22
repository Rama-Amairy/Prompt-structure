import os
import sys
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR


try:
    MAIN_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    sys.path.append(MAIN_DIR)
    from helper import Settings, get_settings
    from model import OpenRouterModel
    from logs import log_error, log_info
except ImportError as e:
    raise ImportError(f"error in importing {e}")

chat_route = APIRouter()


@chat_route.post("/chatting", response_class=JSONResponse)
async def chattnig(settings: Settings = Depends(get_settings)):
    pass

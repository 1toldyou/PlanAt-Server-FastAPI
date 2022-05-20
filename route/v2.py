# Builtin library
from typing import Optional, List
import sys
import json
from datetime import datetime
import time
import hashlib
import requests
import uuid

# Framework core library
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse, StreamingResponse
from fastapi import APIRouter, Header, File, Query
from fastapi.responses import JSONResponse

# Local file
from constant import AuthConfig
from util import random_content, json_body
import util.mongodb_data_api as DocumentDB

router = APIRouter()


@router.get("", tags=["V2"])
async def v2_endpoint():
    return JSONResponse(status_code=200, content={"status": "implementing"})


@router.post("/calendar/event/create", tags=["V2"])
async def v2_create_calendar_event():
    pass


@router.post("/calendar/event/edit", tags=["V2"])
async def v2_edit_calendar_event():
    pass


@router.get("/calendar/event/get", tags=["V2"])
async def v2_get_calendar_event():
    pass

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
from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse

# Local file
from util import random_content, json_body
import util.pymongo_wrapper as DocumentDB

router = APIRouter()


@router.post("/create", tags=["V2"])
async def v2_create_user(request: Request, user_profile: json_body.UserProfileObject, password: str = Header(None)):
    db_client = DocumentDB.get_client()
    person_id = random_content.generate_person_id()
    full_profile = {
        "structure_version": 7,
        "person_id": person_id,
        "metadata": {
            "uuid": str(uuid.uuid4()),
            "seed": str(random_content.get_int(16)),
            "registration_timestamp_int": str(int(datetime.now().timestamp()))
        },
        "naming": {
            "unique_name": user_profile.naming.unique_name,
            "display_name_partial": user_profile.naming.display_name_partial,
            "display_name_full": user_profile.naming.display_name_full,
            "localization": [],
            "historical_name": []
        },
        "picture": {
            "avatar": {
                "image_id": user_profile.picture.avatar.image_id,
                "image_url": user_profile.picture.avatar.image_url
            },
            "background": {
                "image_id": user_profile.picture.background.image_id,
                "image_url": user_profile.picture.background.image_url
            }
        },
        "about": {
            "short_description": user_profile.about.short_description,
            "full_description": user_profile.about.full_description,
            "company_name": user_profile.about.company_name,
            "job_title": user_profile.about.job_title
        },
        "status": {
            "current_status": user_profile.status.current_status,
            "until": {
                "text": user_profile.status.until.text,
                "timestamp_int": user_profile.status.until.timestamp_int,
                "timezone_name": user_profile.status.until.timezone_name,
                "timezone_offset": user_profile.status.until.timezone_offset
            },
            "default_status": user_profile.status.default_status
        },
        "contact_method_collection": {
            "email_primary": {
                "domain_name": user_profile.contact_method_collection.email_primary.domain_name,
                "full_address": user_profile.contact_method_collection.email_primary.full_address
            },
            "phone": {
                "country_code": user_profile.contact_method_collection.phone.country_code,
                "regular_number": user_profile.contact_method_collection.phone.regular_number
            },
            "physical_address": {
                "full_address": user_profile.contact_method_collection.physical_address.full_address,
                "street_address": user_profile.contact_method_collection.physical_address.street_address,
                "city": user_profile.contact_method_collection.physical_address.city,
                "province": user_profile.contact_method_collection.physical_address.province,
                "country": user_profile.contact_method_collection.physical_address.country,
                "continent": user_profile.contact_method_collection.physical_address.continent,
                "post_code": user_profile.contact_method_collection.physical_address.post_code
            },
            "github": {
                "user_name": "",
                "user_handle": ""
            },
            "twitter": {
                "user_name": user_profile.contact_method_collection.twitter.user_name,
                "user_handle": user_profile.contact_method_collection.twitter.user_handle,
                "user_id": user_profile.contact_method_collection.twitter.user_id
            }
        }
    }
    profile_insert_query = DocumentDB.insert_one(db_client=db_client, collection="User", document_body=full_profile)
    print(profile_insert_query.inserted_id)
    calendar_index_insert_query = DocumentDB.insert_one(db_client=db_client,
                                                        collection="CalendarEventIndex",
                                                        document_body={"structure_version": 1, "person_id": person_id, "event_id_list": []})
    print(calendar_index_insert_query.inserted_id)
    login_credential_insert_query = DocumentDB.insert_one(db_client=db_client,
                                                          collection="LoginV1",
                                                          document_body={
                                                              "structure_version": 1,
                                                              "person_id": person_id,
                                                              "password_hash": hashlib.sha512(password.encode("utf-8")).hexdigest(),
                                                              "password_length": len(password),
                                                          })
    print(login_credential_insert_query.inserted_id)
    return JSONResponse(status_code=200, content={"status": "created", "person_id": person_id, "password": password})


@router.post("/delete", tags=["V2"])
async def v2_delete_user(request: Request, name_and_password: json_body.UnsafeLoginBody):
    mongoSession = DocumentDB.get_client()
    credential_verify_query = DocumentDB.find_one(collection="LoginV1",
                                                  find_filter={"person_id": name_and_password.person_id},
                                                  db_client=mongoSession)
    print(credential_verify_query)
    # the hash string generated using hashlib is lowercase
    if hashlib.sha512(name_and_password.password.encode("utf-8")).hexdigest() != credential_verify_query["password_hash"]:
        return JSONResponse(status_code=403,
                            content={"status": "not found or not match",
                                     "person_id": name_and_password.person_id,
                                     "password": name_and_password.password})


@router.get("/profile", tags=["V2"])
async def v2_get_user_profile():
    pass


@router.post("/profile/name/display_name", tags=["V2"])
async def v2_update_user_profile_name_displayname():
    pass


@router.post("/profile/about/description", tags=["V2"])
async def v2_update_user_profile_about_description():
    pass


@router.post("/profile/status", tags=["V2"])
async def v2_update_user_profile_status():
    pass


@router.post("/profile/picture", tags=["V2"])
async def v2_update_user_profile_picture():
    pass

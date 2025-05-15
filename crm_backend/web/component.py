# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import numpy as np
import pandas as pd
from io import BytesIO
from fastapi import APIRouter, Depends, HTTPException, Request, File, UploadFile, Form
from fastapi.security import OAuth2PasswordBearer
# from fastapi.responses import RedirectResponse
from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload
from fastapi.responses import JSONResponse

from crm_backend.event import *
from crm_backend.const import *
from crm_backend.schema.operator import *
from crm_backend.schema.schema import *
from crm_backend.plugin.message import sender

router = APIRouter()

IoParse = {
        "xlsx": pd.read_excel,
        "xls": pd.read_excel,
        "csv": pd.read_csv
        }

# class UUIDEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, UUID):
#             return str(obj)
#         return super().default(obj)

# add token to header Authorization header (Bearer <token>)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="on_login")

# @async_lru_cache cause is not bound to a Session
async def get_current_user(token: str=Depends(oauth2_scheme)):
    async with async_ops as ctx:    
        # token to user_id / default is lazy loading
        req = select(Token).options(joinedload(Token.user)).where(Token.token == token)
        token_obj = await ctx.on_query_obj(req)
        # instance need to attach session
        return token_obj[0][0].user
    

@router.post("/on_sms")
# login module need sms which have not token
async def on_sms(requst: Request):
    data = await requst.json()

    verify_code = np.random.randint(100000, 999999)
    template_code = _Template.verify.value
    template_param = json.dumps({"code": verify_code})
    try:
        await sender.send_message(data["phone"], template_code, template_param)
        async with async_ops as ctx:
            data = {"phone": data["phone"], "verify_code": verify_code}
            await ctx.on_insert_obj(VerifyCode(**data))
        return {"status": 0, "data": ""}
    except Exception as e:
        return {"status": 1, "data": str(e)}
    

async def verify_code(phone: str, verify_code: str):
    async with async_ops as ctx:
        req = select(VerifyCode).where(VerifyCode.phone == phone)
        req = req.order_by(VerifyCode.created_at.desc()).limit(1)
        verify_obj = await ctx.on_query_obj(req)
        print("verify_obj ",verify_obj)
        return verify_obj[0][0].verify_code == verify_code


@router.post("/upload")
async def upload_file(files: list[UploadFile] = File(...), table: str=Form(...), user: User=Depends(get_current_user)):
    # form_data = await request.form()
    try:
        for file in files:
            # Form argument / query parameters direct add 
            proc_engine = IoParse[file.filename.split(".")[-1]]
            # Read the file content (as bytes)
            with BytesIO(await file.read()) as contents:
                df = proc_engine(contents)
                temp = df.T.to_dict()
                df.loc[:, "user_id"] = user.user_id
                data = df.T.to_dict()
                async with async_ops as ctx:
                    orm_cls = ctx._orm_map[table]
                    objs = [orm_cls(**v) for k, v in data.items()]
                    await ctx.on_insert_obj(objs)
                    return {"status": 0,"data": list(temp.values())}
    except Exception as e:
        return {"status": 1,  "data": str(e)}


@router.get("/api")
def api():
    return {"route": "component"}

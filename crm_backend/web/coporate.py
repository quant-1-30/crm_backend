#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import select, and_, or_, delete
from fastapi import APIRouter, Depends

from .component import get_current_user
from crm_backend.schema.operator import *
from crm_backend.schema.schema import *
from crm_backend.event import *

router = APIRouter()

@router.get("/detail")
async def on_detail(name: str):
    async with async_ops as ctx:
        # data = await request.json()
        req = select(CoporateInfo).where(CoporateInfo.name == name)
        rows = await ctx.on_query_obj(req)
        # data = [{"name": item[0].name,
        #          "price": item[0].price,
        #          "category": item[0].price}
        #          for item in rows]
        data = [row[0].model_to_dict() for row in rows]
        return {"status": 0, "data": data}

@router.get("/list")
async def on_query():
    async with async_ops as ctx:
        req = select(Coporate)
        rows = await ctx.on_query_obj(req)
        # records = [{"name": item[0].name,
        #          "contact": item[0].name,
        #          "phone": item[0].phone}
        #          for item in rows]
        records = [row[0].model_to_dict() for row in rows]
        return {"status": 0, "data": records}

@router.get("/delete")
async def on_delete(coporate_name: str, user: User=Depends(get_current_user)):
    async with async_ops as ctx:
        req = delete(CoporateInfo).where(CoporateInfo.coporate_name == coporate_name)
        try:
            await ctx.on_delete_obj(req)
            return {"status": 0}
        except Exception as e:
            return {"status": 1, "message": str(e)}

@router.get("/api")
def api():
    return {"route": "coporate"}

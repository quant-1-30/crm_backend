# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import APIRouter
from sqlalchemy import select, and_, update

from crm_backend.event import *
from crm_backend.const import *
from crm_backend.schema.operator import *
from crm_backend.schema.schema import *
from .component import verify_code
router = APIRouter()


@router.post("/on_register")
async def on_register(item: RegisterEvent):
    async with async_ops as ctx:
        data = item.model_dump()
        code = data.pop("verify_code")
        eq = await verify_code(item.phone, code)
        if not eq:
            return {"status": 1, "data": "verify code is incorrect"}
        try:
            refresh_user = await ctx.on_insert_obj(User(**data), return_obj=True)
            print("refresh_user ", refresh_user)
            # insert token
            await ctx.on_insert_obj(Token(user_id=refresh_user[0].user_id))
            return {"status": 0, "data": ''}
        except Exception as e:
             return {"status": 1, "data": str(e)}
        

@router.post("/on_reset")
async def on_reset(item: ResetEvent):
    async with async_ops as ctx:
        eq = await verify_code(item.phone, item.verify_code)
        if not eq:
            return {"status": 1, "data": "verify code is incorrect"}
        req = update(User).where(User.phone == item.phone).values(passwd=item.passwd)
        await ctx.on_update(req)
        return {"status": 0, "data": ''}


@router.post("/on_login")
async def on_login(item: LoginEvent):
    """
        query user info from db and build token to db
    """
    async with async_ops as ctx:
        req = select(User).where(and_(User.name == item.name, User.passwd == item.passwd))
        user = await ctx.on_query_obj(req)
        if user:
            req = select(Token).where(Token.user_id == str(user[0][0].user_id))
            resp = await ctx.on_query_obj(req)
            return {"status": 0, "data": 
                                       {"token": resp[0][0].token, "name": user[0][0].name}}
        else:
            return {"status": 1, "error": "Invalid user_id / password"}
            
            # raise HTTPException(
            #     status_code=status.HTTP_401_UNAUTHORIZED,
            #     detail="Invalid token",
            #     headers={"WWW-Authenticate": "Bearer"},
            # )
            # return RedirectResponse(url=f"/on_register")



@router.get("/api")
def api():
    return {"route": "home"}

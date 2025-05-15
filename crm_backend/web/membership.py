#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from sqlalchemy import select, and_, or_, update
from fastapi import APIRouter, Depends

from crm_backend.schema.operator import *
from crm_backend.schema.schema import *
from crm_backend.event import *
from crm_backend.const import *
from crm_backend.plugin.message import sender
from .component import get_current_user
from utils.dt_utility import parse_date_range
router = APIRouter()


@router.post("/on_register")
async def on_register(item: MemberShipEvent, user: User=Depends(get_current_user)):
    async with async_ops as ctx:
        data = item.model_dump()
        print("on_register data ", data)
        data["user_id"] = user.user_id
        try:
            _obj = await ctx.on_insert_obj(MemberShip(**data), return_obj=True)
            data = _obj[0].model_to_dict()
            return {"status": 0, "data": data}
        except Exception as e:
            return {"status": 1, "data": str(e)}
        

@router.post("/on_update")
async def on_update(event: UpdateEvent, user: User=Depends(get_current_user)):
    print("on_update event ", event)
    try:
        async with async_ops as ctx:
            upd = update(MemberShip).where(MemberShip.member_id == event.member_id).values(name=event.name, 
                                                                                           phone=event.phone, 
                                                                                           birth=event.birth)
            await ctx.on_update(upd)
            return {"status": 0, "data": ""}
    except Exception as e:
        return {"status": 1, "data": str(e)}


@router.post("/on_consume")
async def on_consume(event: MemberEvent, user: User=Depends(get_current_user)):
    async with async_ops as ctx:
        # membership 
        req = select(MemberShip).where(MemberShip.member_id == event.member_id)
        m_obj = await ctx.on_query_obj(req)
        print("m_obj ", m_obj[0][0])
        # update balance
        balance = m_obj[0][0].balance + int(event.charge) + int(event.discount) - int(event.consume)
        if balance < 0:
            return {"status": 1, "data": balance}

        upd = update(MemberShip).where(MemberShip.member_id == event.member_id).values(balance=balance)
        await ctx.on_update(upd)

        if event.charge:
            charge_dict = event.model_dump(exclude={"consume", "balance"})
            charge_dict["user_id"] = user.user_id
            charge_dict["name"] = m_obj[0][0].name
            charge_dict["operator"] = user.name
            await ctx.on_insert_obj([ChargeRecord(**charge_dict)])
        
        if event.consume:
            consume_dict = event.model_dump(exclude={"charge", "discount", "balance"})
            consume_dict["user_id"] = user.user_id
            consume_dict["name"] = m_obj[0][0].name
            consume_dict["operator"] = user.name
            await ctx.on_insert_obj([ConsumeRecord(**consume_dict)])

        try:
            # send message
            if event.charge:
                template_code = _Template.charge.value
                template_param = json.dumps({"name": m_obj[0][0].name, "charge": event.charge, "balance": balance})
                await sender.send_message(m_obj[0][0].phone, template_code, template_param)
                print("send charge message success")
            if event.consume:
                template_code = _Template.consume.value
                template_param = json.dumps({"name": m_obj[0][0].name, "consume": event.consume, "balance": balance})
                await sender.send_message(m_obj[0][0].phone, template_code, template_param) 
                print("send consume message success")
            return {"status": 0, "data": ""}
        except Exception as e:
            return {"status": 1, "data": str(e)}
        

@router.get("/charge_detail")
# async def on_charge_detail(event: ReqEvent=Depends()):
async def on_charge_detail(member_id: str="", 
                           startDate: str="", 
                           endDate: str="", 
                           user: str=Depends(get_current_user)):
    async with async_ops as ctx:
        if startDate and endDate:
            ranges = parse_date_range(startDate, endDate)
        else:
            ranges = [datetime.datetime(1990, 1, 1), datetime.datetime.now()]

        # charge record
        req = select(ChargeRecord).where(ChargeRecord.created_at.between(ranges[0], ranges[1]))
        req = req.where(ChargeRecord.member_id == member_id)

        # row_objs
        _obj = await ctx.on_query_obj(req)
        records = [row[0].model_to_dict() for row in _obj]
        return {"status": 0, "data": records}
    

@router.get('/consume_detail')
async def on_consume_detail(member_id: str="", 
                            startDate: str="", 
                            endDate: str="", 
                            user: str=Depends(get_current_user)):
    async with async_ops as ctx:
        if startDate and endDate:
            ranges = parse_date_range(startDate, endDate)
        else:
            ranges = [datetime.datetime(1990, 1, 1), datetime.datetime.now()]

        # consume record
        req = select(ConsumeRecord).where(ConsumeRecord.created_at.between(ranges[0], ranges[1]))
        req = req.where(ConsumeRecord.member_id == member_id)

        _obj = await ctx.on_query_obj(req)  
        records = [row[0].model_to_dict() for row in _obj]
        return {"status": 0, "data": records}


@router.get("/list")
async def on_query(user: str=Depends(get_current_user)):
    try:
        async with async_ops as ctx:
            req = select(MemberShip)
            # obj ---> row object
            data = await ctx.on_query_obj(req)
            records = [row[0].model_to_dict() for row in data]
            return {"status": 0, "data": records}
    except Exception as e:
        return {"status": 1, "data": str(e)}
    

@router.get("/api")
def api():
    return {"route": "membership"}

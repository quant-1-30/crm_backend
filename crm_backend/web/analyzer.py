#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from toolz import reduceby
from sqlalchemy import select, and_, or_
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, time

from schema.operator import *
from schema.schema import *
from event import *
from const import *
from .component import get_current_user
from utils.dt_utility import iso_unpack, parse_date_range

router = APIRouter()


@router.post("/stats")
async def on_stats(event: StatsEvent, user: str=Depends(get_current_user)):
    
    def on_reduce(acc, item):
        return acc + item['value']
    try:
        async with async_ops as ctx:
            # created_at datetime and need to end of seesion
            sdate, edate = parse_date_range(event.startDate, event.endDate)

            # 充值
            charge_req = select(ChargeRecord).where(
                ChargeRecord.created_at.between(sdate, edate))
            rows = await ctx.on_query_obj(charge_req)
            # 按频率分组
            data = [{"frequency": iso_unpack(row[0].created_at, event.frequency), "value": row[0].charge} for row in rows]
            charge_aggregated = reduceby(key="frequency", binop=on_reduce, seq=data, init=0)
            charge_aggregated = [{k: v} for k, v in charge_aggregated.items()]

            # 消费
            consume_req = select(ConsumeRecord).where(
                ConsumeRecord.created_at.between(sdate, edate))
            rows = await ctx.on_query_obj(consume_req)
            # 按频率分组
            data = [{"frequency": iso_unpack(row[0].created_at, event.frequency), "value": row[0].consume} for row in rows]
            # 聚合
            consume_aggregated = reduceby(key="frequency", binop=on_reduce, seq=data, init=0)
            consume_aggregated = [{k:v} for k,v in consume_aggregated.items()]

            return {"status": 0, "data": {
                            "charge": charge_aggregated, 
                            "consume": consume_aggregated}}
    except Exception as e:
        return {"status": 1, "data": str(e)}


@router.get("/api")
def api():
    return {"route": "analyzer"}

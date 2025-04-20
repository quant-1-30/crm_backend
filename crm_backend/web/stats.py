#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from toolz import reduceby
from sqlalchemy import select, and_, or_
from fastapi import APIRouter, Depends


from schema.operator import *
from schema.schema import *
from event import *
from const import *
from .component import get_current_user
from utils.dt_utility import ts2date, freq_iso

router = APIRouter()


@router.post("/aggregate")
async def on_aggregate(event: StatsEvent, user: str=Depends(get_current_user)):

    def sum_values(acc, item):
        return acc + item['value']

    async with async_ops as ctx:
        sdate= ts2date(event.start_date)
        edate= ts2date(event.end_date)
        # 充值
        charge_req = select(ChargeRecord.created_at, ChargeRecord.charge).where(ChargeRecord.created_at.between(sdate, edate))
        rows = await ctx.on_query_obj(charge_req)
        
        data = [{"freq": freq_iso(item[0].created_at), "charge": item[0].charge} for item in rows]

        charge_aggregated = reduceby(key="freq", binop=sum_values, seq=data, init=0)
        charge_aggregated = [{k: v} for k, v in charge_aggregated.items()]
        # 消费
        consume_req = select(ConsumeRecord.created_at, ConsumeRecord.consume).where(ConsumeRecord.created_at.between(sdate, edate))
        rows = await ctx.on_query_obj(consume_req)

        data = [{"freq": freq_iso(item[0].created_at), "consume": item[0].consume} for item in rows]

        consume_aggregated = reduceby(key="freq", binop=sum_values, seq=data, init=0)
        consume_aggregated = [{k:v} for k,v in consume_aggregated.items()]
        return {"success": 0, "data": {"charge": charge_aggregated, "consume": consume_aggregated}}


@router.get("/api")
def api():
    return {"route": "stats"}

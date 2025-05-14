#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from toolz import reduceby
from sqlalchemy import select, and_, or_, func
from fastapi import APIRouter, Depends


from schema.operator import *
from schema.schema import *
from event import *
from const import *
from .component import get_current_user
from utils.dt_utility import parse_date_range

router = APIRouter()


@router.get("/snapshot")
async def on_snapshot(user: str=Depends(get_current_user)):
    """
        totalMembers: 0,
        totalCompanies: 0,
        totalCharges: 0,
        totalBalance: 0,
    """
    try:
        async with async_ops as ctx:
            # 会员
            member_req = select(func.count(MemberShip.id))
            rows = await ctx.on_query_obj(member_req)
            total_members = rows[0][0]
            # 公司
            coporate_req = select(func.count(Coporate.id))
            rows = await ctx.on_query_obj(coporate_req)
            total_coporates = rows[0][0]
            # 充值
            charge_req = select(func.sum(ChargeRecord.charge))
            rows = await ctx.on_query_obj(charge_req)
            total_charges = rows[0][0]
            # 余额
            balance_req = select(func.sum(MemberShip.balance))
            rows = await ctx.on_query_obj(balance_req)
            total_balance = rows[0][0]
            
            data = {
                "totalMembers": total_members, 
                "totalCompanies": total_coporates, 
                "totalCharges": total_charges, 
                "totalBalance": total_balance
            }
            return {"status": 0, "data": data}
    except Exception as e:
            return {"status": 1, "data": str(e)}


@router.get("/activity")
async def on_activity(startDate: str="", endDate: str="", user: str=Depends(get_current_user)):
    """
        {
          title: '会员',
          dataIndex: 'name',
          key: 'name',
        },
        {
          title: '充值',
          dataIndex: 'charge',
          key: 'charge',
        },
        {
          title: '操作员',
          dataIndex: 'operator',
          key: 'operator',
        },
        {
          title: '时间',
          dataIndex: 'created_at',
          key: 'created_at',
        },
    """
    # print("on_activity", startDate, endDate)
    if startDate and endDate:
        ranges = parse_date_range(startDate, endDate)
    else:
        # latest 7 days
        ranges = [datetime.datetime.now() - datetime.timedelta(days=7), datetime.datetime.now()]

    print("on_activity", ranges)

    try:
        async with async_ops as ctx:
            charge_req = select(ChargeRecord).where(ChargeRecord.created_at.between(ranges[0], ranges[1]))
            rows = await ctx.on_query_obj(charge_req)
            data = [row[0].model_to_dict() for row in rows]
            return {"status": 0, "data": data}
    except Exception as e:
        return {"status": 1, "data": str(e)}


@router.get("/api")
def api():
    return {"route": "dashboard"}

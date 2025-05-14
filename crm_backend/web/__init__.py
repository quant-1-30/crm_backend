# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from toolz import valfilter
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import select
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from schema.schema import Categorical
from schema.operator import *
from schema.schema import *
from plugin.message import sender
from utils.dt_utility import str2date
from const import *
from .home import router as login_router
from .membership import router as membership_router
from .coporate import router as coporate_router
from .component import router as component_router
from .analyzer import router as analyzer_router
from .dashboard import router as dashboard_router
# from .ws import router as ws_router


# 创建 APScheduler
scheduler = AsyncIOScheduler()

# 定义任务
async def scheduled_task():
    now = datetime.datetime.now()
    # get membership birthday
    async with async_ops as ctx:
        req = select(MemberShip)
        objs = await ctx.on_query_obj(req)
        members_birth = {"_".join([obj.member_name, obj.member_phone]): str2date(obj.birth_date) for obj in objs}
        on_birth = valfilter(lambda x: x.month == now.month and x.day == now.day, members_birth)

        for name_phone, birthday in on_birth.items():
            name, phone = name_phone.split("_")
            params = json.dumps({"name": name})
            await sender.send_message(phone, _Template.birthday.value, params)
            print(f"{birthday}今天是{name}的生日")


async def on_prepare():
    # customers = [Customer(name=item) for item in _Customer]
    categories = [Categorical(name=item) for item in _Categorical]
    try:
        # await async_ops.on_insert_obj(customers)
        await async_ops.on_insert_obj(categories)
    except Exception as e:
        print(f"Error: {e}")


async def on_startup():
    await on_prepare()
    # scheduler.add_job(scheduled_task, "interval", seconds=10)
    scheduler.add_job(scheduled_task, "cron", hour=9, minute=0, second=0)
    scheduler.start()


def on_shutdown():
    scheduler.shutdown()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Running before startup: Initializing resources...")
    await on_startup()
    # Perform setup tasks here (e.g., database connection, cache setup)
    yield  # App runs here
    on_shutdown()
    print("🛑 Running on shutdown: Cleaning up resources...")

# 创建 FastAPI 应用
# slash False return 404 not 307
app = FastAPI(lifespan=lifespan, redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    # when fronted is set cors , * is not allowed
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),     # 允许所有来源。可以是特定域名列表。 
    allow_credentials=True,
    allow_methods=os.getenv("CORS_METHODS", "*").split(","),    # 允许所有方法（如 GET、POST）。
    allow_headers=os.getenv("CORS_HEADERS", "*").split(","),    # 允许所有头。
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    # 在请求到达路由之前运行的代码
    print(f"Incoming request: {request.method} {request.url}")
    
    response = await call_next(request)  # 调用下一个中间件或路由处理函数

    # 在响应返回之前运行的代码
    print(f"Outgoing response status: {response.status_code}")
    return response


# 将 APIRouter 实例包含到主应用程序中
app.include_router(login_router, prefix="/home")
app.include_router(membership_router, prefix="/membership")
app.include_router(coporate_router, prefix="/coporate")
app.include_router(component_router, prefix="/component")
app.include_router(analyzer_router, prefix="/analyzer")
app.include_router(dashboard_router, prefix="/dashboard")
# app.include_router(ws_router, prefix="/ws")

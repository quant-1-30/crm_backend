#! /usr/bin/env python3

# import datetime
from typing import Union
from datetime import datetime, time

def str2date(date: Union[int, str], fmt: str="%Y%m%d"):
    struct_dt = datetime.strptime(str(date), fmt)
    return struct_dt


def iso_unpack(date: datetime, freq: str):
    if freq == "day":
        return date.strftime("%Y%m%d")
    elif freq == "week":
        return date.isocalendar()[1]
    else:
        return date.isocalendar()[0]


def parse_date_range(start_date: str, end_date: str, fmt="%Y-%m-%d") -> tuple[datetime, datetime]   :
    """解析日期范围并设置时间边界"""
    start = datetime.strptime(start_date, fmt)
    end = datetime.strptime(end_date, fmt)
        
    # 设置开始时间为当天的开始 (00:00:00)
    start = datetime.combine(start.date(), time.min)
    # 设置结束时间为当天的结束 (23:59:59.999999)
    end = datetime.combine(end.date(), time.max) 
    return start, end
#! /usr/bin/env python3

import datetime
from typing import Union

def int2date(date: Union[int, str], fmt: str="%Y%m%d"):
    struct_dt = datetime.datetime.strptime(str(date), fmt)
    return struct_dt

def ts2date(ts: int):
    date = datetime.datetime.fromtimestamp(ts)
    return date

def freq_iso(freq, date):
    if freq == "day":
        return date.strftime("%Y%m%d")
    elif freq == "week":
        return date.isocalendar()[1]
    else:
        return date.isocalendar()[0]
    
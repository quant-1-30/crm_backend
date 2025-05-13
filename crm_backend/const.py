#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import enum


# class _Customer(enum.Enum):
# # class CustomerEnum(int, Enum):
#     member = "membership"
#     coporate = "coporate"


class _Categorical(enum.Enum):
# class CategoricalEnum(str, Enum):

    standard = "标大"
    lexuary = "豪大"
    business = "商大"
    standard_dual = "标双"
    lexuary_dual = "豪双"
    business_dual = "商双"
    suite = "套房"


class _Template(enum.Enum):

    verify = "SMS_314795532"
    charge = "SMS_480490015"
    consume = "SMS_480470024"
    birthday = "SMS_480440021"



ProxyMapping = {
    "协议单位": "coporate",
    "协议单位价格": "coporate_info",
}


__all__ = ["_Categorical", "_Template", "ProxyMapping"]


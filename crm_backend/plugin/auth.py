#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import jwt
import datetime


def generate_token(user_id: str):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    return jwt.encode(payload, "secret", algorithm="HS256")


def verify_token(token: str):
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

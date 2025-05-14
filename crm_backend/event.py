#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import re
from pydantic import BaseModel, field_validator, Field


class RegisterEvent(BaseModel):

    name: str
    phone: int
    passwd: str
    verify_code: str

    @field_validator("phone", mode="before")
    def validate_phone(cls, value):
        pattern = r"^1[3-9]\d{9}$"
        if not re.match(pattern, str(value)):
            raise ValueError("phone must be a valid phone number")
        return value
    
    @field_validator("verify_code", mode="before")
    def validate_verify_code(cls, value):
        pattern = r"^\d{6}$"
        if not re.match(pattern, str(value)):
            raise ValueError("verify code must be 6 digits")
        return value

    # class Config:
    #     date_encoders = {
    #         datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
    #     }

    # @field_serializer("timestamp")
    # def serialize_timestamp(self, timestamp: datetime) -> str:
    #     return timestamp.strftime('%Y-%m-%d %H:%M:%S')

class UpdateEvent(BaseModel):

    member_id: str
    name: str
    phone: int
    birth: int


class LoginEvent(BaseModel):
     
     name: str
     passwd: str


class ResetEvent(BaseModel):

     passwd: str
     phone: int
     verify_code: str

class MemberShipEvent(BaseModel):

    name: str
    phone: int
    birth: int
    balance: int = Field(default=0)

class MemberEvent(BaseModel):

    member_id: str
    charge: int
    discount: int
    consume: int


class CoporateEvent(BaseModel):

    name: str
    contact: str
    phone: int


class StatsEvent(BaseModel):

    startDate: str
    endDate: str
    frequency: str


class ReqEvent(BaseModel):

    start_dt: int=Field(default=19900101, description="start of range")
    end_dt: int=Field(default=20500101, description="end of range")
    member_id: str = Field(default="", description="member id")


class RespEvent(BaseModel):
     
     status: int
     error: str


__all__ = ["LoginEvent", "RegisterEvent", "ResetEvent", "MemberShipEvent", "MemberEvent", "StatsEvent", "ReqEvent", "RespEvent", "UpdateEvent"]

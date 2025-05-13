#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import inspect
import datetime
import uuid
from typing import Optional, List

from sqlalchemy import Integer, String, ForeignKey, BigInteger, Text, UUID, LargeBinary, Sequence, Column, DateTime, func, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.inspection import inspect

from const import _Categorical


# declarative base class
class Base(DeclarativeBase):
   
    # __abstract__ = True
    # similar to auto_increment
    # primary = unique + not null
    # 没有主键, orm 自动创建id
    # PrimaryKeyConstraint / primary_key=True
    # id_sequence = Sequence('user_id_seq', start=1000, increment=5)
    
    def model_to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class User(Base):

    # backref在主类里面申明 / back_populates显式两个类申明
    # default lazy="select" / "joined" / "selectin" 
    # one to many all, delete-orphan / many to many  all, delete 
    # uselist False -对一
    # #association table 多对多关系

    __tablename__ = "user_info"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, use_existing_column=True)
    phone: Mapped[int] = mapped_column(BigInteger, unique=True)
    passwd: Mapped[str] = mapped_column(String(30), use_existing_column=True)
    # as_uuid=True uuid object / False  str
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    # user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), unique=True, default=lambda: str(uuid.uuid4))

    __table_args__ = (
        PrimaryKeyConstraint("id", "user_id", "phone", name="pk_id_user_phone"),
        # {"extend_existing": True}
    )
    
    # verify_code: Mapped["VerifyCode"] = relationship(
    #     back_populates="user", cascade="all, delete-orphan")

    token: Mapped["Token"] = relationship(
        back_populates="user", cascade="all, delete-orphan")
    
    membership: Mapped["MemberShip"] = relationship(
        # save_update default
        back_populates="user")
    
    charge_records: Mapped[List["ChargeRecord"]] = relationship(
        back_populates="user")
    
    consume_records: Mapped[List["ConsumeRecord"]] = relationship(
        back_populates="user")    
    
    coporates: Mapped[List["Coporate"]] = relationship(
        back_populates="user"
    )
    
    templates: Mapped[List["Template"]] = relationship(
        back_populates="user")


class VerifyCode(Base):

    __tablename__ = "verify_code"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # phone: Mapped[int] = mapped_column(ForeignKey("user_info.phone", onupdate="CASCADE"))
    phone: Mapped[int] = mapped_column(BigInteger, nullable=False)
    # DateTime(timezone=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(), use_existing_column=True)
    verify_code: Mapped[str] = mapped_column(String(30), use_existing_column=True)
    # user: Mapped["User"] = relationship(back_populates="verify_code") 


class Token(Base):

    __tablename__ = "token"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True)
    token: Mapped[str] = mapped_column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    user_id: Mapped[str] = mapped_column(ForeignKey("user_info.user_id", ondelete="CASCADE"))

    __table_args__ = (
        PrimaryKeyConstraint("id", "user_id", name="pk_id_user"),
        # {"extend_existing": True}
    )

    user: Mapped["User"] = relationship(back_populates="token")

    def __repr__(self) -> str:
        return f"Token(id={self.id!r}, token={self.token!r})"


# class Customer(Base):

#     __tablename__ = "customer"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     # reserved name="type" / key
#     # native_enum=True means enum in database name / False means enum in python value
#     # default save enum name
#     # name = Column(Enum(_Customer, native_enum=True), nullable=False, unique=True)
#     # enum value must be string
#     name = Column(Enum(_Customer, values_callable=lambda x: [i.value for i in x]), nullable=False, unique=True)


class MemberShip(Base):

    __tablename__ = "membership"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True)
    member_id: Mapped[str] = mapped_column(UUID(as_uuid=True), unique=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(30), use_existing_column=True)
    phone: Mapped[BigInteger] = mapped_column(BigInteger, unique=True)
    birth: Mapped[BigInteger] = mapped_column(BigInteger, default=0, use_existing_column=True)
    balance: Mapped[int] = mapped_column(Integer, default=0, use_existing_column=True)
    # 计算默认值用server_default --- dababase 非default --- python
    # 默认日期 func.now / func.current_timestamp()
    register_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(), use_existing_column=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_info.user_id", onupdate="CASCADE"))

    __table_args__ = (
        PrimaryKeyConstraint("id", "name", "phone", name="pd_id_member_name_phone"),
    )

    user: Mapped["User"] = relationship(
        back_populates="membership")

    charge_records: Mapped[List["ChargeRecord"]] = relationship(
        back_populates="membership", cascade="all, delete-orphan"
    )

    consume_records: Mapped[List["ConsumeRecord"]] = relationship(
        back_populates="membership", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"MemberShip(id={self.id!r}, name={self.name!r}, phone={self.phone!r}, user_id={self.user_id!r}, member_id={self.member_id!r}, register_time={self.register_time!r})"


class ChargeRecord(Base):

    __tablename__ = "charge_record"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("membership.member_id", ondelete="CASCADE"))
    charge: Mapped[int] = mapped_column(Integer, nullable=False)
    discount: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(), use_existing_column=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_info.user_id"))
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    operator: Mapped[str] = mapped_column(String(30), nullable=False)

    # __table_args__ = (
    #     PrimaryKeyConstraint("id", name="pk_id"),
    #     # {"extend_existing": True}
    # )

    user: Mapped["User"] = relationship(
        back_populates="charge_records")
    
    membership: Mapped["MemberShip"] = relationship(
        back_populates="charge_records")
    

class ConsumeRecord(Base):

    __tablename__ = "consume_record"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("membership.member_id"))
    consume: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(), use_existing_column=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_info.user_id"))
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    operator: Mapped[str] = mapped_column(String(30), nullable=False)
    
    # __table_args__ = (
    #     PrimaryKeyConstraint("id", name="pk_id"),
    #     # {"extend_existing": True}
    # )

    user: Mapped["User"] = relationship(
        back_populates="consume_records")
    
    membership: Mapped["MemberShip"] = relationship(
        back_populates="consume_records")


class Coporate(Base):

    __tablename__ = "coporate"
    
    id: Mapped[int] = mapped_column(Integer, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    contact: Mapped[str] = mapped_column(String(30), nullable=True)
    phone: Mapped[BigInteger] = mapped_column(BigInteger, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_info.user_id"))

    __table_args__ = (
        PrimaryKeyConstraint("id", "name", name="pd_id_name_coporate"),
    )

    user: Mapped["User"] = relationship(
        back_populates="coporates"
    )
    
    coporate_info: Mapped[List["CoporateInfo"]] = relationship(
        back_populates="coporate", cascade="all, delete-orphan"
    )


class Categorical(Base):

    __tablename__ = "categorical"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # default save enum name
    # name = Column(Enum(_Categorical, name='_Categorical_enum', native_enum=True), unique=True)
    name = Column(Enum(_Categorical, values_callable=lambda x: [e.value for e in x], name='_Categorical_enum'), unique=True)


class CoporateInfo(Base):

    __tablename__ = "coporate_info"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(ForeignKey("coporate.name"), use_existing_column=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[str] = mapped_column(ForeignKey("categorical.name"), use_existing_column=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_info.user_id"))

    coporate: Mapped["Coporate"] = relationship(
        back_populates="coporate_info")

    def __repr__(self) -> str:
        return f"CoprateInfo(id={self.id!r}, name={self.name!r}, price={self.price!r}, category={self.category!r})"


class Template(Base):

    __tablename__ = "template"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_info.user_id"))

    __table_args__ = (
        # name is unique
        PrimaryKeyConstraint("id", "name", name="pd_id_name"),
    )
    
    user: Mapped["User"] = relationship(
        back_populates="templates")
    
"""
This file contains table assets
"""

from sqlalchemy import Column, Float, BIGINT

from .base import BaseModel


class Currency(BaseModel):
    __tablename__ = "currency"

    adm_id = Column(BIGINT, primary_key=True)
    yuan = Column(Float)



from datetime import datetime
from typing import TYPE_CHECKING

from app.models.device import Device
from sqlalchemy import Boolean, Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class FirebaseToken(Base):
    # __tablename__ = 'firebase_token'
    id = Column(Integer, primary_key=True, index=True)
    value = Column(String(), nullable=False)
    created = Column(DateTime(), nullable=True, default=datetime.utcnow)

    device_id = Column(Integer(), ForeignKey(Device.id), nullable=False)

    device = relationship(Device, back_populates='firebase_tokens')

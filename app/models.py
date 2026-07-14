from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from app.database import Base

class NetworkDevice(Base):

    __tablename__ = "network_devices"

    id = Column(
        Integer,
        primary_key = True,
        index = True
    )

    name = Column(
        String,
        nullable = False
    )

    ip = Column(
        String,
        unique = True,
        nullable = False
    )

class PingHistory(Base):

    __tablename__ = "ping_history"

    id = Column(
        Integer,
        primary_key = True,
        index = True
    )

    device_id = Column(
        Integer
    )

    status = Column(
        String
    )

    response_time = Column(
        Float,
        nullable = True
    )

    timestamp = Column(
        DateTime,
        default = datetime.utcnow
    )
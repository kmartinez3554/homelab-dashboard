from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import NetworkDevice, PingHistory

def get_or_create_device(db: Session, name: str, ip: str) -> NetworkDevice:
    
    device = db.query(NetworkDevice).filter(
        NetworkDevice.ip == ip
    ).first()

    if device is None:
        device = NetworkDevice(
            name = name,
            ip = ip
        )

        db.add(device)
        db.commit()
        db.refresh(device)

    return device

def save_ping_result(
    db : Session,
    device_id: int,
    status: str,
    response_time: float | None
):
    history = PingHistory(
        device_id = device_id,
        status = status,
        response_time = response_time
    )

    db.add(history)
    db.commit()

def get_average_response_time(db: Session, device_id: int):
    return(
        db.query(func.avg(PingHistory.response_time))
        .filter(
            PingHistory.device_id == device_id,
            PingHistory.status == "online"
        )
        .scalar()
    )

def get_total_checks(db: Session, device_id: int):
    return(
        db.query(PingHistory)
        .filter(
            PingHistory.device_id == device_id)
        .count()
    )

def get_failed_checks(db: Session, device_id: int):
    return(
        db.query(PingHistory)
        .filter(
            PingHistory.device_id == device_id,
            PingHistory.status == "offline"
        )
        .count()
    )

def calculate_uptime(db: Session, device_id: int):

    total = get_total_checks(db, device_id)

    if total == 0:
        return 100.0

    failed = get_failed_checks(db, device_id)

    return round(((total - failed) / total) * 100, 2)

def get_ping_history(db: Session, device_id: int, limit: int = 50):

    return(
        db.query(PingHistory)
        .filter(
            PingHistory.device_id == device_id
        )
        .order_by(
            PingHistory.timestamp.desc()
        )
        .limit(limit)
        .all()
    )
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import NetworkDevice, PingHistory

from app.services.network import check_device
from app.config import NETWORK_DEVICES

from app.repositories.network_repository import(
    get_or_create_device,
    save_ping_result,
    get_average_response_time,
    get_total_checks,
    get_failed_checks,
    calculate_uptime
)

router = APIRouter()

@router.get("/network")
def network_status(
    db: Session = Depends(get_db)
):

    results = []

    for device in NETWORK_DEVICES:

        status = check_device(device["ip"])

        device_record = get_or_create_device(
            db,
            device["name"],
            device["ip"]
        )

        save_ping_result(
            db,
            device_record.id,
            status["status"],
            status["response_time"]
        )

        results.append({
            "name": device["name"],
            **status
        })

    return results

@router.get("/network/stats")
def network_stats(
    db: Session = Depends(get_db)
):
    stats = []

    devices = db.query(NetworkDevice).all()

    for device in devices:

        stats.append({
            "name": device.name,
            "ip": device.ip,
            "uptime": calculate_uptime(db, device.id),
            "average_ping": get_average_response_time(db, device.id),
            "checks": get_total_checks(db, device.id),
            "failures": get_failed_checks(db, device.id),
        })

    return stats

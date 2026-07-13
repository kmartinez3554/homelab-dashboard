import psutil
import socket
import platform

def get_system_info():
    return{
        "hostname": socket.gethostname(),
        "operating_system": platform.system(),
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage":psutil.disk_usage("/").percent
    }
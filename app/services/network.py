import subprocess

def check_device(ip):

    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "2", ip],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )

        if result.returncode == 0:

            output = result.stdout.decode()

            time = None

            for line in output.split("\n"):
                if "time=" in line:
                    time = line.split("time=")[1].split(" ")[0]
                    break

            return{
                "ip": ip,
                "status": "online",
                "response_time": float(time) if time else None
            }
        
        else:
            return{
                "ip": ip,
                "status": "offline",
                "response_time": None
            }
    except Exception as e:
        return{
            "ip": ip,
            "status":"error",
            "repsonse_time": None,
            "error": str(e)
        }
from datetime import datetime

def fastmcp_get_datetime(input: dict = {}) -> dict:
    now = datetime.now()
    return {
        "tool_name": "fastmcp_get_datetime",
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%I:%M:%S %p")
    }

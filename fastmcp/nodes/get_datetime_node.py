from tools.datetime_tool import fastmcp_get_datetime

def get_datetime_node(state: dict) -> dict:
    result = fastmcp_get_datetime()
    return {**state, **result}

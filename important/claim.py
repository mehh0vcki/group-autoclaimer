from time import time
from important.switch import account_switch
from aiosonic import HTTPClient, HttpResponse

# NOTE: i hate this file, and i wish to never see it ever again

async def handle_response(response: HttpResponse):
    data: list = {}

    data["status_code"] = response.status_code
    data["json"] = await response.json()
    
    return data

async def claim_group(group_id: int, headers: dict) -> dict:
    client: HTTPClient = HTTPClient()

    start_time: float = time()

    join_request: HttpResponse = await client.post(f"https://groups.roblox.com/v1/groups/{group_id}/users", headers=headers)
    claim_request: HttpResponse = await client.post(f"https://groups.roblox.com/v1/groups/{group_id}/claim-ownership", headers=headers)

    end_time: float = time()

    data: list = {}
    data["join"] = await handle_response(join_request)
    data["claim"] = await handle_response(claim_request)
    data["time"] = end_time - start_time

    return data

async def leave_group(group_id: int, user_id: int, headers: dict) -> dict:
    client: HTTPClient = HTTPClient()

    start_time: float = time()

    leave_request: HttpResponse = await client.delete(f"https://groups.roblox.com/v1/groups/{group_id}/users/{user_id}", headers=headers)

    end_time: float = time()

    data: list = {}
    data["leave"] = await handle_response(leave_request)
    data["time"] = end_time - start_time

    return data

async def shout_group(group_id: int, message: str, headers: dict) -> dict:
    client: HTTPClient = HTTPClient()
    json: dict = {"message": message}

    start_time: float = time()

    shout_rqeuest: HttpResponse = await client.patch(f"https://groups.roblox.com/v1/groups/{group_id}/status", json=json, headers=headers)

    end_time: float = time()

    data: list = {}
    data["shout"] = await handle_response(shout_rqeuest)
    data["time"] = end_time - start_time

    return data
import aiosonic
import json

async def check_user(user_id: int) -> int:
    owned_groups = []

    async with aiosonic.HTTPClient() as client:
        response = await client.get(f"https://groups.roblox.com/v2/users/{user_id}/groups/roles?includeLocked=false")

        if response.status_code == 200:
            data = await response.json()
            owned_groups = [group["group"]["id"] for group in data["data"] if group["role"]["rank"] == 255]
            not_owned_groups = [group["group"]["id"] for group in data["data"] if group["role"]["rank"] != 255]

            return len(owned_groups), not_owned_groups
        else:
            error_message = f"Couldn't get the number of groups owned. {response.status_code} / {await response.json()}"
            return error_message

async def send_webhook(json_data: dict) -> None:
    with open("files/settings.json", "r") as file:
        data = json.load(file)

    async with aiosonic.HTTPClient() as client:
        for webhook in data["webhooks"]:
            await client.post(webhook, json=json_data)
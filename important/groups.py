from important.request import send_webhook
from format import generate_text
from datetime import datetime
import aiosonic, discord, json as json_lib

async def check_group(group_id: int, time: float, headers: dict, bot: discord.Client) -> None:
    client = aiosonic.HTTPClient()
    today = datetime.now().strftime("%Y-%m-%d")

    funds_request = await client.get(f"https://economy.roblox.com/v1/groups/{group_id}/currency", headers=headers)
    pending_request = await client.get(f"https://economy.roblox.com/v1/groups/{group_id}/revenue/summary/{today}", headers=headers)
    members_request = await client.get(f"https://groups.roblox.com/v1/groups/{group_id}", headers=headers) # why not
    clothing_request = await client.get(f"https://catalog.roblox.com/v1/search/items/details?Category=3&SortType=Relevance&CreatorTargetId={group_id}&ResultsPerPage=100&CreatorType=2", headers=headers)
    
    funds = pending = members = clothing = 0

    if funds_request.status_code == 200:
        json = await funds_request.json()

        if json.get("robux"): funds = json["robux"]
        else: funds = 0
    
    if pending_request.status_code == 200:
        json = await pending_request.json()

        if json.get("pendingRobux"): pending = json["pendingRobux"]
        else: pending = 0
    
    if members_request.status_code == 200:
        json = await members_request.json()

        if json.get("memberCount"): members = json["memberCount"]
        else: members = 0

    if clothing_request.status_code == 200:
        json = await clothing_request.json()

        clothing = 0
        while True:
            next_cursor: str = json["nextPageCursor"]
            clothing += len(json['data'])

            if next_cursor == None:
                break

            url = f"https://catalog.roblox.com/v1/search/items/details?Category=3&SortType=Relevance&CreatorTargetId={group_id}&ResultsPerPage=100&CreatorType=2&Cursor={next_cursor}"
            clothing_request = await client.get(url, headers=headers)
            json = await clothing_request.json()
    
    json: dict = {
        "embeds": [
            {
                "author": {
                    "icon_url": "https://tr.rbxcdn.com/f68f1cd8d17e887da5196f9225ec6529/150/150/Image/Png",
                    "name": "mehhovcki™"
                },
                "title": "group was succesfully autoclaimed",
                "fields": [
                    {
                        "name": "robux",
                        "value": f"{funds}",
                        "inline": True
                    },
                    {
                        "name": "pending",
                        "value": f"{pending}",
                        "inline": True
                    },
                    {
                        "name": "clothing",
                        "value": f"{clothing}",
                        "inline": True
                    },
                    {
                        "name": "members",
                        "value": f"{members}",
                        "inline": True
                    }
                ],
                "description": f"**{group_id}** group was succesfully autoclaimed in **{round(time, 4)} seconds**. [group link](https://roblox.com/groups/{group_id}/i-like-big-cocks)",
                "thumbnail": {
                    "url": "https://i.ibb.co/1T5V3Fy/Png-2.png"
                },
                "footer": {
                    "text": "furry autoclaimer rewrited™",
                    "icon_url": "https://i.ibb.co/z7spQ2t/furry.png"
                },
                "color": 10640584
            }
        ]
    }

    with open("files/settings.json", "r") as file:
        data = json_lib.load(file)

    mode = data["requirements"]["mode"]
    funds_req = data["requirements"]["funds"]
    pending_req = data["requirements"]["pending"]
    members_req = data["requirements"]["members"]
    clothing_req = data["requirements"]["clothing"]

    if mode in [">", ">=", "<", "<="]:
        if (mode == ">" and (funds > funds_req or pending > pending_req or members > members_req or clothing > clothing_req)) or \
        (mode == ">=" and (funds >= funds_req or pending >= pending_req or members >= members_req or clothing >= clothing_req)) or \
        (mode == "<" and (funds < funds_req or pending < pending_req or members < members_req or clothing < clothing_req)) or \
        (mode == "<=" and (funds <= funds_req or pending <= pending_req or members <= members_req or clothing <= clothing_req)):
            json["content"] = f"{bot.user.mention}, epic group right here"
    else:
        generate_text("unknown mode!! Detection mode should be one of these: >, >=, <, <=. Choosing default mode", 3)
        if funds >= funds_req or pending >= pending_req or members >= members_req or clothing >= clothing_req:
            json["content"] = f"{bot.user.mention}, epic group right here"
    
    await send_webhook(json)
    return None

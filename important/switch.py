import asyncio, json
from format import generate_text
from important.request import send_webhook
from secrets import SystemRandom
from aiosonic import HTTPClient, HttpResponse, HttpHeaders

is_switching: bool = False

async def get_account_data(headers: dict) -> dict:
    client: HTTPClient = HTTPClient()
    data: dict = {}

    response: HttpResponse = await client.get("https://users.roblox.com/v1/users/authenticated", headers=headers)
    if response.status_code == 200:
        json: dict = await response.json()

        data["user_id"] = json["id"]
        data["username"] = json["name"]
        data["displayName"] = json["displayName"]

    return data

async def update_headers(cookie: str) -> list:
    client: HTTPClient = HTTPClient()

    headers: list = {
        "Cookie": f"GuestData=UserID=-1458690174; .ROBLOSECURITY={cookie}; RBXEventTrackerV2=CreateDate=11/19/2023 12:07:42 PM&rbxid=5189165742&browserid=200781876902;",
        "Content-Type": "application/json",
        "x-csrf-token": None,
        "User-Agent": "Mozilla/5.0 (Linux; Linux x86_64; en-US) AppleWebKit/533.41 (KHTML, like Gecko) Chrome/48.0.1076.318 Safari/533"
    }

    try:
        response: HttpResponse = await client.post("https://catalog.roblox.com//", headers=headers)
        response_headers: HttpHeaders = response.headers    
    except:
        return await update_headers(cookie)

    if response_headers.get("x-csrf-token") is not None:
        headers["x-csrf-token"] = response_headers.get("x-csrf-token")

    return headers

async def new_account() -> tuple[str, int, str, dict]:
    user_data = await account_switch()

    user_account: dict = user_data[0]
    headers: dict = await update_headers(user_data[1])

    username = user_account["username"]
    user_id = user_account["user_id"]
    cookie = user_data[1]
    headers = headers
    return username, user_id, cookie, headers

async def account_switch():
    global is_switching
    if is_switching:
        generate_text("Account switching function is already working, but still got runned by someone.", 3)
        return None

    is_switching = True

    
    from important.claim import claim_group, leave_group
    with open("files/cookies.txt", "r") as file:
        cookies: list = file.read().splitlines()
        random: SystemRandom = SystemRandom()
    
    with open("files/settings.json", "r") as file:
        data = json.load(file)

    if len(cookies) == 0:
        await send_webhook({"content": f"amount cookies are 0!"})
        print("Amount of cookies are 0! Press Enter to exit programm...")
        input()
        exit(0)

    cookie: str = random.choice(cookies)
    generate_text("Trying to get account to work...", 1)
    headers: list = await update_headers(cookie)

    if headers.get("x-csrf-token") and headers["x-csrf-token"] != None:
        is_switching = False
        attempt: dict = await claim_group(1, headers)
        generate_text("Account valid! Checking for ratelimits!", 1)

        if data["debug"]["showAccountSwitchData"] == True: 
            if data["debug"]["enable"] == False:
                generate_text(str(attempt), 3)

        if attempt["join"]["status_code"] in [200, 409]:
            if attempt["claim"]["status_code"] == 403:
                account_data: dict = await get_account_data(headers)         
                generate_text("Finishing up! Getting user data...", 1)
                
                if account_data.get("user_id") != None:
                    generate_text(f"Everything is ready! Succesfully starting as {account_data['username']}", 1)
                    await leave_group(1, account_data["user_id"], headers)
                    await send_webhook({"content": f"{account_data['username']} ({account_data['user_id']}) has been choosed as claiming account."})
                    return account_data, cookie
            else:
                if attempt["claim"]["status_code"] == 429:
                    generate_text("Cookie have ratelimit on claim; trying again...", 1)
                else:
                    generate_text(f"Weird issue occured: {attempt['claim']['status_code']} / {attempt['claim']['json']}", 1)
        else:
            if attempt["join"]["status_code"] == 429:
                generate_text("Cookie have ratelimit on join; trying again...", 1)
            elif attempt['join']['status_code'] == 401:
                generate_text("Removing cookie!", 1)
                cookies.remove(cookie)
            elif attempt['join']['status_code'] == 403:
                if attempt["join"]["json"].get("errors") != None:
                    if attempt["join"]["json"]["errors"][0]["message"] != "Challenge is required to authorize the request":
                        generate_text("Account is full! Removing it; trying again...", 1)
                        with open("files/full.txt", "a") as f:
                            f.write(cookie + "\n")
                        f.close()
                        cookies.remove(cookie)
                
            else:
                generate_text(f"Weird issue occured: {attempt['join']['status_code']} / {attempt['join']['json']}", 1)
    
    if cookie not in cookies:
        with open("files/cookies.txt", "w") as file:
            for cookie in cookies:
                file.write(f"{cookie}\n")

    generate_text("Trying again in 2 seconds!", 1)
    await asyncio.sleep(2)
    return await account_switch()
## hello chat incorporated. looking into my code, aren't ya? want to improve it? fork!

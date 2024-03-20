from format import generate_logo, generate_text
from important.groups import check_group
from important.request import check_user, send_webhook
from important.claim import claim_group, shout_group, leave_group
from important.switch import account_switch, update_headers, new_account

import discord, json, asyncio, threading, time, os
from discord import Message, Embed
from secrets import choice

async def start() -> tuple[str, int, str, dict, str, str, list, list, bool]:
    enable_handler = None
    generate_text("we are making thing more awesome.. wait until finder will start, it will be quick..", 0)
    start_time: float = time.time()
    with open("files/settings.json", "r") as file:
        data: dict = json.load(file)

    user_data = await account_switch()

    user_account: dict = user_data[0]
    headers: dict = await update_headers(user_data[1])

    end_time: float = time.time()
    
    os.system("cls")
    texts = [
        f"succesfully started as `{user_account['username']}` ({user_account['user_id']})!",
        f"took {round(end_time - start_time, 4)} seconds to load everything up",
        f"claiming from {len(data['claiming_channels'])} channels, trusting to {len(data['trusted'])} users",
        "====================================="
    ]
    generate_logo()
    for text in texts:
        generate_text(text, 0)
        
    await send_webhook({"content": f"succesfully loaded in {round(end_time - start_time, 4)} seconds as `{user_account['username']}` *({user_account['user_id']})*!"}) 
    
    if data["debug"]["enable"] == True:
        if data["debug"]["showDiscordHandler"] == True:
            enable_handler = True

    return user_account["username"], user_account["user_id"], user_data[1], headers, data["prefix"], data["token"], data["claiming_channels"], data["trusted"], enable_handler

def sync_update_headers():
    global headers, cookie
    while True:
        headers = asyncio.run(update_headers(cookie))
        time.sleep(.01)

def handle_id(link: list) -> int:
    for item in link:
        if item.isdigit():
            return int(item)

    return 0

client = discord.Client()

@client.event
async def on_message(msg):
    global user_id, username, cookie, headers, prefix, claiming_channels, trusted, claimed, claimed_attempts
    message: Message = msg

    if message.content.lower().startswith(prefix):
        if message.author.id in trusted or message.author == client.user or message.author.id == 1137484045501092012:

            if message.author == client.user:
                ctx = message
            else:
                ctx = await message.reply("**imagine that there is something useful**")

            with open("files/settings.json", "r") as file:
                body: dict = json.load(file)

            split: list = message.content.split(" ")
            if message.content.lower().startswith(f"{prefix}trust"):
                if message.author.id == client.user.id or message.author.id in trusted:
                    if len(split) > 1:
                        if split[1].isdigit():
                            if int(split[1]) in trusted:
                                body["trusted"].remove(int(split[1]))
                            else:
                                body["trusted"].append(int(split[1]))
                        else:
                            await ctx.edit(f"You cannot add users by pinging them, or saying their name. Usage: \n> **{prefix}trust `user-id`**")
                else:
                    await ctx.edit(f"Only client owners can use this command.")

            elif message.content.lower().startswith(f"{prefix}finder"):
                if message.author.id == client.user.id or message.author.id in trusted:
                    if len(split) == 3:
                        if split[1].lower() == "add" or split[1].lower() == "remove":
                            if split[2].isdigit():
                    
                                if split[1].lower() == "add":
                                    if int(split[2]) in claiming_channels:
                                        await ctx.edit(f"You cannot add same channel twice!")
                                    else:
                                        body["claiming_channels"].append(int(split[2]))

                                elif split[1].lower() == "remove":
                                    if int(split[2]) not in claiming_channels:
                                        await ctx.edit(f"You cannot remove same channel twice!")
                                    else:
                                        body["claiming_channels"].remove(int(split[2]))

                        else:
                            await ctx.edit(f"You need to or remove, or delete finder. Usage: \n> **{prefix}finder `add/remove` `channel-id`**")
                else:
                    await ctx.edit(f"Only client owners can use this command.")

            elif message.content.lower().startswith(f"{prefix}prefix"):
                if message.author.id == client.user.id or message.author.id in trusted:
                    if len(split) > 1:
                        body["prefix"] = split[1]
                        await ctx.edit(f"succesfully changed prefix to **`{split[1]}`**")
                    else:
                        await ctx.edit(f"You cannot change prefix to None. Usage: \n> **{prefix}prefix `new-prefix`**")
                else:
                    await ctx.edit(f"Only client owners can use this command.")

            elif message.content.lower().startswith(f"{prefix}help"):
                await ctx.edit(f"```> {prefix}help >> shows this command\n{prefix}finder [add/remove] [channel-id] >> adds, or removes channel from claiming [OWNERONLY]\n{prefix}trust [user-id] >> adds user to trusted. allows them use this client. [OWNERONLY]\n{prefix}prefix [new-prefix] >> changes prefix\n{prefix}data >> shows trusted, claiming channels and current account [OWNERONLY]\n{prefix}groups >> shows how many groups user owns```")
            
            elif message.content.lower().startswith(f"{prefix}data"):
                await ctx.edit(f"```user: {username}\nuID: {user_id}\nclaiming: {claiming_channels}\ntrusted: {trusted}```")
            
            elif message.content.lower().startswith(f"{prefix}groups"):
                amount, unclaim = await check_user(user_id)

                if len(unclaim) == 0:
                    await ctx.edit(f"**{username}** owns **{amount}** groups")
                else:
                    message = await ctx.edit(f"**{username}** owns **{amount}** groups, and **{len(unclaim)}** unclaimed groups; leaving unclaimed groups")

                    for group_id in unclaim:
                        leave_attempt = await leave_group(group_id, user_id, headers)
                        await message.edit(message.content + "\n" + str(leave_attempt))
            
            elif message.content.lower().startswith(f"{prefix}addcookie"):
                if len(split) > 1:
                    cookie = split[1]

                    with open("files/cookies.txt", "a") as file:
                        file.write(cookie + "\n")
                    file.close()

                    await ctx.add_reaction("✅")
            
            elif message.content.lower().startswith(f"{prefix}switch"):
                if message.author.id == client.user.id or message.author.id in trusted:
                    username, user_id, cookie, headers = await new_account()

            if claiming_channels != body["claiming_channels"] or trusted != body["trusted"] or prefix != body["prefix"]:
                claiming_channels = body["claiming_channels"]
                trusted = body["trusted"]
                prefix = body["prefix"] 

                with open("files/settings.json", "w") as file:
                    json.dump(body, file, indent=4)

                await ctx.add_reaction("✅")
                await ctx.edit(f"succesfully changed!")

    if message.channel.id in claiming_channels:
        group_id = None

        if "roblox.com" in message.content:
            group_id = handle_id(message.content.split("/"))
        else:
            if message.embeds:
                embed: Embed = message.embeds[0]

                if "roblox.com" in embed.title:
                    group_id = handle_id(embed.title.split("/"))
                elif "roblox.com" in embed.description:
                    group_id = handle_id(embed.description.split("/"))
                else:
                    for field in embed.fields:
                        if "roblox.com" in field.value:
                            group_id = handle_id(field.value.split("/"))
                        elif "roblox.com" in field.name:
                            group_id = handle_id(field.name.split("/"))

        if isinstance(group_id, int) and group_id != 0:
            if group_id in claimed:
                return None
            claimed.append(group_id)
            claimed_attempts += 1
            
            claim_attempt: dict = await claim_group(group_id, headers)
            with open('files/settings.json', 'r') as f: data = json.load(f)
            if data['debug']['showClaimData'] == True:
                if data["debug"]["enable"] == False:
                    generate_text(str(claim_attempt), 3)

            if claim_attempt["join"]["status_code"] == 200:
                if claim_attempt["claim"]["status_code"] == 200:
                    generate_text(f"claimed {group_id} in {round(claim_attempt['time'], 4)} seconds!", 0)
                    tasks = [check_group(group_id, claim_attempt["time"], headers, client)]

                    if data["autoclaiming"]["customShouts"] == True:
                        shouts: list = data["autoclaiming"]["shouts"]

                        if len(shouts) == 0 or len(shouts) == 1:
                            generate_text("if you are going to use custom shouts, add more, than just one or none.", 3)
                            shout_text: str = data["autoclaiming"]["defaultShout"]
                        else:
                            shout_text = choice(shouts)
                        
                        tasks.append(
                            shout_group(group_id, shout_text, headers)
                        )
                    
                    await asyncio.gather(*tasks)
                else:
                    leave_attempt: dict = await leave_group(group_id, user_id, headers)
                    if data['debug']['showClaimData'] == True:
                        if data['debug']['enable'] == True:
                            generate_text(str(leave_attempt), 3)
    
                    if claim_attempt["claim"]["status_code"] == 403:
                        generate_text(f"failed to claim {round(claim_attempt['time'], 4)}, because someone was faster", 0)
                        await asyncio.gather(
                            send_webhook({"content": f"succesfully **failed** to autoclaim `{group_id}` in **{round(claim_attempt['time'], 4)} seconds**, because someone got it faster."}),
                        )
                    elif claim_attempt["claim"]["status_code"] in [400, 500]:
                        generate_text(f"failed to claim {round(claim_attempt['time'], 4)}, because roblox did their woopsies ({claim_attempt['claim']['status_code']})", 0)
                        await asyncio.gather(
                            send_webhook({"content": f"succesfully **failed** to autoclaim `{group_id}` in **{round(claim_attempt['time'], 4)} seconds**, because Roblox did their fuck up! :3 ({claim_attempt['claim']['status_code']})"}),
                        )
                    elif claim_attempt["claim"]["status_code"] == 429:
                        generate_text(f"failed to claim {round(claim_attempt['time'], 4)}, because ratelimit. account hopping", 0)
                        await asyncio.gather(
                            send_webhook({"content": f"succesfully **failed** to autoclaim `{group_id}` in **{round(claim_attempt['time'], 4)} seconds**, because caught ratelimit. account-hopping!"}),
                            new_account()
                        )
            else:
                leave_attempt: dict = await leave_group(group_id, user_id, headers)
                if data['debug']['showClaimData'] == True:
                    if data["debug"]["enable"] == False:
                        generate_text(str(leave_attempt), 3)

                if claim_attempt["join"]["status_code"] == 429:
                    generate_text(f"failed to claim {round(claim_attempt['time'], 4)}, because someone ratelimit. account hopping.", 0)
                    await send_webhook({"content": f"succesfully **failed** to autoclaim `{group_id}` in **{round(claim_attempt['time'], 4)} seconds**, because caught ratelimit. account-hopping!"}),
                    claimed_attempts = 0
                    username, user_id, cookie, headers = await new_account()
                if claim_attempt["join"]["status_code"] == 403:
                    if claim_attempt["join"]["json"].get("errors") != None:
                        if claim_attempt["join"]["json"]["errors"][0]["message"] == "You cannot join a closed group.":
                            generate_text(f"failed to claim {round(claim_attempt['time'], 4)}, because group is closed", 0)
                        elif claim_attempt["join"]["json"]["errors"][0]["message"] == "You are already in the maximum number of groups.":
                            generate_text(f"{username} is currently full!", 0)
                            await send_webhook({"content": f"succesfully **failed** to autoclaim `{group_id}` in **{round(claim_attempt['time'], 4)} seconds**, because account is full *||{cookie[:150]}||*"})
                            with open('files/full.txt', 'a') as f:
                                f.write(cookie + '\n')
                                f.close()

                                with open('files/cookies.txt', 'r') as f:
                                    cookies = f.read().splitlines()
                                    f.close()

                                    cookies.remove(cookie)
                                    with open('files/cookies.txt', 'w') as f:
                                        f.write('\n'.join(cookies))
                                    f.close()        
                                claimed_attempts = 0
                                username, user_id, cookie, headers = await new_account()
        if claimed_attempts == 10:
            claimed_attempts = 0
            username, user_id, cookie, headers = await new_account()

claimed = []; claimed_attempts = 0; username, user_id, cookie, headers, prefix, token, claiming_channels, trusted, enable_handler = asyncio.run(start())
threading.Thread(target=sync_update_headers).start()

if enable_handler != None and enable_handler == True: 
    client.run(token=token)
else: 
    client.run(token=token, log_handler=None)

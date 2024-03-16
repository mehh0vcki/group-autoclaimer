<p align="center">
    <img width="500" src="https://raw.githubusercontent.com/mehh0vcki/group-autoclaimer/main/images/title.png" alt="mehhovcki group autoclaimer">
</p>

# mehhovcki group autoclaimer,
or **ansel** is, probably, the most **user-friendly** and **easy to use** group autoclaimer right now. It offers many features, just like

- console Custmozation
- allowance of multipe users to access bot's commands
- unlimited amount of webhooks, cookies
- and many more...




* quick note!
    * now, you can receive support at [this server](https://discord.gg/TdwpsQhtUx). any questions, suggestions and etc will be accepted only here from now on.

## quick access
* [how do i even start using it?](#how-do-i-even-start-using-it)
* [how do i edit `files/settings.json`?](#how-do-i-edit-filessettingsjson) < <i>(you are here!)</i>
    * [webhooks](#webhooks)
    * [claiming channels](#claiming-channels)
    * [debug](#debug)
    * [autoclaiming](#autoclaiming)
    * [colors](#colors)
    * [trusted](#trusted)
    * [prefix & token](#prefix--token)
* [authors & faq](#authors-and-faq)
    * [faq](#faq)

## how do i even start using it?
at first, lets start with programms required to even use this autoclaimer.

1. any normal text editor, for example, [**visual studio code**](https://code.visualstudio.com/download)
2. [**python**](https://python.org/downloads/) *(recommended to use version **3.12.2**, because autoclaimer was written on it)*
3. [**git**](https://git-scm.com/download)

after you install everything required for this autoclaimer, install its source by clicking on **Code**, then **Download ZIP**.

<p align="center"> <img width="300" src="https://raw.githubusercontent.com/mehh0vcki/group-autoclaimer/main/images/install.png" alt="installation button"> 
</p>

after you install everything and extract everything required, open `cmd` and run commmand `python3 -m pip install -r requirements.txt`.

## how do i edit `files/settings.json`?
### webhooks
```json
{
    "webhooks": [],
}
```
* webhooks are being used for sending logs *(join, claim, fail, account switch)* and detections. to put every new webhook, add `"link"`. if you have more, than 1 webhook, after previous add `,`. like this: `["abc", "def"]`

### claiming channels
```json
    "claiming_channels": [],
```
* claiming channels are what your bot autoclaiming from. do not add channels manually, but use `//finder add [channel-id]`.

### requirements
```json
    "requirements": {
        "mode": ">=",
        ...
    },
```
* requirements are settings for detections, that will notify you about group if any of them will be meet. there only 4 modes: `>` *(more than)*, `>=` *(more than or equal to)*, `<` *(less than)* and `<=` *(less than on equal to)*

### debug
```json
    "debug": {
        "enable": false,
        "showAccountSwitchData": true,
        "showDiscordHandler": true,
        "showClaimData": true
    },
```
* debug is a setting, that enables to see more information. you can disable, or enable all debug settings without reloading except for `showDiscordHandler`.

### autoclaiming
```json
"autoclaiming": {
        "customShouts": true,
        "shouts": ["..."]
    },
```
* this enables custom shouts. have more, than 2 shouts in `shouts` list, or else it will use default one. please.

### colors
```json
"colors": {
        "default": [...],
        "account": [...],
        "debug": [...]
    },
```
* change colors in console. please, if you are going to do custom colors, use **2 colors**. if you want only 1 color, do this: `"coloruwant", "coloruwant"`. else: `"coloruwant1", "coloruwant2"`. should be in html format.

### trusted
```json
    "trusted": [],
```
* trusted people, that can use `//help`, `//data` and `//groups`. do not add trusted manually, but use `//trust [user-id]`


### prefix & token
```json
    "prefix": "//",
    "token": ""
```
* 2 most important settings of this autoclaimer. first, is what your bot will respond to. second, is what account your bot is going to run at.

if you don't know how to get discord token, or roblox cookie, also known as **.ROBLOSECURITY**, i recommend you watch this: [roblox](https://youtu.be/sz07F5inaFg) [discord](https://youtu.be/PCU8obaQI64)

## authors and faq
everything is created by [@mehh0vcki](https://github.com/mehh0vcki)

### faq
#### there's no questions yet. ask them in my discord, @mehhovcki to make some appear!

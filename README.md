# Obon Instagram Scraper ![GitHub follow](https://img.shields.io/github/followers/rezaffikri?label=Follow&style=social) ![GitHub repo size](https://img.shields.io/github/repo-size/rezaffikri/ObonInstagramScraper) ![GitHub](https://img.shields.io/github/license/rezaffikri/ObonInstagramScraper)

 Python project to scrap today video and photo with caption and send it to telegram group using.
 The initial code base on [Automated-Media-Collector](https://github.com/ficanovak/Automated-Media-Collector).
 
 ## Requirements
- bot telegram
- python
- instaloader
- telegram-send
 
 ##  Setup
Creating a Bot on Telegram:
- Visit BotFather channel on Telegram
- Send command /newbot
- Follow the BotFather instruction create Bot
- Save the Telegram Bot Token

Install Python:
- Install Python
- Add it to PATH if not automatically

Install Python Project:
- Run CMD as administrator
```elm
pip install instaloader
pip install telegram-send
```

Edit ObonInstagramScraper.py:
- Create or edit AppSettings.json file, see AppSettings.Development.json for example
- Edit username and password on AppSettings.json, insert empty value if you not want to login
    - *If you want to download private user media, you need to login and follow their instagram
    - *If your network has been restricted, you need to login too, or you have to wait before hit again and i don't know how long
- Insert all of username you want to scrap on PROFILES = ["username_1", "username_2"]
- Just in case to prevent network to be restrict, the app will sleep to delay hit, Edit time.sleep(<DelayValue>) to fix value or smaller range number
Connecting Telegram bot:
- Via command line:
    - Run CMD as administrator
    ```elm
    telegram-send --configure-group
    ```
    - Follow the telegram-send instruction to connecting to your group
- Via AppSettings.json:
    - Create or edit AppSettings.json file, see AppSettings.Development.json for example
    - Edit token and chat id on AppSettings.json, insert empty value if you connecting telegram bot via command line
    - Get chat id with this step:
        - Add the Telegram Bot to the group.
        - Get the list of updates for your Bot: api.telegram.org/bot<Telegram Bot Token>/getUpdates, example: api.telegram.org/bot139___UdeY/getUpdates
        - Look for the "chat" object, on the example below the Chat Id is -211287643:
            ```
           "chat":{"id":211287643,"title":"InstagramGroup","type":"group","all_members_are_administrators":true}
            ```
        - If you created the new group with the bot and you only get {"ok":true,"result":[]}, remove and add the bot again to the group.

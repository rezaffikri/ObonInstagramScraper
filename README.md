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
- Save the access token

Install Python:
- Install Python
- Add it to PATH if not automatically

Install Python Project:
- Run CMD as administrator
```elm
pip install instaloader
pip install telegram-send
```
Connecting Telegram bot:
- Run CMD as administrator
```elm
telegram-send --configure-group
```
- Follow the telegram-send instruction to connecting to your group
- Edit ObonInstagramScraper.py for set user or set accounts you'd like to follow, and run it.

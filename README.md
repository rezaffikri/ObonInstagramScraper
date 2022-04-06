# Obon Instagram Scraper ![GitHub follow](https://img.shields.io/github/followers/rezaffikri?label=Follow&style=social) ![GitHub repo size](https://img.shields.io/github/repo-size/rezaffikri/ObonInstagramScraper) ![GitHub](https://img.shields.io/github/license/rezaffikri/ObonInstagramScraper)

 This is my first Python Project, this python project is to scrap instagram today video and photo with caption and send it to telegram group or channel and ready to be deploy on heroku.
 Inspired by by this project [Automated-Media-Collector](https://github.com/ficanovak/Automated-Media-Collector) by [ficanovak](https://github.com/ficanovak).
 
 ## Requirements
- bot telegram
- python
- instaloader
- telegram-send
 
 ##  Setup
Creating a [Bot on Telegram](https://core.telegram.org/bots):
- Visit BotFather channel on Telegram
- Send command /newbot
- Follow the BotFather instruction to create Bot
- Save the Telegram Bot Token

Install Python:
- Install Python
- Add it to PATH if not automatically

Install Python Modules:
- Open cmd and use the following command:
    ```elm
    pip install instaloader

    pip install telegram-send
    ```

Create and configure AppSettings.json:
- See AppSettings.Development.json for example
- Set delay profile and post, if you dont want any delay set min and max to 0
- Set instagram username and password, insert empty value if you don't want to login
    - *If you want to download private user media, you need to login and follow their instagram
    - *If you are not login, to avoid your network/IP being restricted, please set the reasonable delay or leave the delay value as default
    - *If your network/IP has been restricted, you can login and instanly can hit again or if you still don't want to login, you have to wait before hit again and i don't know how long
    - *If you login, to minimize suspicious movements of your instagram account, please set the reasonable delay or leave the delay value as default
    - **Discalimer**: I am not responsible if your instagram account is banned, blocked or restricted. if you concern about your primary instagram account, you can test use this with new instagram account or use it without login
- Set instagram profiles all of username you want to scrap
- Set is_data_retention_on to true if you want to delete downloaded file every the end of day or false to keep forever the downloaded file
- Set is_always_running to true if you want the app to always running or false if you don't need the app to run 24/7 and use scheduler to run this app
- For configure telegram_send check on the Connecting Telegram Bot section

Connecting Telegram Bot:
- Via command line:
    - Open cmd and use the following command:
        ```elm
        telegram-send --configure-group

        or

        telegram-send --configure-channel
        ```
    - Follow the telegram-send instruction to connecting to your group/channel
- Via AppSettings.json:
    - Set telegram_send token with Telegram Bot Token and chat_id with your group/channel chat id, insert both with empty value if you already connecting telegram bot via command line
        - Get chat_id with this step:
            - Add the Telegram Bot to the group/channel, for channel you need to make the bot administrator.
            - Hit api.telegram.org/bot[ token ]/getUpdates, example: api.telegram.org/bot139___:______UdeY/getUpdates
            - Look for the "chat" object, on the example below the Chat Id is -211287643:
                ```elm
                "chat":{"id":211287643,"title":"InstagramGroup","type":"group","all_members_are_administrators":true}
                ```
                - If you only get {"ok":true,"result":[]}, remove and add the bot again to the group/channel.
                - if you can't send message to channel and get response {"ok":false,"error_code":403,"description":"Error: Forbidden: bot is not a member of the channel"}, use this step:
                    - Make sure the channel is public (you can set it private later)
                    - Set the channel url, example telegram.me/testChannel
                    - Then the channel id will be the same as the channel url, so for this example the channel id is testChannel
                    - Hit https://api.telegram.org/bot[ token ]/sendMessage?chat_id=@testChannel&text=Test
                    - If you success send the message, you can change the channel to private again and make sure again the Chat Id is correct and not change

## [Deploy to Heroku](https://devcenter.heroku.com/articles/getting-started-with-python)
- Via Heroku CLI
    - Install Heroku CLI
    - Install git-scm
    - Open cmd on your project and use the following command:
        ```elm
        heroku login

        heroku create NAME_OF_YOUR_HEROKU_APP

        heroku git:remote -a NAME_OF_YOUR_HEROKU_APP

        git add .

        git commit -m "initial-commit"

        git push heroku main
        ```
- Via Heroku Dashbord with Github
    - Create a new app
    - Connect to github
    - Choose your repo to connect
    - Choose your branch to deploy
    - Deploy Branch
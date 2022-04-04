import shutil
import sys
import instaloader
import telegram_send
import time
import datetime
import os
import platform
import random
import json

print("Starting")
L = instaloader.Instaloader(download_comments=False, max_connection_attempts=9, post_metadata_txt_pattern=None, save_metadata=False, download_video_thumbnails=False, download_geotags=False, filename_pattern="{shortcode}")

present = datetime.datetime.now()
folderDownload = "MediaDownloads/"
executedPath = os.getcwd()
print("executedPath: " +executedPath)
donwloadPath = executedPath + "/"  + folderDownload

if os.path.exists("AppSettings.json"):
    with open('AppSettings.json', 'r') as f:
        config = json.load(f)
        instagramUserName = config["instagram"]["username"]
        instagramPassword = config["instagram"]["password"]
        telegramToken = config["telegram_send"]["token"]
        telegramChatId = config["telegram_send"]["chat_id"]
        PROFILES = config["instagram"]["profiles"]

        if not isinstance(PROFILES, list ):
            sys.exit("Profiles is not configured properly")

        pathConfig = telegram_send.get_config_path()
        if not os.path.exists(pathConfig.replace("telegram-send.conf", "")):
            os.makedirs(pathConfig.replace("telegram-send.conf", ""))
        print("telegram-send.conf path: " + pathConfig)
        if telegramToken and telegramChatId:
            with open(pathConfig, 'w+') as f:
                f.write(f'[telegram]\ntoken = {telegramToken}\nchat_id = {telegramChatId}')
                print("Override telegram-send config")
            telegram_send.send(messages=["Telegram bot synced! with Override Config"])
        if instagramUserName and instagramPassword:
            # if you want to download private user media, you need to login and follow their instagram
            # if your network has been restricted, you need to login too, or you have to wait before hit again and i don't know how long
            print("Login")
            BOT_INSTAGRAM_ACCOUNT = L.login(instagramUserName,instagramPassword)
            print("Login successful")
            telegram_send.send(messages=["Instagram login with username: " + instagramUserName]) 
else:
    # assume you are not want to login and already config telegram-send from command line with telegram-send --configure-group
    print("Not login")
    telegram_send.send(messages=["Telegram bot synced! with Default Config"])  

while True:
    try:
        for PROFILE in PROFILES:
            L.dirname_pattern = donwloadPath + PROFILE
            print("Profile: "+PROFILE)
            print("Timeout: random between 31 and 60 seconds")
            time.sleep(random.randint(31,60))
            profile = instaloader.Profile.from_username(L.context, PROFILE)
            print("Profile loaded")
            for post in profile.get_posts():
                #get today post only
                if post.date_local.date() == datetime.datetime.now().date():
                    print("Timeout: random between 31 and 60 seconds")
                    time.sleep(random.randint(31,60))
                    download = L.download_post(post,PROFILE)
                    folderProfile = folderDownload + post.owner_username
                    if download == True:
                        loopId = 0
                        if post.mediacount >= 2:
                            for slide in post.get_sidecar_nodes():
                                try:
                                    loopId = loopId + 1
                                    fileId = "_"+str(loopId)
                                    if not slide.is_video:
                                        with open(folderProfile+"/"+post.shortcode+fileId+".jpg", "rb") as f:
                                            telegram_send.send(images=[f]) 
                                    else:
                                        with open(folderProfile+"/"+post.shortcode+fileId+".mp4", "rb") as f:
                                            telegram_send.send(files=[f])   
                                except ValueError:
                                    print("Send media error")
                                    pass
                        else:
                            try:
                                if not post.is_video:
                                    with open(folderProfile+"/"+post.shortcode+".jpg", "rb") as f:
                                        telegram_send.send(images=[f]) 
                                else:
                                    with open(folderProfile+"/"+post.shortcode+".mp4", "rb") as f:
                                        telegram_send.send(files=[f])   
                            except ValueError:
                                print("Send media error")
                                pass
                        try:
                            if post.caption is None:
                                telegram_send.send(messages=[post.owner_username+": None \n" + post.date_local.strftime("%d/%b/%Y, %H:%M:%S")])
                            else:
                                telegram_send.send(messages=[post.owner_username+": "+post.caption + "\n" + post.date_local.strftime("%d/%b/%Y, %H:%M:%S")])
                        except:
                            print("Send caption error")
                            pass
                    else:
                        # if donwload false, it means all post already downloaded
                        break  
                else:
                    # no new post today
                    break  
            print("Next")
        # every the end of the loop, if old present variable more than datetime.,now delete old file
        if present.date() < datetime.datetime.now().date():
            try:
                present = datetime.datetime.now()
                print("Start delete old file")
                shutil.rmtree(donwloadPath)
                print("Old file deleted")
            except:
                print("Delete old file error")  
    except ValueError:
        print(ValueError)
        pass

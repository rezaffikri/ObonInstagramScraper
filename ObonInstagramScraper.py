import shutil
import sys
import instaloader
import telegram_send
import time
import datetime
import os
import random
import json

print("Starting")
L = instaloader.Instaloader(download_comments=False, post_metadata_txt_pattern=None, save_metadata=False, download_video_thumbnails=False, download_geotags=False, filename_pattern="{shortcode}")

executedPath = os.getcwd()
print("executedPath: " +executedPath)
# convert datetime to your country or local time, for this example i just add +7 hours because my timezone is Asia/jakarta
postDateMin = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
folderDownload = "MediaDownloads/"
donwloadPath = executedPath + "/"  + folderDownload
print("donwloadPath: " +donwloadPath)

if os.path.exists("AppSettings.json"):
    try:
        with open('AppSettings.json', 'r') as f:
            config = json.load(f)
            isDataRetentionOn = config["is_data_retention_on"]
            isAlwaysRunning = config["is_always_running"]
            igDelayProfileMin = int(config["delay"]["profile_min"])
            igDelayProfileMax = int(config["delay"]["profile_max"])
            igDelayPostMin = int(config["delay"]["post_min"])
            igDelayPostMax = int(config["delay"]["post_max"])
            print("igDelayProfileMin:" + config["delay"]["profile_min"] + " igDelayProfileMax:" + config["delay"]["profile_max"] + " igDelayPostMin:" + config["delay"]["post_min"] +" igDelayPostMax:" + config["delay"]["post_max"])    
            profiles = config["instagram"]["profiles"]

            if not isinstance(profiles, list ):
                sys.exit("profiles in AppSettings.json is not configured properly")

            pathConfig = telegram_send.get_config_path()
            if not os.path.exists(pathConfig.replace("telegram-send.conf", "")):
                os.makedirs(pathConfig.replace("telegram-send.conf", ""))
            print("telegram-send.conf path: " + pathConfig)
            
            telegramToken = config["telegram_send"]["token"]
            telegramChatId = config["telegram_send"]["chat_id"]
            if telegramToken and telegramChatId:
                with open(pathConfig, 'w+') as f:
                    f.write(f'[telegram]\ntoken = {telegramToken}\nchat_id = {telegramChatId}')
                    print("telegram-send config via AppSettings.json")
            else:
                print("assume you already set telegram-send config via cmd \nif error please make sure you already configure telegram-send via cmd or via AppSettings.json")
            telegram_send.send(messages=["Telegram bot synced!"])
            
            instagramUserName = config["instagram"]["username"]
            instagramPassword = config["instagram"]["password"]
            if instagramUserName and instagramPassword:
                print("Login instagram")
                L.login(instagramUserName,instagramPassword)
                print("Login instagram successful")
                telegram_send.send(messages=["Instagram login with username: " + instagramUserName])
            else:
                print("Without login instagram")
    except ValueError:
        sys.exit("AppSetting.json is not configured properly: " + ValueError)
else:
    sys.exit("AppSetting.json is not found")

isLastMinutePostCheck = "false"
while True:
    try:
        for itemProfile in profiles:
            L.dirname_pattern = donwloadPath + itemProfile
            print("Profile: "+itemProfile)
            print("Delay Load Profile")          
            time.sleep(random.randint(igDelayProfileMin,igDelayProfileMax))
            profile = instaloader.Profile.from_username(L.context, itemProfile)
            print("Profile loaded")
            for post in profile.get_posts():
                postDateLocal = post.date_utc + datetime.timedelta(hours=7)
                if postDateLocal >= postDateMin:
                    print("Delay Download")
                    time.sleep(random.randint(igDelayPostMin,igDelayPostMax))
                    download = L.download_post(post,itemProfile)
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
                                            telegram_send.send(videos=[f])   
                                except ValueError:
                                    print("Send multiple media error: \n" + ValueError)
                                    pass
                        else:
                            try:
                                if not post.is_video:
                                    with open(folderProfile+"/"+post.shortcode+".jpg", "rb") as f:
                                        telegram_send.send(images=[f]) 
                                else:
                                    with open(folderProfile+"/"+post.shortcode+".mp4", "rb") as f:
                                        telegram_send.send(videos=[f])   
                            except ValueError:
                                print("Send single media error: \n" + ValueError)
                                pass
                        try:
                            if post.caption is None:
                                telegram_send.send(messages=[post.owner_username+": No caption \n" + postDateLocal.strftime("%d/%b/%Y, %H:%M:%S")])
                            else:
                                telegram_send.send(messages=[post.owner_username+": "+post.caption + "\n" + postDateLocal.strftime("%d/%b/%Y, %H:%M:%S")])
                        except:
                            print("Send caption error: \n" + ValueError)
                            pass
                    else:
                        # Post already donwloaded, no need to print info here because download_post from instaloader already print the info
                        break  
                else:
                    print("No new post today")
                    break
        datetimeNowLocal = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
        # every the end of the profiles loop, check postDateMin variable is equal today or not
        if postDateMin.date() < datetimeNowLocal.date():
            if isLastMinutePostCheck == "true":
                try:
                    isLastMinutePostCheck = "false"
                    postDateMin = datetime.datetime(datetimeNowLocal.year, datetimeNowLocal.month, datetimeNowLocal.day, 0, 0, 0)
                    if isDataRetentionOn == "true":
                        if os.path.exists(donwloadPath):
                            print("Start delete old file")
                            shutil.rmtree(donwloadPath)
                            print("Old file deleted")
                        else:
                            print("Folder download is empty")
                except ValueError:
                    print("Delete old file error: \n" + ValueError)
            else:
                isLastMinutePostCheck = "true"     
        if isAlwaysRunning == "false":
            sys.exit("Finish")
    except ValueError:
        print("Something wrong: \n" + ValueError)
        pass
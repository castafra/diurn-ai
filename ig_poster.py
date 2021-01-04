import json 
from instapy_cli import client
from instabot import Bot 
import os

with open('settings/ig_account.json') as json_file:
    data = json.load(json_file)
    username = data['username']
    password = data['password']

picture = r'C:\Users\François\Deep Learning\diurn-ai\to_post'

to_post = os.listdir('to_post')
if len(to_post) > 0 : 
    for file in to_post: 
        if file.endswith(".jpg"):
            picture_tp = picture +'\\'+ file
            print(picture_tp)
            name = file[:-4]
            print(name)
            with open('to_post/' +name+'.txt', 'r') as file_text:
                description_tp = file_text.read()
            print(description_tp)

            ### UPLOAD PHOTO 
            bot = Bot() 
            bot.login(username = username,  
                    password = password) 
            bot.upload_photo(picture_tp, 
                            caption =description_tp) 

            ### DELETE PHOTO AND DESCRIPTION POSTED 
            os.remove('to_post/' +name+'.txt')
            os.remove('to_post/' +name+'.jpg.REMOVE_ME')


'''
with client(username,password) as cli:
    cli.upload(picture,description)
'''
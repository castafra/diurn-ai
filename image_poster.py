import json 
from instapy_cli import client
from instabot import Bot 
import os
from PIL import Image, ImageFont, ImageDraw, ImageEnhance 
from datetime import date 
import requests as requests
import urllib.request as url 

with open('photo_info.json') as file: 
    data = json.load(file)

theme = data['theme']
text = data['text']
caption = data['caption']

today = date.today()
# dd/mm/YY
date = today.strftime("%b-%d-%Y")


class instagramImage():

    def __init__(self): 
        self.theme = theme
        self.text = text
        self.caption = caption
        self.date = date

    def create_background(self):
        with open('settings/unsplash_account.json') as json_file:
            data = json.load(json_file)
        client_id = data['access_key']
        r = requests.get('https://api.unsplash.com/search/photos?query='+self.theme+'&page=1&per_page=30&client_id='+client_id)

        data = r.json()
        link = data['results'][0]['urls']['raw']

        filename = 'background.jpg'
        url.urlretrieve(link,filename)

    def create_image(self,factor = 0.5, img_fraction =1.2):
        original_background_image = Image.open("background.jpg")
        enhancer  = ImageEnhance.Brightness(original_background_image)
        background_image = enhancer.enhance(factor)

        W, H = background_image.size

        fontsize = 1  # starting font size

        font = ImageFont.truetype('fonts/typewriter/TYPEWR__.ttf', fontsize)
        while font.getsize(self.text)[0]/3 < img_fraction*background_image.size[0]:
            # iterate until the text size is just larger than the criteria
            fontsize += 1
            font = ImageFont.truetype('fonts/typewriter/TYPEWR__.ttf', fontsize)
            

        image_editable = ImageDraw.Draw(background_image)

        w, h = image_editable.textsize(self.text,font=font)
        image_editable.text(((W-w)/2,(H-h)/2), self.text, (255, 255, 255), font=font)


        #SAVE THE IMAGE IN THE 2 POST FOLDERS
        
        background_image.save("to_post/"+self.date+"-"+self.theme+".jpg")
        background_image.save("posts/"+self.date+"-"+self.theme+".jpg")

        #SAVE THE CAPTION IN THE 2 POST FOLDERS 
        with open("to_post/"+self.date+"-"+self.theme+".txt",'w') as text_file : 
            text_file.write(self.caption)
        with open("posts/"+self.date+"-"+self.theme+".txt",'w') as text_file : 
            text_file.write(self.caption)

        
    def post_image(self):
        with open('settings/ig_account.json') as json_file:
            data = json.load(json_file)
        username = data['username']
        password = data['password']
        picture = "C:\\Users\\François\\Deep Learning\\diurn-ai\\to_post"

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

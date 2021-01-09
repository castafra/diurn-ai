import json 
from instapy_cli import client
from instabot import Bot 
import os
from PIL import Image, ImageFont, ImageDraw, ImageEnhance 
from datetime import date 
import requests as requests
import urllib.request as url 



today = date.today()
# dd/mm/YY
date = today.strftime("%b-%d-%Y")


class instagramImage():

    def __init__(self): 
        self.themes = ''
        self.texts = ''
        self.caption = ''
        self.date = date

    def retrieve_news(self):
        with open('photo_info.json') as file: 
            data = json.load(file)
            self.themes = data['themes']
            self.texts = data['text']
            self.caption = data['caption']


    def create_background(self):
        with open('settings/unsplash_account.json') as json_file:
            data = json.load(json_file)
        client_id = data['access_key']
        for theme in self.themes:
            r = requests.get('https://api.unsplash.com/search/photos?query='+theme+'&page=1&per_page=30&client_id='+client_id)

            data = r.json()
            link = data['results'][0]['urls']['raw']

            filename = 'backgrounds/background-'+theme+'.jpg'
            url.urlretrieve(link,filename)

    def crop_center(self,pil_img, crop_width, crop_height):
        img_width, img_height = pil_img.size
        return pil_img.crop(((img_width - crop_width) // 2,
                            (img_height - crop_height) // 2,
                            (img_width + crop_width) // 2,
                            (img_height + crop_height) // 2))

    def crop_max_square(self,pil_img):
        return self.crop_center(pil_img, min(pil_img.size), min(pil_img.size))

    def create_image(self,factor = 0.75):
        k = 0
        for theme in self.themes : 
            original_background_image = Image.open('backgrounds/background-'+theme+'.jpg')
            img_cropped = self.crop_max_square(original_background_image)
            enhancer  = ImageEnhance.Brightness(img_cropped)
            background_image = enhancer.enhance(0.4)
           

            W, H = background_image.size

            font = ImageFont.truetype('fonts/typewriter/TYPEWR__.ttf', int(W/18))
                

            image_editable = ImageDraw.Draw(background_image)

            w, h = image_editable.textsize(self.texts[k],font=font)
            image_editable.text(((W-w)/2,(H-h)/2), self.texts[k], (255, 255, 255), font=font)


            #SAVE THE IMAGE IN THE 2 POST FOLDERS
            
            background_image.save("photo_to_post/"+self.date+"-"+str(k+1)+theme+".jpg")
            background_image.save("posts/"+self.date+"-"+str(k+1)+theme+".jpg")
            k += 1

        #SAVE THE CAPTION IN THE 2 POST FOLDERS 
        with open("caption_to_post/"+self.date+"-"+theme+".txt",'w') as text_file : 
            text_file.write(self.caption)
        with open("posts/"+self.date+"-"+theme+".txt",'w') as text_file : 
            text_file.write(self.caption)

        
    def post_image(self):
        with open('settings/ig_account.json') as json_file:
            data = json.load(json_file)
        username = data['username']
        password = data['password']
        picture = "C:\\Users\\François\\Deep Learning\\diurn-ai\\photo_to_post"

        to_post = os.listdir('photo_to_post')
        pictures_tp = []
        name_posts = []
        if len(to_post) > 0 : 
            for file in to_post: 
                if file.endswith(".jpg"):
                    pictures_tp.append( picture +'\\'+ file)
                    name_posts.append(file[:-4])
            caption_to_post = os.listdir('caption_to_post')
            print(caption_to_post) 
            with open('caption_to_post/' +caption_to_post[0], 'r') as file_text:
                description_tp = file_text.read()
            

            ### UPLOAD PHOTO 
            bot = Bot() 
            bot.login(username = username,  password = password) 
            bot.upload_photo(pictures_tp[0], caption =description_tp) 
            #bot.upload_album(pictures_tp, caption =description_tp)

            ### DELETE PHOTO AND DESCRIPTION POSTED 
            os.remove('caption_to_post/' +caption_to_post[0])
            os.remove('photo_to_post/' +to_post[0]+'.REMOVE_ME')
            for file in to_post[1:]:
                os.remove('photo_to_post/' +file)

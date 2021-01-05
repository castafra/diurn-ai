from PIL import Image, ImageFont, ImageDraw, ImageEnhance 
import json
from datetime import date 

with open('photo_info.json') as file: 
    data = json.load(file)

theme = data['theme']
text = data['text']
caption = data['caption']

original_background_image = Image.open("background.jpg")
enhancer  = ImageEnhance.Brightness(original_background_image)
factor = 0.5
background_image = enhancer.enhance(factor)

W, H = background_image.size


fontsize = 1  # starting font size

# portion of image width you want text width to be
img_fraction =1.2

font = ImageFont.truetype('fonts/typewriter/TYPEWR__.ttf', fontsize)
while font.getsize(text)[0] < img_fraction*background_image.size[0]:
    # iterate until the text size is just larger than the criteria
    fontsize += 1
    font = ImageFont.truetype('fonts/typewriter/TYPEWR__.ttf', fontsize)

image_editable = ImageDraw.Draw(background_image)

w, h = image_editable.textsize(text,font=font)
image_editable.text(((W-w)/2,(H-h)/2), text, (255, 255, 255), font=font)


#SAVE THE IMAGE IN THE 2 POST FOLDERS
today = date.today()
# dd/mm/YY
date = today.strftime("%b-%d-%Y")
background_image.save("to_post/"+date+"-"+theme+".jpg")
background_image.save("posts/"+date+"-"+theme+".jpg")

#SAVE THE CAPTION IN THE 2 POST FOLDERS 
with open("to_post/"+date+"-"+theme+".txt",'w') as text_file : 
    text_file.write(caption)
with open("posts/"+date+"-"+theme+".txt",'w') as text_file : 
    text_file.write(caption)

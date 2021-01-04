import image_poster 

def post():
    new_post = image_poster.instagramImage()
    new_post.create_background()
    new_post.create_image()

if __name__ == "__main__":
    post()
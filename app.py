import image_poster 
import news_scrapper
import time 
import random

def scrap():
    news = news_scrapper.getNews(3)
    news.get_history_facts()
    news.get_urls()
    news.get_articles()
    news.get_news()


def post(what = "photo"):
    new_post = image_poster.instagramImage()
    new_post.retrieve_news()
    new_post.create_background()
    new_post.create_image()
    if what == "photo":
        new_post.post_image()
    elif what == "story":
        new_post.post_story()

if __name__ == "__main__":
    scrap()
    post("photo")
    
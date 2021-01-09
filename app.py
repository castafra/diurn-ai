import image_poster 
import news_scrapper

def scrap():
    news = news_scrapper.getNews(3)
    news.get_history_facts()
    news.get_urls()
    news.get_articles()
    news.get_news()


def post():
    new_post = image_poster.instagramImage()
    new_post.retrieve_news()
    new_post.create_background()
    new_post.create_image()
    new_post.post_image()

if __name__ == "__main__":
    scrap()
    post()
    
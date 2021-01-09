import nltk
import newspaper
import string
import re
from collections import Counter
import datetime 
import json
import requests
from bs4 import BeautifulSoup
import random

home_page = "https://www.reuters.com/world"

on_thi_day_page = "https://www.onthisday.com/day/"

stopwords = ['i', 'me', 'my', 'myself', 'we','us' ,'our', 'ours', 'ourselves',
             'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 
             'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 
             "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 
             'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 
             'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 
             'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 
             'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 
             'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 
             'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 
             'through', 'during', 'before', 'after', 'above', 'below', 'to', 
             'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 
             'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 
             'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 
             'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 
             'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 
             "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 
             'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 
             'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 
             'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', 
             "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 
             'weren', "weren't", 'won', "won't","would", 'wouldn', "wouldn't","doesn","reuters"]

class getNews():
    def __init__(self,n):
        self.urls = []
        self.articles = []
        self.themes = []
        self.n = n
        self.events = []
        self.events_year = []

    def get_urls(self):
        page = requests.get(home_page)
        soup = BeautifulSoup(page.content, 'html.parser')
        headlines = []
        for a in soup.find_all('a', href=True):
            if a['href'][:9]=='/article/' and (a['href'] not in headlines):
                headlines.append(a['href'])
                self.urls.append('https://www.reuters.com'+a['href'])

    def get_tokens(self,text):
        text_treated = text.replace('\n',' ').replace('/',' ').replace('-',' ').translate(str.maketrans('', '', string.punctuation))
        tokens = list(filter(lambda w: len(w) > 0, re.split('\W+', text_treated.lower())))
        return tokens

    def remove_stopwords(self,raw_tokens):
        return [x for x in raw_tokens if x not in stopwords]

    def get_articles(self):
        n = 1
        for url in self.urls[:self.n] : 
            article = newspaper.Article(url)
            article.download()
            article.parse()
            title = article.title 
            text = article.text 
            tokens = self.get_tokens(text)
            meaningful_tokens = self.remove_stopwords(tokens)
            occurence = Counter(meaningful_tokens)
            occ = occurence.most_common(2)
            theme= occ[0][0] + ' ' + occ[1][0]
            self.themes.append(theme)
            self.articles.append({'title': title,'text': text, 'tokens': tokens})
            n+= 1

    def get_news(self):
        today = datetime.date.today()
        date = today.strftime("%B %d, %Y")
        NEWS = []
        raw_NEWS = []

        for k in range(len(self.articles)):
            title = self.articles[k]['title']
            toks = list(filter(lambda w: len(w) > 0, re.split('\s*[|\s+]\s*', title)))
            NEW = ''
            raw_NEW = ''
            line = ''
            j=0
            for i in range(len(toks)-1):
                NEW = NEW + toks[i] + ' '
                line = line + toks[i] + ' '
                raw_NEW = raw_NEW + toks[i] + ' '
                if (j+1)%5 == 0 or len(line + toks[i+1])>30:
                    NEW = NEW + '\n\n'
                    line = ''
                    j=-1
                j+=1
            NEW = NEW + toks[-1]
            raw_NEW = raw_NEW[:-1]+'.'
            raw_NEWS.append(raw_NEW)
            NEWS.append(NEW)

        id1 = random.randint(1,3)
        id2 = random.randint(1,3) + id1
        history_fact = "On this date : \n"+"In "+self.events_year[id1]+', '+self.events[id1]+'\n'+"In "+self.events_year[id2]+', '+self.events[id2]
        Caption = 'Hello everyone, today is ' + date +'\n\n<b>History Facts :\n'+history_fact+'\n\nOn the news today :\n\n'+raw_NEWS[0]+'\n\n'+raw_NEWS[1]+'\n\n'+raw_NEWS[2]+'\n\n'+'\n\nSource: Reuters\nImages: Unsplash'

        photo_info = open("photo_info.json","r")
        json_news = json.load(photo_info)
        photo_info.close()

        json_news["themes"] = self.themes
        json_news["text"] = NEWS
        json_news["caption"] = Caption
        json_news["pos"] = list(range(self.n))
        json_news["history_events"] = self.events
        json_news["history_events_year"] = self.events_year

        photo_info = open("photo_info.json","w")
        json.dump(json_news,photo_info)
        photo_info.close()

    def get_history_facts(self):
        months = ['january','february','march','april','may','june','july','august','september','october','november','december']
        dt = datetime.datetime.today()
        month= months[dt.month -1]
        day  = dt.day

        url = "https://www.onthisday.com/day/"+month+"/"+str(day)

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        events_html = soup.findAll("li", {"class": "event"})

        for event in events_html : 
            year = event.a.text
            self.events_year.append(year)
            text = event.text
            text = text[(len(year)+1):]
            self.events.append(text)

        
            






    


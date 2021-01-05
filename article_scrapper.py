import nltk
import newspaper
import string
import re
from collections import Counter
from datetime import date 
import json

today = date.today()
# dd/mm/YY
date = today.strftime("%B %d, %Y")

reuters_article = newspaper.build('https://www.reuters.com/news/world',  memoize_articles = False)

urls = []
for article in reuters_article.articles: 
    url = article.url
    if url.startswith('http://www.reuters.com/article/us-') and len([i for i in urls if url[:44]  in i])==0:
        urls.append(url)


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

def get_tokens(text):
    text_treated = text.replace('\n',' ').replace('/',' ').replace('-',' ').translate(str.maketrans('', '', string.punctuation))
    tokens = list(filter(lambda w: len(w) > 0, re.split('\W+', text_treated.lower())))
    return tokens

def remove_stopwords(raw_tokens):
    return [x for x in raw_tokens if x not in stopwords]

articles = []
n = 1
for url in urls[:3] : 
    article = newspaper.Article(url)
    article.download()
    article.parse()
    title = article.title 
    text = article.text 
    tokens = get_tokens(text)
    meaningful_tokens = remove_stopwords(tokens)
    occurence = Counter(meaningful_tokens)
    if n == 1 : 
        occ = occurence.most_common(2)
        theme= occ[0][0] + ' ' + occ[1][0]
    articles.append({'title': title,'text': text, 'tokens': tokens})
    n+= 1

NEWS = ''

for k in range(len(articles)):
    title = articles[k]['title']
    toks = list(filter(lambda w: len(w) > 0, re.split('\s*[|\s+]\s*', title)))
    for i in range(len(toks)):
        NEWS = NEWS + toks[i] + ' '
        if (i+1)%9 == 0:
            NEWS = NEWS + '\n\n'
    if k != len(articles) - 1 :
        NEWS = NEWS + '\n\n\n\n'


Caption = 'Hello everyone, today is ' + date +'\nSources: Reuters'

print('Theme :',theme)
print('Text :',NEWS)
print('Caption :',Caption)

photo_info = open("photo_info.json","r")
json_news = json.load(photo_info)
photo_info.close()

json_news["theme"] = theme 
json_news["text"] = NEWS
json_news["caption"] = Caption

photo_info = open("photo_info.json","w")
json.dump(json_news,photo_info)
photo_info.close()
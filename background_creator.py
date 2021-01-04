import requests as requests
import urllib.request as url 

theme = 'news'
client_id = 'UGQX5yyaanKLcnefTjbhskio0hLyIyC0Wz2pe9HgHRI'
r = requests.get('https://api.unsplash.com/search/photos?query='+theme+'&page=1&per_page=30&client_id='+client_id)

data = r.json()
link = data['results'][0]['urls']['regular']

filename = 'background.jpg'
url.urlretrieve(link,filename)
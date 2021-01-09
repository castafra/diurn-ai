import json
import requests
from bs4 import BeautifulSoup
import datetime

months = ['january','february','march','april','may','june','july','august','september','october','november','december']
dt = datetime.datetime.today()
month= months[dt.month -1]
day  = dt.day

url = "https://www.onthisday.com/day/"+month+"/"+str(day)

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')


events_html = soup.findAll("li", {"class": "event"})
events = []

for event in events_html : 
    events.append(event.text)
    print(event.a.text)

#print(events)

import requests
from bs4 import BeautifulSoup

request = requests.get("https://www.youtube.com/results?search_query=%E5%91%A8%E6%9D%B0%E5%80%AB")
content = request.content
soup = BeautifulSoup(content, "html.parser")
for time in soup.find_all('span', {"class": "video-time"}):
    print(time.text)
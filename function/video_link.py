import requests
from bs4 import BeautifulSoup

request = requests.get("https://www.youtube.com/results?search_query=%E6%9C%A8%E6%9B%9C4%E8%B6%85%E7%8E%A9")
content = request.content
soup = BeautifulSoup(content, "html.parser")
for element in soup.find_all('a', {"rel": "spf-prefetch"}):
    video_title = element.get('title')
    video_link = element.get('href')
    print(video_title)
    print("https://www.youtube.com{}".format(video_link))
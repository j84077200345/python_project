import requests
from bs4 import BeautifulSoup

request = requests.get("https://www.youtube.com/results?search_query=%E6%9C%A8%E6%9B%9C4%E8%B6%85%E7%8E%A9")
content = request.content
soup = BeautifulSoup(content, "html.parser")
print(soup)
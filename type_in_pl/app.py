import requests
from bs4 import BeautifulSoup

INTRO = "https://blog.hjaem.info/2"

def main():
  res = BeautifulSoup(requests.get(INTRO).content, 'html.parser')
  print(res.prettify())

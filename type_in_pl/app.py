from functools import reduce
import requests
from bs4 import BeautifulSoup

BASE = "https://blog.hjaem.info/"
TOC  = BASE + "2"

def main():
  res = BeautifulSoup(requests.get(TOC).content, 'html.parser')
  article = res.select_one('.article_view')

  intro = article.select_one('p > a[href^="{}"]'.format(BASE))
  outro = article.select('p > a[href^="{}"]'.format(BASE))[-1]

  from itertools import takewhile, dropwhile
  ps = article.select('p')
  lpad = dropwhile(lambda p: p != intro.parent, ps)
  rpad = takewhile(lambda p: p != outro.parent, lpad)

  ps = list(rpad)
  ps.append(outro.parent)

  paired = list(map(
    lambda p: (
      list(map(lambda c: c.text.replace('\xa0', ' '), p.contents)), # title: List[str]
      p.contents[-1].attrs.get('href')),                            # href: str | None
    ps))                                                            # -> List[(List[str], str | None)]

  for p in paired:
    print(p)

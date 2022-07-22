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
      ''.join(map(lambda c: c.text.replace('\xa0', ' '), p.contents)),  # title: str
      p.contents[-1].attrs.get('href')),                                # href: str | None
    ps))                                                                # -> List[(str, str | None)]

  def iter(acc, p):
    title, href = p
    depth = (len(title) - len(title.lstrip())) // 4

    next = {
      'title': title,
      'link': href,
      'children': [],
      'depth': depth + 1
    }

    if depth == 0:
      acc.append(next)
    elif depth > 0:
      target = acc
      try:
        while depth > 0:
          target = target[-1]['children']
          depth = depth - 1
        target.append(next)
      except Exception as e:
        print('error', p, repr(e))

    return acc

  import pprint
  pprint.pprint(reduce(iter, paired, []))

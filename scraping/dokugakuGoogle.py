import urllib.request
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self,site):
        self.site = site

    def scrape(self):
        r = urllib.request.urlopen(self.site)
        html = r.read()
        parser = "html.parser"
        bs = BeautifulSoup(html,parser)
        for tag in bs.find_all('a'):
            url = tag.get('href')
            if url is None:
                continue
            if 'out' in url:
                if 'html' in url:
                    print(url)

news = 'https://blog.with2.net/ranking.php?cid=2341&p=0'
Scraper(news).scrape()
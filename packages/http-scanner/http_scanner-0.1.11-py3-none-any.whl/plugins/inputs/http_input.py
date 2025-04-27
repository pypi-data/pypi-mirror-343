import requests
from bs4 import BeautifulSoup

def fetch(settings):
    urls = settings.get('urls', [])
    texts = []
    for url in urls:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        texts.append(soup.get_text(separator='\n'))
    return texts

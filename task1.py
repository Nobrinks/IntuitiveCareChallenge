from bs4 import BeautifulSoup
from requests import get

BASE_URL = 'http://www.ans.gov.br'
PATH = '/prestadores/tiss-troca-de-informacao-de-saude-suplementar'

def get_html(url):
    return get(url).text

def parse_html(html):
    return BeautifulSoup(html, 'html.parser')

def select_first_url_path(bs,css_class, attribute):
    return bs.select_one(css_class)[attribute]

if __name__ == "__main__":
    page_html=get_html(BASE_URL+PATH)
    soup=parse_html(page_html)
    path=select_first_url_path(soup, '.alert-link', 'href')
    
    accessed_page=get_html(BASE_URL+path)
    
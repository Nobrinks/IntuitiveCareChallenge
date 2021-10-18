from bs4 import BeautifulSoup
from requests import get, codes

def get_html(url):
    response = get(url)
    if response.status_code == codes.OK:
        return response
    else:
        response.raise_for_status()

def parse_html(html):
    return BeautifulSoup(html, 'html.parser')

def select_first_url(bs, css_class, attribute='href'):
    return bs.find(class_=css_class)[attribute]

def download_file(url, filepath):
    pdf_url=get_html(url)
    with open(filepath, 'wb') as file:
        file.write(pdf_url.content)
    print("Download finished.")

if __name__ == "__main__":
    BASE_URL = 'https://www.gov.br'
    ROUTE = '/ans/pt-br/assuntos/prestadores/padrao-para-troca-de-informacao-de-saude-suplementar-2013-tiss'
    # Access the first website page
    page_html=get_html(BASE_URL+ROUTE)
    soup=parse_html(page_html.text)
    # Get link route to the page of the most recent version
    site=select_first_url(soup, "alert-link internal-link")
    # Access a second page where it is the pdf link
    accessed_page=get_html(site)
    soup=parse_html(accessed_page.text)
    # Get the pdf link located in the second page accessed
    pdf_url = select_first_url(soup, "btn btn-primary btn-sm center-block internal-link")
    filename=pdf_url.split('/')[-1]
    # Download the pdf file to the local path
    download_file(pdf_url, filename)
    
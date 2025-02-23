import re
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from bs4 import BeautifulSoup

class webscraper:
    base_url = "https://scholar.google.com/citations?user=ETIBghkAAAAJ&hl=en"
    publication_titles_since_2015 = list()
    publication_links_since_2015 = list()
    
    def get_bs_from_url(url = base_url):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            }
           
            response = urlopen(Request(url, headers=headers)) 
            print("response:")
            print(response)

            # To avoid 'Too many requests'
            time.sleep(5)
            
            return BeautifulSoup(response.read(), 'html.parser')
        
        except HTTPError as e:
            print(f"HTTP error: {e.code} - {e.reason}")
            return None 
        except URLError as e:
            print(f"URL error: {e.reason}")
            return None

    '''
    tr = 'gsc_a_tr'
    td = 'gsc_a_y'
    a = 'gsc_a_at'
    '''
    def gather_articles_by_tr_td_a_name(tr, td, a):
        
        for class_name in bs.find_all('tr', class_ = tr):
        
            # Filter publication year
            year = int(class_name.find('td', class_ = td).span.get_text())
            if year < 2015:
                continue
        
            # Get publications
            publication_titles_since_2015.append(class_name.find('a').get_text())
        
            # Get links
            a_tag = class_name.find('a', class_ = a, href = True)
            if a_tag:
                publication_links_since_2015.append(urljoin(base_url, a_tag['href'])) 

    def get_coauthors_map():
        coauthors_map = {}
        for i, link in enumerate(publication_links_since_2015):
            bs = gather_bs_from_url(link)
        
            # Find authors section
            authors = bs.find('div', string=re.compile('Authors', re.IGNORECASE))
            if authors:
                authors_div = authors.find_next_sibling('div')
                coauthors_map[publication_titles_since_2015[i]] = [author.strip() for author in authors_div.get_text().split(',')
                                                                   if author.strip() != "Sean McGrath"]
        return coauthors_map


bs = webscraper.get_bs_from_url()

# SEARCH

import lxml
# from requests_html import HTMLSession
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin
from api.common.scraper import Scraper

class Parser(Scraper):
    def __init__(self, url):
        self.url = url
        self.count = None
        self.limit_exceeded = False
        self.patents = []
    
    def parse(self):
        html = self.get_html()
        
        soup = BeautifulSoup(html, 'lxml')
        base_url = 'http://www.ic.gc.ca/'
        
        # Check if there were any results
        div_results = soup.find('div', attrs={'class':'section'})
        if not div_results:
            # If none found, then return empty result
            self.count = '0'
            self.limit_exceeded = False
            self.patents = []
            return {'count':self.count, 'limit_exceeded':str(self.limit_exceeded), 'patents':self.patents}
            
        header_info = div_results.find('caption', attrs={'id':'SearchResults'})

        # Get count
        string_with_count = header_info.find('span', attrs={'id':'searchMessage'}) # Second strong tag contains results found string
        count = string_with_count.text
        #print(count)
        self.count = count.split()[0]
        
        # Toggle flag if display limit was exceeded
        # warning = header_info.find('div', attrs={'class':'color-attention'})
        #if warning:
        if int(self.count.split()[0].replace(',',''))>1000:
            self.limit_exceeded = True
        
        # Get patents
        table = soup.find('table', attrs={'id':'ResultsTable'})
        tbody = soup.find('tbody')
        # print(tbody.prettify())
        rows = tbody.find_all('tr')
        print(len(rows))
        for row in rows:
            columns = row.find_all('td')
            # Get patent number
            col2 = columns[1]
            patent_num = col2.get_text().strip()
            # Get patent title
            col3 = columns[2]
            patent_title = col3.get_text()
            # Get patent summary URL
            col2 = columns[1]
            patent_url_segment = col2.find('a').get('href') # Has base missing and query attached at end
            patent_url_raw = urljoin(base_url, patent_url_segment) # Join with base
            patent_url_parsed = urlparse(patent_url_raw) 
            patent_url = patent_url_parsed.scheme + "://" + patent_url_parsed.netloc + patent_url_parsed.path # Strip Query
            # Get Score
            col4 = columns[3]
            score = col4.get_text()
            # Compile data
            patent = [patent_num, patent_title, patent_url, score]
            self.patents.append(patent)
        
        # Create results dictionary
        results = {'count':self.count, 'limit_exceeded':str(self.limit_exceeded), 'patents':[]}
        for p in self.patents:
            d = {'number':p[0], 'title':p[1], 'link':p[2], 'score':p[3]}
            results['patents'].append(d)
            
        return results


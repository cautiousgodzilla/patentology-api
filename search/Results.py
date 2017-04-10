import lxml
import requests
from bs4 import BeautifulSoup
from urllib import urlopen
from urlparse import urlparse
from urlparse import urljoin

class Results(object):
    def __init__(self, url):
        self.url = url
        self.count = None
        self.limit_exceeded = False
        self.patents = []
    def get_html(self):
        html = urlopen(self.url).read()
        return html
        """
        try:
            headers = {'User-Agent': 'Patentology'}
            request = requests.get(self.url, headers=headers)
            if request.status_code == 200:
                html = request.content
                return html
            else:
                raise IOError
        except:
            raise IOError
        """
    def parse(self):
        html = self.get_html()
        soup = BeautifulSoup(html, 'lxml')
        base_url = 'http://www.ic.gc.ca/'
        
        # Check if there were any results
        div_results = soup.find('div', attrs={'class':'section'})
        if not div_results: # If none found or some other error, then return empty result
            self.count = "0"
            self.limit_exceeded = False
            self.patents = []
            return
        header_info = div_results.find('div', attrs={'class':'align-center'})
        # Get count
        string_with_count = header_info.find('strong') # Second strong tag contains results found string
        count = string_with_count.get_text().split()[0]
        self.count = count
        
        # Toggle flag if display limit was exceeded
        warning = header_info.find('div', attrs={'class':'color-attention'})
        if warning:
            self.limit_exceeded = True
        
        # Get patents
        table = soup.find('table', attrs={'id':'ResultsTable'})
        tbody = table.find('tbody')
        rows = tbody.find_all('tr')
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
            # Compile data
            patent = [patent_num, patent_title, patent_url]
            self.patents.append(patent)
    def results(self):
        self.parse()
        return (self.count, self.limit_exceeded, self.patents)

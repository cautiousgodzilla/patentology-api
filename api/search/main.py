# SEARCH
import sys
sys.path.append('..') 
from api.common.incoming import Request
from query import Query
from parser import Parser

def search_handler(arguments):
    payload = Request(arguments, endpoint='search').parse()
    url = Query(payload).generate_url()
    results_dict = Parser(url).parse()
    return results_dict

q = {'keyword': 'gesture', 'date-field': 'exam-request-date', 'date-start': '2021-08-01', 'date-end': '2022-07-31'}
print(search_handler(q))
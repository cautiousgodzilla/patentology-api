# INFO
import sys
sys.path.append('..') 
from api.common.incoming import Request
from parser import Parser
from query import Query

def info_handler(arguments):
    payload = Request(arguments, endpoint='info').parse()
    url = Query(payload).generate_url()
    print(url)
    results = Parser(url)
    results_dict = results.parse()
    return results_dict

x = {'id':'2894056'}
print(info_handler(x))
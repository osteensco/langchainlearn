from googleapiclient.discovery import build
from dotenv import load_dotenv
import pprint
import os



load_dotenv('token.env')

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
GOOGLE_CSE_ID = os.environ.get('GOOGLE_CSE_ID')
my_api_key = GOOGLE_API_KEY
my_cse_id = GOOGLE_CSE_ID

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

results = google_search(
    'stackoverflow site:en.wikipedia.org', my_api_key, my_cse_id, num=10)
for result in results:
    pprint.pprint(result)



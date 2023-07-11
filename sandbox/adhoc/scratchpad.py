import requests

r = requests.get('https://www.scottosteen.com/about/')

from bs4 import BeautifulSoup

soup = BeautifulSoup(r.content.decode('utf-8'), 'html.parser')

first_sentence = soup.find('p').get_text(strip=True)
import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.scottosteen.com/')

soup = BeautifulSoup(r.content.decode('utf-8'), 'html.parser')

first_sentence = soup.find('p').get_text(strip=True)
print(first_sentence)
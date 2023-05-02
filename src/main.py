import requests
from bs4 import BeautifulSoup

URL  = 'https://br.openfoodfacts.org/produto/7891000061190'
page = requests.get(URL).text

soup = BeautifulSoup(page, "html.parser")

table = soup.find(id="panel_nutrition_facts_table_content")
header = []
rows = []

for i, row in enumerate(table.find_all('tr')):
    if i == 0:
        header = [td.text.strip() for td in row.find_all('th')]
    else:
        rows.append([td.text.strip() for td in row.find_all('td')])

print(header)
for row in rows:
    print(row)
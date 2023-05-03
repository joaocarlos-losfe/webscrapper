import requests
from bs4 import BeautifulSoup
from pprint import pprint
from typing import Union
from fastapi import FastAPI, HTTPException

def get_product_data(bar_code: str):
    try:
        FINAL_URL  = f'https://br.openfoodfacts.org/produto/{bar_code}'
        page = requests.get(FINAL_URL).text

        soup = BeautifulSoup(page, "html.parser")

        product_image = soup.find(id="og_image").attrs['src']
        product_name = soup.find("title").text
        table = soup.find(id="panel_nutrition_facts_table_content")
        header = []
        rows = []

        for i, row in enumerate(table.find_all('tr')):
            if i == 0:
                header = [th.text.strip() for th in row.find_all('th')] #table header
            else:
                rows.append([td.text.strip() for td in row.find_all('td')]) #table data

        data = {}

        data["Nome"] = product_name
        data["Imagem"] = product_image
        data["Cabeçalho"] = header
        data["Informações nutricionais"] = []

        text_for_ignore = "Fruits‚ vegetables‚ nuts and rapeseed‚ walnut and olive oils (estimate from ingredients list analysis)"
      
        for row in rows:  
            if row[0] != text_for_ignore: 
                data["Informações nutricionais"].append(row)

        return data          

    except:
        print("falha")
        return None
    
app = FastAPI()

@app.get("/")
def read_root():
    return "🚀 server is running"

@app.get("/product/{bar_code}")
def find_product(bar_code: str):

    data = get_product_data(bar_code)

    if data is not None:
        return data
    
    raise HTTPException(status_code=404, detail="Produto não encontrado")

#data = get_product_data(bar_code='7891000061190')
#run: uvicorn main:app --reload
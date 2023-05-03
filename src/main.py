import requests
from bs4 import BeautifulSoup
from pprint import pprint
from typing import Union
from fastapi import FastAPI, HTTPException

def get_nutritional_information(bar_code: str):
    try:
        FINAL_URL  = f'https://br.openfoodfacts.org/produto/{bar_code}'
        page = requests.get(FINAL_URL).text

        soup = BeautifulSoup(page, "html.parser")

        product_name = soup.find("title").text
        table = soup.find(id="panel_nutrition_facts_table_content")
        header = []
        rows = []

        for i, row in enumerate(table.find_all('tr')):
            if i == 0:
                header = [td.text.strip() for td in row.find_all('th')]
            else:
                rows.append([td.text.strip() for td in row.find_all('td')])

        data = {}
    
        data["Nome do produto"] = product_name
        data["Informações nutricionais"] = {}

        text_for_ignore = "Fruits‚ vegetables‚ nuts and rapeseed‚ walnut and olive oils (estimate from ingredients list analysis)"
      
        for row in rows:  
            if row[0] != text_for_ignore: 
                data["Informações nutricionais"][row[0]] = { "quantidade": row[1], "%VD(*)": row[2] }

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

    data = get_nutritional_information(bar_code)

    if data is not None:
        return data
    
    raise HTTPException(status_code=404, detail="Produto não encontrado")

#data = get_nutritional_information(bar_code='7891000061190')
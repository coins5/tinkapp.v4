
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://resultados.latinka.com.pe/i.do?m=historico&t=0&s=41'
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.select('table')
    print(f"Number of tables found: {len(tables)}")
    if tables:
        # Try to parse the first table to see structure
        # Often the first table is layout, maybe the second is data.
        # Let's look for a table with many rows.
        for i, table in enumerate(tables):
            rows = table.find_all('tr')
            print(f"Table {i} has {len(rows)} rows")
            if len(rows) > 5:
                print(f"--- Table {i} Sample ---")
                for row in rows[:5]:
                    cols = row.find_all(['td', 'th'])
                    print([ele.text.strip() for ele in cols])
                print("---------------------")

except Exception as e:
    print(f"Error: {e}")

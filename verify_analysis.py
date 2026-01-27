
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime
from itertools import combinations

def fetch_tinka_history():
    url = 'https://resultados.latinka.com.pe/i.do?m=historico&t=0&s=41'
    try:
        print("Fetching data...")
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.select('table')
        if not tables or len(tables) < 2:
            return None
        data_table = tables[1]
        rows = data_table.find_all('tr')
        data = []
        for row in rows:
            cols = row.find_all(['td', 'th'])
            cols_text = [ele.text.strip() for ele in cols]
            if len(cols_text) >= 3:
                data.append(cols_text)
        if data:
            max_cols = max(len(x) for x in data)
            cols_names = ['Fecha', 'Sorteo', 'Jugada', 'Boliyapa', 'MegaBoliyapa', 'Ganadores', 'Extra1', 'Extra2'][:max_cols]
            df = pd.DataFrame(data, columns=cols_names)
            return df
        return pd.DataFrame()
    except Exception as e:
        print(f"Error: {e}")
        return None

def process_tinka_df(df):
    df = df.copy()
    try:
        df['Fecha_dt'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y', errors='coerce')
        df = df.dropna(subset=['Fecha_dt']).sort_values('Fecha_dt')
        df['Numeros'] = df['Jugada'].apply(lambda x: [int(n) for n in str(x).split() if n.isdigit()])
        df = df[df['Numeros'].apply(len) == 6]
        return df
    except Exception as e:
        print(f"Error processing: {e}")
        return df

def run_metrics(df):
    if df.empty:
        print("DataFrame is empty")
        return

    # Frequencies
    all_numbers = df['Numeros'].explode().astype(int)
    print("Frequencies calculated.")
    
    # Delays
    last_draw_date = df['Fecha_dt'].iloc[-1]
    min_b = int(all_numbers.min())
    max_b = 45 # Assuming
    possible_numbers = range(min_b, max_b + 1)
    delays = {}
    for num in possible_numbers:
        found = False
        for idx, row in df.sort_values('Fecha_dt', ascending=False).iterrows():
            if num in row['Numeros']:
                days_diff = (last_draw_date - row['Fecha_dt']).days
                delays[num] = days_diff
                found = True
                break
    print("Delays calculated.")

    # Pairs
    pair_counts = {}
    for nums in df['Numeros']:
        pairs = list(combinations(sorted(nums), 2))
        for p in pairs:
            pair_counts[p] = pair_counts.get(p, 0) + 1
    print("Pairs calculated.")

    # Parity
    def count_parity(nums):
        evens = sum(1 for n in nums if n % 2 == 0)
        return evens
    df['Paridad'] = df['Numeros'].apply(count_parity)
    print("Parity calculated.")

    # Sums
    df['Suma'] = df['Numeros'].apply(sum)
    print(f"Mean Sum: {df['Suma'].mean()}")

    # Jumps & Consecutive
    nums_sorted = np.sort(np.array(df['Numeros'].tolist()), axis=1)
    jumps_df = pd.DataFrame()
    for i in range(5):
        jumps_df[f'Jump_{i}'] = nums_sorted[:, i+1] - nums_sorted[:, i]
    
    print("Jumps calculated.")
    
    # Repeated Jumps
    repeated = 0
    for i in range(4):
        repeated += (jumps_df[f'Jump_{i}'] == jumps_df[f'Jump_{i+1}']).sum()
    print(f"Repeated consecutive jumps found: {repeated}")

    # Consecutive Numbers
    consecutives = (jumps_df == 1).sum().sum()
    print(f"Total consecutive pairs found: {consecutives}")

    # Endings
    all_numeros = df['Numeros'].explode().astype(int)
    endings = all_numeros % 10
    print(f"Endings distribution calculated. Most common ending: {endings.mode()[0]}")

if __name__ == "__main__":
    df = fetch_tinka_history()
    if df is not None:
        print(f"Fetched {len(df)} rows")
        df_clean = process_tinka_df(df)
        print(f"Cleaned {len(df_clean)} rows")
        run_metrics(df_clean)
        print("Verification Successful!")
    else:
        print("Failed to fetch data")

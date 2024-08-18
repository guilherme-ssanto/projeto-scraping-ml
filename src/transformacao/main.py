import pandas as pd
import sqlite3
from datetime import datetime 

df = pd.read_json('../data/data.jsonl', lines=True)

#setar o pandas para mostrar todas as colunas
pd.options.display.max_columns = None

#adicionar a coluna _source com um valor fixo
df['_source'] = "https://lista.mercadolivre.com.br/tenis/corrida-masculino"

#adicionar a coluna _data_coleta com a data e hora atuais
df['_data_coleta'] = datetime.now()

#tratar os valores para numeros
df['old_price_reais'] = df['old_price_reais'].fillna(0).astype(float)
df['old_price_centavos'] = df['old_price_centavos'].fillna(0).astype(float)
df['new_price_reais'] = df['new_price_reais'].fillna(0).astype(float)
df['new_price_centavos'] = df['new_price_centavos'].fillna(0).astype(float)
df['reviews_rating_number'] = df['reviews_rating_number'].fillna(0).astype(float)

#remover os parametros das colunas 'reviews_amount'
df['reviews_amount'] = df['reviews_amount'].str.replace('[\(\)]', '', regex=True)
df['reviews_amount'] = df['reviews_amount'].fillna(0).astype(int)

#tratar os precos como floats e calcular os valores totais
df['old_price'] = df['old_price_reais'] + df['old_price_centavos'] / 100
df['new_price'] = df['new_price_reais'] + df['new_price_centavos'] / 100

#remover as colunas antigas de preços 
df.drop(columns=['old_price_reais','old_price_centavos','new_price_reais','new_price_centavos'])

#Conectar ao banco de dados SQLite 
conn = sqlite3.connect('../data/quotes.db')

#salvar o df no bd sqlite
df.to_sql('mercadolivre_items', conn, if_exists='replace', index=False)

conn.close()

print(df.head())
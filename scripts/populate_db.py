import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Incarca variabilele din fisierul .env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# 1. Configurare conexiune MongoDB
# INLOCUIESTE AICI cu string-ul tau de conectare din Atlas
CONNECTION_STRING = os.getenv("MONGO_URI")

client = MongoClient(CONNECTION_STRING)
db = client['ProiectAutovit'] # Numele bazei de date
collection = db['Anunturi']   # Numele colectiei (tabelului)

# 2. Citire fisier CSV
import sys
if len(sys.argv) > 1:
    # Use filename provided in command line
    filename = sys.argv[1]
else:
    # Default fallback
    filename = 'date_autovit_test.csv'

print(f"Loading data from: {filename}")
csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', filename)
df = pd.read_csv(csv_path)

# 3. PRELUCRARE CRITICA (Data Type Casting)
# Chiar daca datele sunt "curate", CSV-ul le citeste uneori ca text.
# Fortam conversia in numere pentru filtrare corecta (ex: Pret < 10000).

# Convertim in intregi (gestionam eventualele erori daca fisierul e gol)
try:
    df['An_fabricatie'] = df['An_fabricatie'].astype(int)
    df['Pret'] = df['Pret'].astype(int)
    df['Km'] = df['Km'].astype(int)
    df['Putere'] = df['Putere'].astype(int)
    df['Capacitate_Cilindrica'] = df['Capacitate_Cilindrica'].astype(int)
except Exception as e:
    print(f"Eroare la conversia datelor: {e}")

# 4. Transformare in dictionar pentru MongoDB
data_to_insert = df.to_dict('records')

# 5. Inserare in baza de date
# Golim colectia inainte, ca sa nu avem duplicate cand testam scriptul de mai multe ori
collection.delete_many({}) 
result = collection.insert_many(data_to_insert)

print(f"Au fost introduse {len(result.inserted_ids)} anunturi in baza de date MongoDB!")
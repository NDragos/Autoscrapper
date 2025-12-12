import pandas as pd
from pymongo import MongoClient

# 1. Configurare conexiune MongoDB
CONNECTION_STRING = "mongodb+srv://mario:Jt.uipT19VRLa7m@cluster0.rvoavsc.mongodb.net/?appName=Cluster0"

try:
    client = MongoClient(CONNECTION_STRING)
    db = client['ProiectAutovit']
    collection = db['Anunturi']

    # Test conexiune
    client.admin.command('ping')
    print("Conexiune la MongoDB reusita!")
except Exception as e:
    print(f"Eroare grava la conectare: {e}")
    exit()

# 2. Citire fisier CSV
# Specificam ca 'N/A' trebuie tratat ca valoare lipsa (NaN)
try:
    df = pd.read_csv('date_autovit_test.csv', na_values=['N/A', 'null', 'None', '-'])
except Exception as e:
    print(f"Nu am putut citi fisierul CSV: {e}")
    exit()

# 3. PRELUCRARE SI CURATARE DATE

# Lista coloanelor care TREBUIE sa fie numerice
coloane_numerice = ['An_fabricatie', 'Pret', 'Km', 'Putere', 'Capacitate_Cilindrica']

for col in coloane_numerice:
    # Pasul A: Fortam conversia in numere. Daca da eroare (ex: text ciudat), pune NaN
    df[col] = pd.to_numeric(df[col], errors='coerce')

    # Pasul B: Umplem valorile lipsa (NaN) cu 0
    df[col] = df[col].fillna(0)

    # Pasul C: Convertim in Integer (Numar intreg, fara virgula)
    df[col] = df[col].astype(int)

print("Datele au fost curatate si convertite in numere (int)!")

# 4. Inserare in MongoDB
# Stergem tot ce era vechi ca sa nu amestecam date bune cu date proaste
x = collection.delete_many({})
print(f"Am sters {x.deleted_count} anunturi vechi (curatare baza).")

# Transformam in dictionar si inseram
data_to_insert = df.to_dict('records')

if len(data_to_insert) > 0:
    result = collection.insert_many(data_to_insert)
    print(f"SUCCES: Au fost introduse {len(result.inserted_ids)} anunturi corecte in MongoDB!")
else:
    print("Nu exista date de introdus.")
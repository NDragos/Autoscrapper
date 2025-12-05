from flask import Flask, request, jsonify
from flask_cors import CORS
from backend_autovit import AutovitBackend

# --- CONFIGURARE ---
app = Flask(__name__)
# Permitem oricarei pagini web sa acceseze acest server (pentru dezvoltare)
CORS(app) 

# Conectarea la baza de date (Initializeaza clasa ta)
# Inlocuieste cu string-ul tau real
CONNECTION_STRING = "mongodb+srv://mario:Jt.uipT19VRLa7m@cluster0.rvoavsc.mongodb.net/?appName=Cluster0"
backend = AutovitBackend(CONNECTION_STRING)

# --- ENDPOINT 1: POPULARE DROPDOWN-URI ---
# Site-ul va cere: "Da-mi lista de Marci" sau "Da-mi Modelele pentru marca X"
# URL apelat de site: /api/optiuni?categorie=Marca
# URL apelat de site: /api/optiuni?categorie=Model&marca_parinte=BMW
@app.route('/api/optiuni', methods=['GET'])
def obtine_optiuni():
    try:
        # 1. Citim ce categorie vrea site-ul (Marca, Model, Combustibil, etc.)
        categorie_ceruta = request.args.get('categorie')
        
        # 2. Verificam daca exista un filtru parinte (ex: Vrea modele, dar doar pentru o Marca anume)
        marca_parinte = request.args.get('marca_parinte')
        filtru_parinte = None
        
        if marca_parinte:
            filtru_parinte = {"Marca": marca_parinte}

        # 3. Folosim functia ta din backend_autovit.py
        lista_optiuni = backend.get_optiuni_filtru(categorie_ceruta, filtru_parinte)
        
        # 4. Trimitem lista inapoi catre site in format JSON
        return jsonify({
            "succes": True,
            "date": lista_optiuni
        })

    except Exception as e:
        return jsonify({"succes": False, "eroare": str(e)}), 500


# --- ENDPOINT 2: FILTRARE SI CAUTARE ---
# Site-ul trimite un JSON cu toate filtrele selectate de utilizator
# URL apelat de site: /api/cauta
@app.route('/api/cauta', methods=['POST'])
def cauta_masini():
    try:
        # 1. Primim datele din site (format JSON)
        # Acestea vor arata exact ca dictionarul python din exemplul anterior:
        # {"Marca": "...", "Pret_max": 10000, "Combustibil": "..."}
        filtre_primite = request.json
        
        print(f"Am primit o cerere de filtrare: {filtre_primite}") # Pentru debug in consola ta

        # 2. Folosim functia ta de cautare complexa
        rezultate = backend.cauta_anunturi(filtre_primite)

        # 3. Returnam lista de masini gasite
        return jsonify({
            "succes": True,
            "numar_rezultate": len(rezultate),
            "rezultate": rezultate
        })

    except Exception as e:
        return jsonify({"succes": False, "eroare": str(e)}), 500

# --- PORNIRE SERVER ---
if __name__ == '__main__':
    # Serverul va rula pe portul 5000
    print("Serverul Backend a pornit! Astept cereri de la site...")
    app.run(debug=True, port=5000)
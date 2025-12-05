from flask import Flask, request, jsonify
from flask_cors import CORS
from backend_autovit import AutovitBackend

# --- Configurare Server ---
app = Flask(__name__)
CORS(app) 

# Configurare conexiune MongoDB
# TODO: Pentru productie, utilizati variabile de mediu pentru credentiale.
CONNECTION_STRING = "mongodb+srv://mario:Jt.uipT19VRLa7m@cluster0.rvoavsc.mongodb.net/?appName=Cluster0"
backend = AutovitBackend(CONNECTION_STRING)

# --- Endpoint-uri API ---

@app.route('/api/optiuni', methods=['GET'])
def obtine_optiuni():
    """ 
    GET: Returneaza optiunile pentru dropdown-uri.
    Params: categorie (obligatoriu), marca_parinte (optional)
    """
    try:
        categorie_ceruta = request.args.get('categorie')
        marca_parinte = request.args.get('marca_parinte')
        
        filtru_parinte = {"Marca": marca_parinte} if marca_parinte else None
        
        lista_optiuni = backend.get_optiuni_filtru(categorie_ceruta, filtru_parinte)
        
        return jsonify({
            "succes": True,
            "date": lista_optiuni
        })

    except Exception as e:
        return jsonify({"succes": False, "eroare": str(e)}), 500


@app.route('/api/cauta', methods=['POST'])
def cauta_masini():
    """ 
    POST: Primeste filtrele in format JSON si returneaza lista de masini.
    Body Ex: {"Marca": "BMW", "Pret_max": 20000}
    """
    try:
        filtre_primite = request.json
        print(f"[Server] Request filtrare primit: {filtre_primite}") 

        rezultate = backend.cauta_anunturi(filtre_primite)

        return jsonify({
            "succes": True,
            "numar_rezultate": len(rezultate),
            "rezultate": rezultate
        })

    except Exception as e:
        return jsonify({"succes": False, "eroare": str(e)}), 500

if __name__ == '__main__':
    print("Serverul Backend a pornit pe portul 5000.")
    app.run(debug=True, port=5000)
from pymongo import MongoClient

class AutovitBackend:
    def __init__(self, connection_string):
        # Conectarea la baza de date
        self.client = MongoClient(connection_string)
        self.db = self.client['ProiectAutovit']
        self.collection = self.db['Anunturi']

    def get_optiuni_filtru(self, categorie, filtru_parinte=None):
        """
        Returneaza lista de optiuni unice pentru meniurile dropdown.
        Ex: Daca categorie="Marca", returneaza ["BMW", "Audi", ...]
        
        filtru_parinte: Ajuta la dependente. 
        Ex: Daca vrei Modele, dar doar pentru Marca="BMW".
        """
        query = {}
        if filtru_parinte:
            # Ex: filtru_parinte = {"Marca": "BMW"}
            query = filtru_parinte

        # Returneaza valorile distincte gasite in baza de date
        # Ex: Daca in DB avem doar 3 marci, doar alea 3 vor fi returnate.
        try:
            return sorted(self.collection.distinct(categorie, query))
        except Exception as e:
            print(f"Eroare la extragerea optiunilor: {e}")
            return []

    def cauta_anunturi(self, filtre_user):
        """
        Construieste query-ul complex pentru MongoDB bazat pe ce a completat utilizatorul.
        
        filtre_user: Un dictionar cu ce a completat omul pe site.
        Cheile trebuie sa fie specifice:
        - Pentru text exact: 'Marca', 'Combustibil', etc.
        - Pentru intervale: 'Pret_min', 'Pret_max', 'An_min', 'An_max', etc.
        """
        query = {}

        # 1. FILTRE CATEGORIALE (Meniuri Dropdown)
        # Verificam daca utilizatorul a selectat ceva pentru fiecare categorie
        campuri_text = ['Marca', 'Model', 'Combustibil', 'Tip_cutie_viteze', 'Tip_Caroserie']
        
        for camp in campuri_text:
            if camp in filtre_user and filtre_user[camp]: # Daca exista si nu e gol
                query[camp] = filtre_user[camp]

        # 2. FILTRE NUMERICE (Intervale: De la - Pana la)
        # Lista de campuri care au intervale numerice
        campuri_numerice = ['Pret', 'An_fabricatie', 'Km', 'Putere', 'Capacitate_Cilindrica']

        for camp in campuri_numerice:
            min_key = f"{camp}_min" # ex: Pret_min
            max_key = f"{camp}_max" # ex: Pret_max
            
            val_min = filtre_user.get(min_key)
            val_max = filtre_user.get(max_key)

            # Logica pentru MongoDB Range Query ($gte = min, $lte = max)
            interval_query = {}
            
            if val_min: # Daca utilizatorul a completat "De la"
                interval_query['$gte'] = int(val_min)
            
            if val_max: # Daca utilizatorul a completat "Pana la"
                interval_query['$lte'] = int(val_max)

            # Daca am gasit macar o limita (min sau max), adaugam in query
            if interval_query:
                query[camp] = interval_query

        # Executam cautarea si returnam doar campurile necesare
        # Returnam Link-ul si datele esentiale pentru afisare scurta
        rezultate = self.collection.find(query, {'_id': 0})
        
        return list(rezultate)
from pymongo import MongoClient

class AutovitBackend:
    def __init__(self, connection_string):
        """ Initializare conexiune la MongoDB Atlas. """
        self.client = MongoClient(connection_string)
        self.db = self.client['ProiectAutovit']
        self.collection = self.db['Anunturi']

    def get_optiuni_filtru(self, categorie, filtru_parinte=None):
        """ 
        Returneaza lista de valori unice pentru o categorie (ex: Marci), 
        aplicand optional un filtru parinte (ex: Modele doar pentru BMW).
        """
        query = {}
        if filtru_parinte:
            query = filtru_parinte

        try:
            return sorted(self.collection.distinct(categorie, query))
        except Exception as e:
            print(f"[Backend] Eroare la extragerea optiunilor: {e}")
            return []

    def cauta_anunturi(self, filtre_user):
        """ 
        Construieste query-ul dinamic si returneaza lista de anunturi 
        care respecta criteriile (text exact sau intervale numerice).
        """
        query = {}

        # 1. Filtre Categoriale (Exact Match)
        campuri_text = ['Marca', 'Model', 'Combustibil', 'Tip_cutie_viteze', 'Tip_Caroserie']
        for camp in campuri_text:
            if camp in filtre_user and filtre_user[camp]:
                query[camp] = filtre_user[camp]

        # 2. Filtre Numerice (Range Query)
        campuri_numerice = ['Pret', 'An_fabricatie', 'Km', 'Putere', 'Capacitate_Cilindrica']
        
        for camp in campuri_numerice:
            min_key = f"{camp}_min"
            max_key = f"{camp}_max"
            
            val_min = filtre_user.get(min_key)
            val_max = filtre_user.get(max_key)

            interval_query = {}
            
            # Validare: ne asiguram ca valoarea nu e None si nu e string gol
            if val_min and str(val_min).strip() != "":
                interval_query['$gte'] = int(val_min)
            
            if val_max and str(val_max).strip() != "":
                interval_query['$lte'] = int(val_max)

            if interval_query:
                query[camp] = interval_query

        # Returnam rezultatele fara campul intern _id
        try:
            rezultate = self.collection.find(query, {'_id': 0})
            return list(rezultate)
        except Exception as e:
            print(f"[Backend] Eroare la cautare: {e}")
            return []
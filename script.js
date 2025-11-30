const API_URL = "http://127.0.0.1:5000/api";

// 1. Executat cand pagina se incarca
window.onload = async () => {
    // Populam dropdown-urile initiale
    await populeazaDropdown('Marca', 'Marca');
    await populeazaDropdown('Combustibil', 'Combustibil');
    await populeazaDropdown('Tip_cutie_viteze', 'Tip_cutie_viteze');
    await populeazaDropdown('Tip_Caroserie', 'Tip_Caroserie');
};

// 2. Functie generica pentru a cere optiuni de la Python
async function populeazaDropdown(categorie, elementId, parinte = null) {
    let url = `${API_URL}/optiuni?categorie=${categorie}`;
    if (parinte) {
        url += `&marca_parinte=${parinte}`;
    }

    try {
        const response = await fetch(url);
        const data = await response.json();
        
        const select = document.getElementById(elementId);
        // Pastram doar prima optiune (cea implicita)
        select.innerHTML = select.options[0].outerHTML;

        if (data.succes) {
            data.date.forEach(optiune => {
                const option = document.createElement('option');
                option.value = optiune;
                option.textContent = optiune;
                select.appendChild(option);
            });
        }
    } catch (err) {
        console.error("Eroare la incarcare optiuni:", err);
    }
}

// 3. Cand se schimba Marca -> Incarca Modelele
async function incarcaModele() {
    const marcaSelectata = document.getElementById('Marca').value;
    const modelSelect = document.getElementById('Model');

    if (!marcaSelectata) {
        modelSelect.disabled = true;
        modelSelect.innerHTML = '<option value="">Alege întâi Marca</option>';
        return;
    }

    modelSelect.disabled = false;
    await populeazaDropdown('Model', 'Model', marcaSelectata);
}

// 4. Functia de CAUTARE (Trimite filtrele la Python)
async function cautaAnunturi() {
    const btn = document.querySelector('.btn-search');
    const loading = document.getElementById('loading');
    const container = document.getElementById('rezultate-container');
    
    // UI Update
    btn.disabled = true;
    loading.style.display = 'block';
    container.innerHTML = '';

    // Colectam datele din inputuri
    // Luam doar ce a completat utilizatorul (ignoram campurile goale)
    const filtre = {};
    const ids = [
        'Marca', 'Model', 'Combustibil', 'Tip_cutie_viteze', 'Tip_Caroserie',
        'Pret_min', 'Pret_max', 'An_fabricatie_min', 'An_fabricatie_max',
        'Km_min', 'Km_max', 'Putere_min', 'Putere_max', 
        'Capacitate_Cilindrica_min', 'Capacitate_Cilindrica_max'
    ];

    ids.forEach(id => {
        const valoare = document.getElementById(id).value;
        if (valoare) {
            filtre[id] = valoare;
        }
    });

    try {
        // Trimitem POST catre server
        const response = await fetch(`${API_URL}/cauta`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(filtre)
        });

        const data = await response.json();

        // Afisam rezultatele
        if (data.succes && data.rezultate.length > 0) {
            data.rezultate.forEach(masina => {
                const card = `
                    <div class="car-card">
                        <h3>${masina.Marca} ${masina.Model}</h3>
                        <span class="price">${masina.Pret} EUR</span>
                        <div class="details">
                            <p>📅 An: ${masina.An_fabricatie}</p>
                            <p>🚗 ${masina.Combustibil} | ${masina.Tip_cutie_viteze}</p>
                            <p>🛣️ ${masina.Km} KM</p>
                            <p>⚡ ${masina.Putere} CP | ${masina.Capacitate_Cilindrica} cm3</p>
                        </div>
                        <a href="${masina.Link}" target="_blank" class="car-link">Vezi Anunț pe Autovit</a>
                    </div>
                `;
                container.innerHTML += card;
            });
        } else {
            container.innerHTML = '<p style="grid-column: 1/-1; text-align: center;">Nu s-au găsit anunțuri conform filtrelor.</p>';
        }

    } catch (err) {
        console.error(err);
        container.innerHTML = '<p style="color:red">Eroare de conexiune cu serverul.</p>';
    } finally {
        btn.disabled = false;
        loading.style.display = 'none';
    }
}
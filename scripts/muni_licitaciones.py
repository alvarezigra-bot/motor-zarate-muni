import os
import requests
from bs4 import BeautifulSoup
import json

def scrap_licitaciones():
    folder = 'api_muni/licitaciones'
    os.makedirs(folder, exist_ok=True)
    
    # URL de transparencia y licitaciones
    url_licitaciones = "https://zarate.gob.ar/licitaciones/"
    
    print("💰 INICIANDO MOTOR DE LICITACIONES Y OBRAS 2026...")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url_licitaciones, headers=headers, timeout=20)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Buscamos bloques de licitaciones
        licitaciones = soup.find_all(['tr', 'div', 'p'], string=lambda text: text and ("202" in text or "Licitación" in text))
        
        count = 0
        for lic in licitaciones:
            texto = lic.get_text(strip=True)
            if len(texto) > 10: # Evitar ruidos
                count += 1
                lic_data = {
                    "id": count,
                    "descripcion": texto,
                    "entorno": "Zárate 2026",
                    "estado": "En Proceso de Triangulación",
                    "url_origen": url_licitaciones
                }
                with open(f"{folder}/licitacion_{count}.json", 'w', encoding='utf-8') as f:
                    json.dump(lic_data, f, indent=4, ensure_ascii=False)
                
        print(f"✅ Se mapearon {count} movimientos de licitaciones.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    scrap_licitaciones()

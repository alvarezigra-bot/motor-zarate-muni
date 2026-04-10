import os
import requests
from bs4 import BeautifulSoup
import json
import time

def scrap_muni():
    folder = 'api_muni/boletines'
    os.makedirs(folder, exist_ok=True)
    
    # URL de Boletines Oficiales de Zárate
    url_boletines = "https://zarate.gob.ar/boletin-oficial/"
    
    print("🛰️ INICIANDO MOTOR MUNI: Extrayendo Boletines Oficiales 2026...")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url_boletines, headers=headers, timeout=20)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Buscamos los links a los boletines (suelen ser archivos .pdf o links a SIBOM)
        links = soup.find_all('a', href=True)
        count = 0
        
        for link in links:
            href = link['href']
            if ".pdf" in href or "sibom" in href:
                count += 1
                boletin_data = {
                    "id": count,
                    "url": href,
                    "titulo": link.get_text(strip=True) or f"Boletín {count}",
                    "entidad": "Municipalidad de Zárate",
                    "estado": "Descargado para Triangulación",
                    "fecha_scaneo": "2026-04-10"
                }
                
                with open(f"{folder}/boletin_{count}.json", 'w', encoding='utf-8') as f:
                    json.dump(boletin_data, f, indent=4, ensure_ascii=False)
                
        print(f"✅ Se detectaron {count} documentos oficiales.")

    except Exception as e:
        print(f"❌ Error conectando a la web municipal: {e}")

if __name__ == "__main__":
    scrap_muni()

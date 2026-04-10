import os
import requests
from bs4 import BeautifulSoup
import json
import re

def deep_scan_finance():
    # Carpetas para los datos específicos
    folders = ['api_muni/finanzas', 'api_muni/obras_detalle']
    for f in folders: os.makedirs(f, exist_ok=True)
    
    # Fuentes críticas para triangular
    targets = {
        "licitaciones": "https://zarate.gob.ar/licitaciones/",
        "obras": "https://zarate.gob.ar/obras-en-marcha/",
        "aguas": "https://zarate.gob.ar/aguas-de-zarate/"
    }
    
    print("🔍 INICIANDO PROFUNDIZACIÓN PARA TRIANGULAR...")

    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for sector, url in targets.items():
        try:
            print(f"📡 Escaneando sector: {sector}")
            res = requests.get(url, headers=headers, timeout=20)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Buscamos patrones de montos (ej: $1.000.000)
            montos = re.findall(r'\$\s?(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)', soup.get_text())
            
            # Buscamos CUITs potenciales (XX-XXXXXXXX-X)
            cuits = re.findall(r'\b\d{2}-\d{8}-\d{1}\b', soup.get_text())

            data_sector = {
                "sector": sector,
                "url_fuente": url,
                "montos_detectados": montos,
                "cuits_detectados": cuits,
                "hallazgos": soup.get_text()[:500].replace('\n', ' '), # Un resumen del texto
                "alerta_triangulacion": len(montos) > 0
            }

            with open(f'api_muni/finanzas/{sector}.json', 'w', encoding='utf-8') as f:
                json.dump(data_sector, f, indent=4, ensure_ascii=False)
                
        except Exception as e:
            print(f"❌ Error en {sector}: {e}")

    print("✅ Finanzas y montos mapeados para el cruce.")

if __name__ == "__main__":
    deep_scan_finance()

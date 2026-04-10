import os
import requests
from bs4 import BeautifulSoup
import json
import time

def scrap_muni_historico():
    # Carpetas para organizar por año
    base_folder = 'api_muni/boletines'
    os.makedirs(base_folder, exist_ok=True)
    
    # URL base del SIBOM de Zárate (donde suelen estar los archivos)
    # Vamos a probar un rango extendido
    print("🕰️ INICIANDO MOTOR HISTÓRICO MUNICIPAL...")

    # Intentaremos capturar por patrones de URL comunes en municipios
    urls_semilla = [
        "https://zarate.gob.ar/boletin-oficial/",
        "https://zarate.gob.ar/boletines-anteriores/"
    ]

    count = 0
    headers = {'User-Agent': 'Mozilla/5.0'}

    for url in urls_semilla:
        try:
            res = requests.get(url, headers=headers, timeout=20)
            soup = BeautifulSoup(res.text, 'html.parser')
            links = soup.find_all('a', href=True)

            for link in links:
                href = link['href']
                if ".pdf" in href:
                    count += 1
                    # Extraer año del link si es posible (ej: boletin_2023.pdf)
                    # Si no, lo dejamos como histórico
                    nombre_archivo = href.split('/')[-1]
                    
                    boletin_data = {
                        "id": count,
                        "archivo": nombre_archivo,
                        "url": href,
                        "titulo": link.get_text(strip=True) or nombre_archivo,
                        "fuente": "SIBOM / Web Municipal",
                        "fecha_scaneo": "2026-04-10"
                    }

                    with open(f"{base_folder}/historico_{count}.json", 'w', encoding='utf-8') as f:
                        json.dump(boletin_data, f, indent=4, ensure_ascii=False)
                    print(f"📦 Mapeado: {nombre_archivo}", end="\r")

        except Exception as e:
            print(f"\n❌ Error en {url}: {e}")

    print(f"\n✅ Total de documentos municipales mapeados: {count}")

if __name__ == "__main__":
    scrap_muni_historico()

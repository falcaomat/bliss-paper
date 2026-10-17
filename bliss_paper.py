#!/usr/bin/env python3
"""

Bliss Paper - Programa que muda wallpaper Bliss conforme o clima da sua região. 

Utiliza somente biblioteca padrão do Python (sem pip install)

Uso:
  python3 bliss_paper.py     # loop, atualiza a cada 15 min
  python3 bliss_paper.py -u  # atualiza uma vez e sai

"""
from datetime import datetime
import ctypes
import json
import os
import platform
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

# Base (Localização + Tempo)
LATITUDE = None     # ex: -22.85  (None = detectar pelo IP)
LONGITUDE = None    # ex: -43.05  (None = detectar pelo IP)
INTERVALO_MINUTO = 15
MINUTOS_POR_DO_SOL = 30
PASTA = Path(__file__).resolve().parent / "wallpapers"

# Numeração (WMO) Organização Meteorológica Mundial
CHUVA = {55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82}
NUBLADO = {3, 45, 48, 51, 53}
NEVE = {71, 73}
NEVE_FORTE = {75, 85, 86}
NEVE_GRAO = {77} 
TEMPESTADE = {95, 96, 99}

# Qualquer outro número (0 e 1) = Sol


def http_json(url):
    with urllib.request.urlopen(url, timeout=15) as r:
        return json.load(r)


def obter_localizacao():
    if LATITUDE is not None and LONGITUDE is not None:
        return LATITUDE, LONGITUDE
    dados_local = http_json("http://ip-api.com/json/?fields=lat,lon,status")
    if dados_local.get("status") != "success":
        raise RuntimeError("Não detectei a localização. Defina LATITUDE e LONGITUDE.")
    return dados_local["lat"], dados_local["lon"]


def obter_clima():
    lat, lon = obter_localizacao() # Localização

    url = ("https://api.open-meteo.com/v1/forecast"
           f"?latitude={lat}&longitude={lon}" # 1. Verifica Latitude e Longitude 
           "&current=weather_code,is_day" # 2. Pede o clima e vê se é dia ou noite
           "&daily=sunset&timezone=auto&forecast_days=1") # 3. Pede o horário que o sol se põe, vem fuso-horário atual e somente hoje. 
    
    dados_clima = http_json(url) # 4. Faz o pedido e guarda resposta
    momento_atual = dados_clima["current"]
    
    codigo = momento_atual["weather_code"] # 5. Entrega a numeração da tabela WMO

    agora = datetime.fromisoformat(momento_atual["time"])
    por_do_sol = datetime.fromisoformat(dados_clima["daily"]["sunset"][0])
    minutos_restantes = (por_do_sol - agora).total_seconds() / 60
    
    if minutos_restantes >= 0:
        horas = int (minutos_restantes // 60)
        minutos = int (minutos_restantes % 60)
        print(f"Faltam {horas}h {minutos:02d} minutos para o pôr do sol") # Confere quanto tempo para o por do sol
    else: 
        print("O sol já se pôs hoje")
    
    if codigo in TEMPESTADE:
        return "tempestade", codigo
    if not momento_atual["is_day"] or minutos_restantes < 0: # 6. Verifica se é dia ou noite
        if codigo in CHUVA:
            return "noite-chuva", codigo
        return "noite", codigo
    if codigo in CHUVA:
        return "chuva", codigo

    if codigo in NUBLADO:
        return "nublado", codigo
    if 0 <= minutos_restantes <= MINUTOS_POR_DO_SOL:
            return "por-do-sol", codigo
    if codigo in NEVE:
        return "neve", codigo
    if codigo in NEVE_GRAO:
        return "neve-grao", codigo
    if codigo in NEVE_FORTE:
        return "neve-forte", codigo
    return "sol", codigo


def achar_imagem(nome):
    p = PASTA / f"{nome}.jpg"
    if p.exists():
        return p
    return None


def definir_wallpaper(caminho):
    caminho = str(caminho)
    sistema = platform.system()

    if sistema == "Windows":
        ctypes.windll.user32.SystemParametersInfoW(20, 0, caminho, 3)
        return

    if sistema == "Linux":
        uri = "file://" + caminho
        desk = os.environ.get("XDG_CURRENT_DESKTOP", "").upper()

        if any(d in desk for d in ("GNOME", "UNITY", "PANTHEON", "BUDGIE", "ZORIN")) \
                and shutil.which("gsettings"):
            for chave in ("picture-uri", "picture-uri-dark"):
                subprocess.run(["gsettings", "set", "org.gnome.desktop.background", chave, uri])
        elif "CINNAMON" in desk and shutil.which("gsettings"):
            subprocess.run(["gsettings", "set", "org.cinnamon.desktop.background", "picture-uri", uri])
        elif "MATE" in desk and shutil.which("gsettings"):
            subprocess.run(["gsettings", "set", "org.mate.background", "picture-filename", caminho])
        elif "KDE" in desk and shutil.which("plasma-apply-wallpaperimage"):
            subprocess.run(["plasma-apply-wallpaperimage", caminho])
        elif "XFCE" in desk and shutil.which("xfconf-query"):
            props = subprocess.run(["xfconf-query", "-c", "xfce4-desktop", "-l"],
                                   capture_output=True, text=True).stdout.splitlines()
            for p in props:
                if p.endswith("last-image"):
                    subprocess.run(["xfconf-query", "-c", "xfce4-desktop", "-p", p, "-s", caminho])
        elif shutil.which("feh"):
            subprocess.run(["feh", "--bg-fill", caminho])
        else:
            raise RuntimeError(f"Desktop '{desk}' não suportado. Instale o 'feh'.")
        return

    raise RuntimeError(f"Sistema '{sistema}' não suportado.")


def atualizar(ultimo=[None]):
    tipo, codigo = obter_clima()
    img = achar_imagem(tipo)
    print(f"Clima (código {codigo}) -> {tipo}")
    if img is None:
        print(f"Faltando a imagem '{tipo}' em {PASTA}")
        return
    if img != ultimo[0]:
        definir_wallpaper(img)
        ultimo[0] = img
        print(f"Wallpaper: {img.name}")


def main():
    PASTA.mkdir(exist_ok=True)
    uma_vez = "-u" in sys.argv
    while True:
        try:
            atualizar()
        except Exception as e:
            print(f"Erro: {e}")
        if uma_vez:
            break
        time.sleep(INTERVALO_MINUTO * 60)


if __name__ == "__main__":
    main()

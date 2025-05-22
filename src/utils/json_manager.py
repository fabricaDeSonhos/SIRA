import json
import os

def ler_json(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        return []
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def escrever_json(caminho_arquivo, dados):
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

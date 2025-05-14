import hashlib
import os
import zipfile


def compactar_csv_para_zip(nome_entidade: str) -> str:
    caminho_csv = f"data/{nome_entidade}.csv"
    caminho_zip = f"data/{nome_entidade}.zip"

    if not os.path.exists(caminho_csv):
        raise FileNotFoundError(f"Arquivo {caminho_csv} não encontrado.")

    with zipfile.ZipFile(caminho_zip, "w") as zipf:
        zipf.write(caminho_csv, arcname=f"{nome_entidade}.csv")
    return caminho_zip


def calcular_hash_csv(entidade: str) -> str:
    caminho_csv = f"data/{entidade}.csv"

    try:
        with open(caminho_csv, "rb") as f:
            conteudo = f.read()
            hash_obj = hashlib.sha256(conteudo)
            return hash_obj.hexdigest()
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo {caminho_csv} não encontrado.")

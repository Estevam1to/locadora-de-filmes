import csv
import os
import xml.etree.ElementTree as ET


def converter_csv_para_xml(entidade: str) -> str:
    caminho_csv = f"data/{entidade}.csv"
    caminho_xml = f"data/{entidade}.xml"

    if not os.path.exists(caminho_csv):
        raise FileNotFoundError(f"Arquivo {caminho_csv} não encontrado.")

    with open(caminho_csv, mode="r", encoding="utf-8") as csvfile:
        leitor = csv.DictReader(csvfile)
        raiz = ET.Element(entidade)

        for linha in leitor:
            item = ET.SubElement(
                raiz, entidade[:-1]
            )  # singulariza, ex: clientes → cliente
            for chave, valor in linha.items():
                campo = ET.SubElement(item, chave)
                campo.text = valor

    arvore = ET.ElementTree(raiz)
    arvore.write(caminho_xml, encoding="utf-8", xml_declaration=True)

    return caminho_xml

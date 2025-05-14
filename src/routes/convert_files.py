from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from config.logs import registrar_log
from utils.csv_utils import calcular_hash_csv, compactar_csv_para_zip
from utils.xml_utils import converter_csv_para_xml

router = APIRouter()


@router.get("/compactar/{entidade}")
def compactar_csv(entidade: str):
    registrar_log(f"Solicitação para compactar arquivo CSV: {entidade}")
    try:
        zip_path = compactar_csv_para_zip(entidade)
        registrar_log(f"Arquivo CSV compactado com sucesso: {entidade}")
        return FileResponse(
            zip_path, media_type="application/zip", filename=f"{entidade}.zip"
        )
    except FileNotFoundError:
        registrar_log(f"Arquivo CSV não encontrado: {entidade}", nivel="error")
        raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado")


@router.get("/hash/{entidade}")
def obter_hash_csv(entidade: str):
    registrar_log(f"Solicitação para calcular hash do arquivo CSV: {entidade}")
    try:
        hash_valor = calcular_hash_csv(entidade)
        registrar_log(f"Hash calculado com sucesso para: {entidade}")
        return {"entidade": entidade, "hash": hash_valor}
    except FileNotFoundError:
        registrar_log(
            f"Arquivo CSV não encontrado para hash: {entidade}", nivel="error"
        )
        raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado")


@router.get("/converter/{entidade}/xml")
def converter_para_xml(entidade: str):
    registrar_log(f"Solicitação para converter CSV para XML: {entidade}")
    try:
        xml_path = converter_csv_para_xml(entidade)
        registrar_log(f"Conversão para XML concluída com sucesso: {entidade}")
        return FileResponse(
            xml_path, media_type="application/xml", filename=f"{entidade}.xml"
        )
    except FileNotFoundError:
        registrar_log(
            f"Arquivo CSV não encontrado para conversão: {entidade}", nivel="error"
        )
        raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado")

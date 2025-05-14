import csv
import os
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from config.logs import logger, registrar_log
from schemas.cliente import Cliente

router = APIRouter()

CLIENTES_CSV = "data/clientes.csv"

def read_clientes() -> List[Cliente]:
    if not os.path.exists(CLIENTES_CSV):
        return []
    with open(CLIENTES_CSV, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [Cliente(**row) for row in reader]

def write_clientes(clientes: List[Cliente]):
    with open(CLIENTES_CSV, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=Cliente.model_fields.keys())
        writer.writeheader()
        for cliente in clientes:
            writer.writerow(cliente.dict())

def get_cliente_by_id(cliente_id: int) -> Optional[Cliente]:
    return next((c for c in read_clientes() if int(c.id) == cliente_id), None)

def create_cliente(cliente: Cliente):
    clientes = read_clientes()
    clientes.append(cliente)
    write_clientes(clientes)

def update_cliente(cliente_id: int, novo_cliente: Cliente) -> bool:
    clientes = read_clientes()
    for idx, c in enumerate(clientes):
        if int(c.id) == cliente_id:
            clientes[idx] = novo_cliente
            write_clientes(clientes)
            return True
    return False

def delete_cliente(cliente_id: int) -> bool:
    clientes = read_clientes()
    novos_clientes = [c for c in clientes if int(c.id) != cliente_id]
    if len(novos_clientes) == len(clientes):
        return False
    write_clientes(novos_clientes)
    return True


@router.post("/")
def criar_cliente(cliente: Cliente):
    create_cliente(cliente)
    registrar_log(f"Cliente criado com sucesso (ID: {cliente.id})")
    return {"mensagem": "Cliente criado com sucesso"}

@router.get("/", response_model=List[Cliente])
def listar_clientes():
    registrar_log("Listagem de clientes solicitada")
    return read_clientes()

@router.get("/quantidade")
def quantidade_clientes():
    registrar_log("Contagem de clientes solicitada")
    clientes = read_clientes()
    return {"quantidade": len(clientes)}

@router.get("/filtrar", response_model=List[Cliente])
def filtrar_clientes(
    nome: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    data_cadastro_min: Optional[str] = Query(None),
    data_cadastro_max: Optional[str] = Query(None),
):
    registrar_log(f"Filtragem de clientes solicitada: nome={nome}, email={email}")
    clientes = read_clientes()
    filtrados = []

    for cliente in clientes:
        if nome and nome.lower() not in cliente.nome.lower():
            continue
        if email and email.lower() not in cliente.email.lower():
            continue
        if data_cadastro_min and cliente.data_cadastro < data_cadastro_min:
            continue
        if data_cadastro_max and cliente.data_cadastro > data_cadastro_max:
            continue
        filtrados.append(cliente)

    return filtrados

@router.get("/{cliente_id}", response_model=Cliente)
def obter_cliente(cliente_id: int):
    cliente = get_cliente_by_id(cliente_id)
    if not cliente:
        registrar_log(f"Tentativa de acesso a cliente inexistente (ID: {cliente_id})", nivel="warning")
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    logger.info(f"Cliente consultado (ID: {cliente_id})")
    return cliente

@router.put("/{cliente_id}")
def atualizar_cliente(cliente_id: int, novo_cliente: Cliente):
    if not update_cliente(cliente_id, novo_cliente):
        registrar_log(f"Tentativa de atualizar cliente inexistente (ID: {cliente_id})", nivel="warning")
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    registrar_log(f"Cliente atualizado com sucesso (ID: {cliente_id})")
    return {"mensagem": "Cliente atualizado com sucesso"}

@router.delete("/{cliente_id}")
def excluir_cliente(cliente_id: int):
    if not delete_cliente(cliente_id):
        registrar_log(f"Tentativa de exclusão de cliente inexistente (ID: {cliente_id})", nivel="warning")
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    registrar_log(f"Cliente excluído com sucesso (ID: {cliente_id})")
    return {"mensagem": "Cliente excluído com sucesso"}

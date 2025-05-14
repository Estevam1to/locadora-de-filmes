import csv
import os
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from config.logs import registrar_log
from schemas.aluguel import Aluguel

ALUGUEIS_CSV = "data/alugueis.csv"

router = APIRouter()


def read_alugueis() -> List[Aluguel]:
    if not os.path.exists(ALUGUEIS_CSV):
        return []
    with open(ALUGUEIS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [Aluguel(**row) for row in reader]


def write_alugueis(alugueis: List[Aluguel]):
    with open(ALUGUEIS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=Aluguel.model_fields.keys())
        writer.writeheader()
        for aluguel in alugueis:
            writer.writerow(aluguel.dict())


def get_aluguel_by_id(aluguel_id: int) -> Optional[Aluguel]:
    return next((a for a in read_alugueis() if int(a.id) == aluguel_id), None)


def create_aluguel(aluguel: Aluguel):
    alugueis = read_alugueis()
    alugueis.append(aluguel)
    write_alugueis(alugueis)


def update_aluguel(aluguel_id: int, novo_aluguel: Aluguel) -> bool:
    alugueis = read_alugueis()
    for idx, a in enumerate(alugueis):
        if int(a.id) == aluguel_id:
            alugueis[idx] = novo_aluguel
            write_alugueis(alugueis)
            return True
    return False


def delete_aluguel(aluguel_id: int) -> bool:
    alugueis = read_alugueis()
    novos = [a for a in alugueis if int(a.id) != aluguel_id]
    if len(novos) == len(alugueis):
        return False
    write_alugueis(novos)
    return True


@router.post("/")
def criar_aluguel(aluguel: Aluguel):
    create_aluguel(aluguel)
    registrar_log(f"Aluguel criado com sucesso (ID: {aluguel.id})")
    return {"mensagem": "Aluguel criado com sucesso"}


@router.get("/", response_model=List[Aluguel])
def listar_alugueis():
    registrar_log("Listagem de alugueis solicitada")
    return read_alugueis()


@router.get("/quantidade")
def quantidade_alugueis():
    registrar_log("Contagem de alugueis solicitada")
    alugueis = read_alugueis()
    return {"quantidade": len(alugueis)}


@router.get("/filtrar", response_model=List[Aluguel])
def filtrar_alugueis(
    status: Optional[str] = Query(None),
    cliente_id: Optional[int] = Query(None),
    filme_id: Optional[int] = Query(None),
    data_inicio_min: Optional[str] = Query(None),
    data_inicio_max: Optional[str] = Query(None),
):
    registrar_log(
        f"Filtragem de alugueis solicitada: status={status}, cliente_id={cliente_id}, filme_id={filme_id}"
    )
    alugueis = read_alugueis()
    filtrados = []

    for aluguel in alugueis:
        if status and status.lower() != aluguel.status.lower():
            continue
        if cliente_id and int(aluguel.cliente_id) != cliente_id:
            continue
        if filme_id and int(aluguel.filme_id) != filme_id:
            continue
        if data_inicio_min and aluguel.data_inicio < data_inicio_min:
            continue
        if data_inicio_max and aluguel.data_inicio > data_inicio_max:
            continue
        filtrados.append(aluguel)

    return filtrados


@router.get("/{aluguel_id}", response_model=Aluguel)
def obter_aluguel(aluguel_id: int):
    aluguel = get_aluguel_by_id(aluguel_id)
    if not aluguel:
        registrar_log(
            f"Tentativa de acesso a aluguel inexistente (ID: {aluguel_id})",
            nivel="warning",
        )
        raise HTTPException(status_code=404, detail="Aluguel não encontrado")
    registrar_log(f"Aluguel consultado (ID: {aluguel_id})")
    return aluguel


@router.put("/{aluguel_id}")
def atualizar_aluguel(aluguel_id: int, novo_aluguel: Aluguel):
    if not update_aluguel(aluguel_id, novo_aluguel):
        registrar_log(
            f"Tentativa de atualizar aluguel inexistente (ID: {aluguel_id})",
            nivel="warning",
        )
        raise HTTPException(status_code=404, detail="Aluguel não encontrado")
    registrar_log(f"Aluguel atualizado com sucesso (ID: {aluguel_id})")
    return {"mensagem": "Aluguel atualizado com sucesso"}


@router.delete("/{aluguel_id}")
def excluir_aluguel(aluguel_id: int):
    if delete_aluguel(aluguel_id):
        registrar_log(f"Aluguel excluído com sucesso (ID: {aluguel_id})")
        return {"mensagem": "Aluguel excluído com sucesso"}
    else:
        registrar_log(
            f"Tentativa de exclusão de aluguel inexistente (ID: {aluguel_id})",
            nivel="warning",
        )
        raise HTTPException(status_code=404, detail="Aluguel não encontrado")

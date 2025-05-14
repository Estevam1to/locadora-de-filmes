import csv
import os
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from config.logs import registrar_log
from schemas.filme import Filme

router = APIRouter()


FILMES_CSV = "data/filmes.csv"


def read_filmes() -> List[Filme]:
    if not os.path.exists(FILMES_CSV):
        return []
    with open(FILMES_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [Filme(**row) for row in reader]


def write_filmes(filmes: List[Filme]):
    with open(FILMES_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=Filme.model_fields.keys())
        writer.writeheader()
        for filme in filmes:
            writer.writerow(filme.dict())


def get_filme_by_id(filme_id: int) -> Optional[Filme]:
    return next((f for f in read_filmes() if int(f.id) == filme_id), None)


def create_filme(filme: Filme):
    filmes = read_filmes()
    filmes.append(filme)
    write_filmes(filmes)


def update_filme(filme_id: int, novo_filme: Filme) -> bool:
    filmes = read_filmes()
    for idx, f in enumerate(filmes):
        if int(f.id) == filme_id:
            filmes[idx] = novo_filme
            write_filmes(filmes)
            return True
    return False


def delete_filme(filme_id: int) -> bool:
    filmes = read_filmes()
    new_filmes = [f for f in filmes if int(f.id) != filme_id]
    if len(filmes) == len(new_filmes):
        return False
    write_filmes(new_filmes)
    return True


@router.post("/")
def criar_filme(filme: Filme):
    create_filme(filme)
    registrar_log(f"Filme criado com sucesso (ID: {filme.id})")
    return {"mensagem": "Filme criado com sucesso"}


@router.get("/", response_model=List[Filme])
def listar_filmes():
    registrar_log("Listagem de filmes solicitada")
    return read_filmes()


@router.get("/quantidade")
def quantidade_filmes():
    registrar_log("Contagem de filmes solicitada")
    filmes = read_filmes()
    return {"quantidade": len(filmes)}


@router.get("/filtrar", response_model=List[Filme])
def filtrar_filmes(
    genero: Optional[str] = Query(None),
    ano_min: Optional[int] = Query(None),
    ano_max: Optional[int] = Query(None),
):
    registrar_log(
        f"Filtragem de filmes solicitada: genero={genero}, ano_min={ano_min}, ano_max={ano_max}"
    )
    filmes = read_filmes()
    filtrados = []

    for filme in filmes:
        if genero and genero.lower() not in filme.genero.lower():
            continue
        if ano_min and int(filme.ano_lancamento) < ano_min:
            continue
        if ano_max and int(filme.ano_lancamento) > ano_max:
            continue
        filtrados.append(filme)

    return filtrados


@router.get("/{filme_id}")
def obter_filme(filme_id: int):
    filme = get_filme_by_id(filme_id)
    if not filme:
        registrar_log(
            f"Tentativa de acesso a filme inexistente (ID: {filme_id})", nivel="warning"
        )
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    registrar_log(f"Filme consultado (ID: {filme_id})")
    return filme


@router.put("/{filme_id}")
def atualizar_filme(filme_id: int, novo_filme: Filme):
    if not update_filme(filme_id, novo_filme):
        registrar_log(
            f"Tentativa de atualizar filme inexistente (ID: {filme_id})",
            nivel="warning",
        )
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    registrar_log(f"Filme atualizado com sucesso (ID: {filme_id})")
    return {"mensagem": "Filme atualizado com sucesso"}


@router.delete("/{filme_id}")
def excluir_filme(filme_id: int):
    if not delete_filme(filme_id):
        registrar_log(
            f"Tentativa de exclusão de filme inexistente (ID: {filme_id})",
            nivel="warning",
        )
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    registrar_log(f"Filme excluído com sucesso (ID: {filme_id})")
    return {"mensagem": "Filme excluído com sucesso"}

from datetime import date
from typing import Optional

from pydantic import BaseModel


class Aluguel(BaseModel):
    id: int
    cliente_id: int
    filme_id: int
    data_aluguel: date
    data_devolucao: Optional[date] = None
    status: str = "ativo"  # Default status is "ativo"

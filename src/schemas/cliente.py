from datetime import date

from pydantic import BaseModel, EmailStr


class Cliente(BaseModel):
    id: int
    nome: str
    email: EmailStr
    telefone: str
    data_cadastro: date

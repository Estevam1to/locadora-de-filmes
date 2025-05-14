from pydantic import BaseModel


class Filme(BaseModel):
    id: int
    titulo: str
    genero: str
    ano_lancamento: int
    disponivel: bool

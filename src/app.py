from fastapi import FastAPI

from routes import aluguel, cliente, filme, convert_files

app = FastAPI()

app.include_router(filme.router, prefix="/filmes", tags=["Filmes"])
app.include_router(cliente.router, prefix="/clientes", tags=["Clientes"])
app.include_router(aluguel.router, prefix="/alugueis", tags=["Alugueis"])
app.include_router(
    convert_files.router, prefix="/converter", tags=["Conversão de Arquivos"]
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=5000, workers=2)

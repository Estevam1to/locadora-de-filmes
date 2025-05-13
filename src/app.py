from fastapi import FastAPI

app = FastAPI()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=5000, workers=2)

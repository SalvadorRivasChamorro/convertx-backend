from fastapi import FastAPI

app = FastAPI(title="ConvertX API")

@app.get("/")
def home():
    return {"status":"ConvertX API funcionando"}

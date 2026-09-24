from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import List
import tempfile
import os
import zipfile


app = FastAPI(title="ConvertX API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "status": "ConvertX API funcionando"
    }


@app.post("/convert")
async def convert(
    files: List[UploadFile] = File(...),
    type: str = Form(...)
):

    folder = tempfile.mkdtemp()
    zip_path = os.path.join(folder, "convertidos.zip")

    with zipfile.ZipFile(zip_path, "w") as zipf:

        for file in files:
            path = os.path.join(folder, file.filename)

            with open(path, "wb") as f:
                f.write(await file.read())

            zipf.write(path, file.filename)


    return FileResponse(
        zip_path,
        filename="convertidos.zip"
    )

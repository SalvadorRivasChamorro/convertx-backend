from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import List
import tempfile
import os
import zipfile
import subprocess


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
    return {"status": "ConvertX API funcionando"}


@app.post("/convert")
async def convert(
    files: List[UploadFile] = File(...),
    type: str = Form(...)
):

    folder = tempfile.mkdtemp()
    zip_path = os.path.join(folder, "convertidos.zip")

    converted_files = []


    for file in files:

        original = os.path.join(folder, file.filename)

        with open(original, "wb") as f:
            f.write(await file.read())


        output = folder


        if type == "docx_pdf":
            formato = "pdf"

        elif type == "ppt_pdf":
            formato = "pdf"

        elif type == "pdf_docx":
            formato = "docx"

        else:
            formato = "pptx"


        subprocess.run([
            "libreoffice",
            "--headless",
            "--convert-to",
            formato,
            "--outdir",
            output,
            original
        ])


        nombre = os.path.splitext(file.filename)[0] + "." + formato

        convertido = os.path.join(folder, nombre)


        if os.path.exists(convertido):
            converted_files.append(convertido)


    with zipfile.ZipFile(zip_path, "w") as zipf:

        for file in converted_files:
            zipf.write(
                file,
                os.path.basename(file)
            )


    return FileResponse(
        zip_path,
        filename="ConvertX_resultados.zip"
    )

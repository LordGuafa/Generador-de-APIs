"""
Este archivo contiene la inizializacion y los endpoints de la api
"""
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os, zipfile, shutil
from controller import leer_xml, generate_script, create_docker, crear_api

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

@app.post("/generate_project")
async def load_xml(file: UploadFile = File(...)):
    filename = file.filename
    project_dir = f"api's/{filename[:-4]}"
    if os.path.exists(f"schemas/{filename}"):
        return "File alredy exists"   
    with open(f"schemas/{filename}", "wb") as buffer:
        buffer.write(await file.read())     
    os.makedirs(project_dir, exist_ok=True)
    root = leer_xml(filename)
    generate_script(root, filename)
    create_docker(root, filename)
    crear_api(root, filename)
    zip_filename = f"{project_dir}.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, project_dir)
                zipf.write(file_path, arcname)

    # Remove the project directory
    shutil.rmtree(project_dir)
    
    # Return the ZIP file
    return FileResponse(zip_filename, media_type='application/zip', filename=os.path.basename(zip_filename))
    
"""
Este archivo contiene la inizializacion y los endpoints de la api
"""
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import zipfile
import shutil
from controller import leer_xml, generate_script, create_docker, crear_api, create_dockerXpressSQL, create_docker_mongo
from SQLfolder import crearApiSQLJS, crearEndPointsSQL
from mongodb import crearApiMongo, crearEndPointsMongo, crearModeloMongo
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    res = FileResponse(zip_filename, media_type='application/zip',
                       filename=os.path.basename(zip_filename))
    # Return the ZIP file
    return res


@app.post("/GenerateProjectXpressSQL")
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
    create_dockerXpressSQL(root, filename)
    crearApiSQLJS(root, project_dir)
    crearEndPointsSQL(root, project_dir)
    zip_filename = f"{project_dir}.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, project_dir)
                zipf.write(file_path, arcname)

    # Remove the project directory
    shutil.rmtree(project_dir)

    res = FileResponse(zip_filename, media_type='application/zip',
                       filename=os.path.basename(zip_filename))
    # Return the ZIP file
    return res


@app.post("/GenerateProjectXpressMongoBD")
async def load_xml(file: UploadFile = File(...)):
    filename = file.filename
    project_dir = f"api's/{filename[:-4]}"
    if os.path.exists(f"schemas/{filename}"):
        return "File alredy exists"
    with open(f"schemas/{filename}", "wb") as buffer:
        buffer.write(await file.read())
    os.makedirs(project_dir, exist_ok=True)
    root = leer_xml(filename)
    crearApiMongo(root, project_dir)
    crearEndPointsMongo(root, project_dir)
    crearModeloMongo(root, project_dir)
    create_docker_mongo(root, filename)
    zip_filename = f"{project_dir}.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, project_dir)
                zipf.write(file_path, arcname)

    # Remove the project directory
    shutil.rmtree(project_dir)

    res = FileResponse(zip_filename, media_type='application/zip',
                       filename=os.path.basename(zip_filename))
    # Return the ZIP file
    return res


@app.get("/eliminar/{filename}")
def delete(filename):
    project_dir = f"api's/{filename[:-4]}"
    zip_filename = f"{project_dir}.zip"
    os.remove(zip_filename)
    os.remove(f"schemas/{filename}")

import xml.etree.ElementTree as ET
import os

def crear_api(root, filename):
    ruta=f"api's/{filename[:-4]}/backend"
    os.mkdir(ruta)

    entidades = root.findall("Entidad")
    main = ""

    main += '''
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from DAO.FacadeDAO import FacadeDAO
from model.Schemas import UserCreate, UserLogin

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
    '''
    file_path = f"{ruta}/main.py"
    with open(file_path, 'w') as file:
        file.write(main)

    ruta2=f"{ruta}/model"
    os.mkdir(ruta2)

    Schemas=""

    Schemas += '''
from pydantic import BaseModel\n\n
    '''
    for entidad in entidades:
        Schemas += f'''class {entidad[0].text}(BaseModel):\n'''
        atributos = entidad.findall("Atributo")
        for atributo in atributos:
            if atributo.find("autoincrementable") is not None:
                Schemas+=""
            else:
                Schemas += f"\t{atributo[1].text}:"
                if(atributo[0].text == "VARCHAR"):
                    Schemas += f"str\n"
                elif(atributo[0].text == "INT"):
                    Schemas += f"int\n"
                elif(atributo[0].text == "BOOLEAN"):
                    Schemas += f"bool\n"
                elif(atributo[0].text == "TIME"):
                    Schemas += f"int\n"
                
        Schemas += "\n"

    Schemas = Schemas.replace("ñ", "n")
    file_path = f'{ruta2}/Schemas.py'
    with open(file_path, 'w') as file:
        file.write(Schemas)

    modelo=""
    modelo += '''
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()\n\n'''

    for entidad in entidades:
        modelofor2=modelo
        modelo += f'''class {entidad[0].text}(Base):\n'''
        atributos = entidad.findall("Atributo")
        
        modelo += f'\t__tablename__ = "{entidad[0].text}"\n'
        
        for atributo in atributos:
            modelomomento=modelo
            modelomomento += f"\t{atributo[1].text}= Column("
            
            if(atributo[0].text == "VARCHAR"):
                modelomomento += f"String,"
            elif(atributo[0].text == "INT"):
                modelomomento += f"Integer,"
            elif(atributo[0].text == "BOOLEAN"):
                modelomomento += f"{atributo[1].text}=True,"
            elif(atributo[0].text == "TIME"):
                modelomomento += f"Integer,"

            if atributo.find("llavePrimaria") is not None:
                modelomomento += " primary_key=True,"
            else:
                modelomomento += ""

            if atributo.find("autoincrementable") is not None:
                modelomomento += " autoincrement=True,"
            else:
                modelomomento += ""

            if atributo.find("nullable").text == "true":
                modelomomento += " nullable=True,"
            else:
                modelomomento += " nullable=False,"
            
            if atributo.find("llaveUnica") is not None:
                modelomomento += " unique=True)\n"
            else:
                modelomomento += "unique=False)\n"
            
            
            modelo= modelomomento



        modelo = modelo.replace("ñ", "n")
        file_path = f'{ruta2}/{entidad[0].text}.py'
        with open(file_path, 'w') as file:
            file.write(modelo)
        
        modelo = modelofor2


    ruta3=f"{ruta}/routes"
    os.mkdir(ruta3)

    auth=""

    auth += '''
from fastapi import APIRouter
from DAO.FacadeDAO import create_user, login_user
from model.Schemas import '''

    for i, entidad in enumerate(entidades):
        auth += f'{entidad[0].text}'
        if i < len(entidades) - 1:
            auth += ','




    auth += '''
\n\nauth_routes = APIRouter()\n
    '''

    for entidad in entidades:
        auth += f'@auth_routes.post("/{entidad[0].text}")\n'
        auth += f'def {entidad[0].text}(request: {entidad[0].text}):\n \treturn {entidad[0].text}(request) \n\n'
    file_path = f'{ruta3}/auth.py'
    with open(file_path, 'w') as file:
        file.write(auth)
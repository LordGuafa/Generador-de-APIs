"""
Este archivo se encarga de crear el projecto en python
"""

import os


def create_connection(ruta):
    """
    Este metodo se encarga de crear el archivo encargado de crear la conexion a la base de datos
    """
    ruta_connection = f"{ruta}/DAO"
    os.mkdir(ruta_connection)

    connection = """
    import os
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, scoped_session, Session
    from dotenv import load_dotenv
    from sqlalchemy.exc import SQLAlchemyError

    class Connection:
        __instance = None

        def __new__(cls):
            if cls.__instance is None:
                cls.__instance = super(Connection, cls).__new__(cls)
                try:
                    cls.__instance._initialize()
                except Exception as e:
                    cls.__instance = None
                    raise e
            return cls.__instance

        def _initialize(self):
            load_dotenv()
            db_user = os.getenv('DB_USER')
            print(db_user)
            db_password = os.getenv('DB_PASSWORD')
            db_url = os.getenv('DB_URL')
            db_port = os.getenv('DB_PORT')
            db_name = os.getenv('DB_NAME')

            if not all([db_user, db_password, db_url, db_port, db_name]):
                raise ValueError("Una o más variables de entorno faltan.")

            database_connection = (
                f"mysql+pymysql://{db_user}:{db_password}@{db_url}:{db_port}/{db_name}"
            )

            try:
                self._engine = create_engine(database_connection)
                self._session_factory = sessionmaker(bind=self._engine)
                self._session = scoped_session(self._session_factory)
            except SQLAlchemyError as e:
                raise RuntimeError(f"Error al inicializar la conexión con la base de datos: {e}")

        def get_session(self):
            try:
                return self._session()
            except SQLAlchemyError as e:
                raise RuntimeError(f"Error al obtener la sesión de la base de datos: {e}")

        def close_session(self):
            try:
                self._session.remove()
            except SQLAlchemyError as e:
                raise RuntimeError(f"Error al cerrar la sesión de la base de datos: {e}")
            
    class BaseDAO:
        def __init__(self) -> None:
            self.db: Session = Connection().get_session()

        def commit(self):
            self.db.commit()

        def close(self):
            self.db.close()"""

    file_path = f"{ruta_connection}/Connection.py"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(connection)


def create_models(ruta, entidades):
    """
    Este metodo se encarga de crear los modelos de las entidades
    """
    ruta_models = f"{ruta}/model"
    os.mkdir(ruta_models)
    # Creacion del Schemas
    schemas = """
from pydantic import BaseModel\n\n"""

    for entidad in entidades:
        schemas += f"""class {entidad[0].text}(BaseModel):\n"""
        atributos = entidad.findall("Atributo")
        for atributo in atributos:
            if atributo.find("autoincrementable") is not None:
                schemas += ""
            else:
                schemas += f"\t{atributo[1].text}:"
                if atributo[0].text == "VARCHAR":
                    schemas += "str\n"
                elif atributo[0].text == "INT":
                    schemas += "int\n"
                elif atributo[0].text == "BOOLEAN":
                    schemas += "bool\n"
                elif atributo[0].text == "TIME":
                    schemas += "str\n"
        schemas += "\n"

    schemas = schemas.replace("ñ", "n")
    file_path = f"{ruta_models}/Schemas.py"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(schemas)

    # Creacion de los modelos
    modelo = ""
    modelo += """
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()\n\n"""

    for entidad in entidades:
        modelofor2 = modelo
        modelo += f"""class {entidad[0].text}(Base):\n"""
        atributos = entidad.findall("Atributo")
        modelo += f'\t__tablename__ = "{entidad[0].text}"\n'
        for atributo in atributos:
            modelomomento = modelo
            modelomomento += f"\t{atributo[1].text}= Column("
            if atributo[0].text == "VARCHAR":
                modelomomento += "String,"
            elif atributo[0].text == "INT":
                modelomomento += "Integer,"
            elif atributo[0].text == "BOOLEAN":
                modelomomento += f"{atributo[1].text}=True,"
            elif atributo[0].text == "TIME":
                modelomomento += "Integer,"

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
            modelo = modelomomento

        modelo = modelo.replace("ñ", "n")
        file_path = f"{ruta_models}/{entidad[0].text}.py"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(modelo)
        modelo = modelofor2

    init = ""
    for entidad in entidades:
        init += f"from model.{entidad[0].text} import {entidad[0]}\n"
    file_path = f"{ruta_models}/__init__.py"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(init)

def create_main(ruta, entidades):
    """
    Este metodo crea el archivo main de la aplicacion
    """
    main = """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model import """

    for entidad in entidades:
        main += f"{entidad[0].text} "

    main += """
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
"""
    file_path = f"{ruta}/main.py"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(main)

def create_routes(ruta, entidades):
    """
    Este metodo crea los endpoints de la api
    """
    # Creacion de las rutas
    ruta3 = f"{ruta}/routes"
    os.mkdir(ruta3)

    rutas = ""

    rutas += """
from fastapi import APIRouter\n"""

    for entidad in entidades:
        atributos = entidad.findall("Atributo")
        rutasprueba = rutas
        rutasprueba += f"from model.Schemas import {entidad[0].text}\n\n"

        rutasprueba += f"{entidad[0].text}_route = APIRouter()\n\n"

        rutasprueba += f'@{entidad[0].text}_route.post("/create_{entidad[0].text}")\n'
        rutasprueba += (
            f"def create_{entidad[0].text}(request: {entidad[0].text}):\n\treturn "
        )
        rutasprueba += "{" + '"Response" : "Success create"' + "}\n\n"
        rutasprueba += f'@{entidad[0].text}_route.get("/read_{entidad[0].text}")\n'
        rutasprueba += (
            f"def get_{entidad[0].text}():\n"
            + "\treturn {"
            + f'"Response" : "List of {entidad[0].text}"'
            + "}\n\n"
        )
        for atributo in atributos:
            if atributo.find("llavePrimaria") is not None:
                tipodedato = ""
                if atributo[0].text == "INT":
                    tipodedato += "int"
                elif atributo[0].text == "VARCHAR":
                    tipodedato += "str"
                elif atributo[0].text == "BOOLEAN":
                    tipodedato += "str"
                elif atributo[0].text == "TIME":
                    tipodedato += "str"

                rutasprueba += (
                    f'@{entidad[0].text}_route.get("/read_{entidad[0].text}/'
                    + "{"
                    + f"{atributo[1].text}"
                    + "}"
                    + '")\n'
                )
                rutasprueba += f"def get_{entidad[0].text}({atributo[1].text}: "
                rutasprueba += (
                    f"{tipodedato}):\n"
                    + "\treturn {"
                    + f'"Response": "Details of cliente {atributo[1].text}"'
                    + "}\n\n"
                )

                rutasprueba += (
                    f'@{entidad[0].text}_route.PUT("/update_{entidad[0].text}/'
                    + "{"
                    + f"{atributo[1].text}"
                    + "}"
                    + '")\n'
                )
                rutasprueba += f"def update_{entidad[0].text}({atributo[1].text}: "
                rutasprueba += (
                    f"{tipodedato}):\n"
                    + "\treturn {"
                    + '"Response" : "Success update"'
                    + "}\n\n"
                )

                rutasprueba += (
                    f'@{entidad[0].text}_route.delete("/delete_{entidad[0].text}/'
                    + "{"
                    + f"{atributo[1].text}"
                    + "}"
                    + '")\n'
                )
                rutasprueba += f"def get_{entidad[0].text}({atributo[1].text}: "
                rutasprueba += (
                    f"{tipodedato}):\n"
                    + "\treturn {"
                    + '"Response" : "Success delete"'
                    + "}\n\n"
                )

            else:
                rutasprueba += ""

        file_path = f"{ruta3}/{entidad[0].text}.py"
        with open(file_path, "w", encoding='utf-8') as file:
            file.write(rutasprueba)

def crear_api(root, filename):
    """
    Este metodo se encarga de crear toda la api
    """
    ruta = f"api's/{filename[:-4]}/backend"
    os.mkdir(ruta)

    entidades = root.findall("Entidad")

    create_main(ruta, entidades)
    create_models(ruta, entidades)
    create_connection(ruta)
    create_routes(ruta, entidades)


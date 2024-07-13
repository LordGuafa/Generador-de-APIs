"""
En este archivo se encuentra la logica para crear el projecto de la api
"""

import os

str_types = [
    "VARCHAR", "CHAR", "TINYTEXT", "TEXT", "MEDIUMTEXT", "LONGTEXT", 
    "DATE", "TIME", "DATETIME", "TIMESTAMP", "GEOMETRY", "POINT", 
    "LINESTRING", "POLYGON", "MULTIPOINT", "MULTILINESTRING", 
    "MULTIPOLYGON", "GEOMETRYCOLLECTION", "JSON", "ENUM"
    ]

int_types = [
    "TINYINT", "SMALLINT", "MEDIUMINT", "INT", "INTEGER", "BIGINT", 
    "YEAR", "BIT"
]

float_types = [
    "FLOAT", "DOUBLE", "DOUBLE PRECISION", "DECIMAL", "NUMERIC"
]

boolean_types = [
    "BOOLEAN"
]

bytes_types = [
    "BINARY", "VARBINARY", "TINYBLOB", "BLOB", "MEDIUMBLOB", "LONGBLOB"
]

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


def create_schemas(ruta, entidades):
    """
    Este metodo crea los schemas que se usaran en la api para pedir datos
    """
    os.mkdir(ruta)
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
                schemas += f"\t{atributo[1].text.lower()}:"
                if atributo[0].text in str_types:
                    schemas += "str\n"
                elif atributo[0].text in int_types:
                    schemas += "int\n"
                elif atributo[0].text in float_types:
                    schemas += "float\n"
                elif atributo[0].text in boolean_types:
                    schemas += "bool\n"
                elif atributo[0].text in bytes_types:
                    schemas += "bytes\n"

    schemas = schemas.replace("ñ", "n")
    file_path = f"{ruta}/Schemas.py"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(schemas)


def create_models(ruta, entidades):
    """
    Este metodo se encarga de crear los modelos de las entidades
    """
    ruta_models = f"{ruta}/model"
    create_schemas(ruta_models, entidades)
    
    # Creacion de los modelos
    modelo = ""
    modelo += """
from sqlalchemy import Column, Integer, String, Boolean, Float, LargeBinary
from sqlalchemy.orm import declarative_base

Base = declarative_base()\n\n"""

    for entidad in entidades:
        modelofor2 = modelo
        modelo += f"""class {entidad[0].text}(Base):\n"""
        atributos = entidad.findall("Atributo")
        modelo += f'\t__tablename__ = "{entidad[0].text}"\n'
        for atributo in atributos:
            modelomomento = modelo
            modelomomento += f"\t{atributo[1].text.lower()}= Column("
            if atributo[0].text in str_types:
                modelomomento += "String,"
            elif atributo[0].text in int_types:
                modelomomento += "Integer,"
            elif atributo[0].text in float_types:
                modelomomento += "Float,"
            elif atributo[0].text in boolean_types:
                modelomomento += "Boolean,"
            elif atributo[0].text in bytes_types:
                modelomomento += "LargeBinary,"

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
        init += f"from model.{entidad[0].text} import {entidad[0].text}\n"
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

    for i, entidad in enumerate(entidades):
        main += f"{entidad[0].text}"
        if i < len(entidades) - 1:
            main += ", "
        else:
            main += "\n"
    for entidad in entidades:
        main += f"from routes.{entidad[0].text} import {entidad[0].text}_routes\n"

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
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
    for entidad in entidades:
        main += f'app.include_router({entidad[0].text}_routes, prefix="/{entidad[0].text}")\n'

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

    rutas = """
from fastapi import APIRouter\n"""
    initroutes = ""
    for entidad in entidades:
        atributos = entidad.findall("Atributo")
        rutasprueba = rutas
        rutasprueba += f"from model.Schemas import {entidad[0].text}\n"
        rutasprueba += f"from controller import {entidad[0].text}_controller as controller\n\n"

        rutasprueba += f"{entidad[0].text}_routes = APIRouter()\n\n"

        rutasprueba += f'@{entidad[0].text}_routes.post("/create_{entidad[0].text}")\n'
        rutasprueba += (
            f"def create_{entidad[0].text}(request: {entidad[0].text}):\n"
        )
        rutasprueba += f"\treturn controller.create_{entidad[0].text}(request)\n\n"
        rutasprueba += f'@{entidad[0].text}_routes.get("/read_{entidad[0].text}")\n'
        rutasprueba += (
            f"def get_{entidad[0].text}_list():\n"
            + f"\treturn controller.get_{entidad[0].text}()\n\n"
        )
        for atributo in atributos:
            if atributo.find("llavePrimaria") is not None:
                tipodedato = ""
                if atributo[0].text in str_types:
                    tipodedato = "str"
                elif atributo[0].text in int_types:
                    tipodedato = "int"
                elif atributo[0].text in boolean_types:
                    tipodedato = "bool"
                elif atributo[0].text == float_types:
                    tipodedato = "float"
                elif atributo[0].text == bytes_types:
                    tipodedato = "byte"

                rutasprueba += (
                    f'@{entidad[0].text}_routes.get("/read_{entidad[0].text}/'
                    + "{"
                    + f"{atributo[1].text.lower()}"
                    + "}"
                    + '")\n'
                )
                rutasprueba += f"def get_{entidad[0].text}({atributo[1].text.lower()}: "
                rutasprueba += (
                    f"{tipodedato}):\n"
                    + f"\treturn controller.get_{entidad[0].text}_{atributo[1].text.lower()}({atributo[1].text.lower()})\n\n"
                )

                rutasprueba += (
                    f'@{entidad[0].text}_routes.put("/update_{entidad[0].text}/'
                    +'{'
                    +f'{atributo[1].text.lower()}'
                    +'}'
                    +'")\n'
                )
                rutasprueba += f"def update_{entidad[0].text}(request: {entidad[0].text}, {atributo[1].text.lower()}: {tipodedato}):\n"
                rutasprueba += (
                    f"\treturn controller.update_{entidad[0].text}(request, {atributo[1].text.lower()})\n\n"   
                )

                rutasprueba += (
                    f'@{entidad[0].text}_routes.delete("/delete_{entidad[0].text}/'
                    + "{"
                    + f"{atributo[1].text.lower()}"
                    + "}"
                    + '")\n'
                )
                rutasprueba += f"def delete_{entidad[0].text}({atributo[1].text.lower()}: "
                rutasprueba += (
                    f"{tipodedato}):\n"
                + f"\treturn controller.delete_{entidad[0].text}({atributo[1].text.lower()})\n\n"
                )
            elif atributo.find("llaveUnica") is not None:
                tipodedato = ""
                if atributo[0].text in str_types:
                    tipodedato = "str"
                elif atributo[0].text in int_types:
                    tipodedato = "int"
                elif atributo[0].text in boolean_types:
                    tipodedato = "bool"
                elif atributo[0].text == float_types:
                    tipodedato = "float"
                elif atributo[0].text == bytes_types:
                    tipodedato = "byte"

                rutasprueba += (
                    f'@{entidad[0].text}_routes.get("/read_{entidad[0].text}_{atributo[1].text.lower()}/'
                    + "{"
                    + f"{atributo[1].text.lower()}"
                    + "}"
                    + '")\n'
                )
                rutasprueba += (
                    f"def get_{entidad[0].text}_{atributo[1].text.lower()}({atributo[1].text.lower()}: "
                )
                rutasprueba += (
                    f"{tipodedato}):\n"
                    + f"\treturn controller.get_{entidad[0].text}_{atributo[1].text.lower()}({atributo[1].text.lower()})\n\n"
                )
            else:
                rutasprueba += ""

        file_path = f"{ruta3}/{entidad[0].text}.py"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(rutasprueba)
        initroutes += f"from routes.{entidad[0].text} import {entidad[0].text}\n"
    file_path = f"{ruta3}/__init__.py"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(initroutes)


def create_DAO(ruta, entidades):
    ruta_DAO = f"{ruta}/DAO"
    DAOinit = ""
    DAOtext = """
from typing import List
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from """

    DAOtext += "DAO.Connection import BaseDAO\n"
    for entidad in entidades:
        DAOtextprueba = DAOtext
        DAOtextprueba += (
            f"from model.{entidad[0].text} import {entidad[0].text}\n\n"
        )

        DAOtextprueba += f"class {entidad[0].text}DAO(BaseDAO):\n"

        DAOtextprueba += "#CREATE\n"
        DAOtextprueba += f"\tdef create_{entidad[0].text}(self, {entidad[0].text.lower()}: {entidad[0].text}):\n"
        DAOtextprueba += "\t\ttry:\n"
        DAOtextprueba += f"\t\t\tself.db.add({entidad[0].text.lower()})\n"
        DAOtextprueba += "\t\t\tself.commit()\n"
        DAOtextprueba += f"\t\t\tself.db.refresh({entidad[0].text.lower()})\n"
        DAOtextprueba += "\t\texcept IntegrityError:\n"
        DAOtextprueba += "\t\t\tself.db.rollback()\n"

        atributos = entidad.findall("Atributo")
        for atributo in atributos:
            if atributo.find("llavePrimaria") is not None:
                DAOtextprueba += f"\t\t\tif self.db.query({entidad[0].text}).filter({entidad[0].text}.{atributo[1].text.lower()} == {entidad[0].text.lower()}.{atributo[1].text.lower()}).first():\n"
                DAOtextprueba += f'\t\t\t\traise HTTPException(status_code=400, detail="{atributo[1].text.lower()} already registered")\n'
            else:
                DAOtextprueba += f""
        DAOtextprueba += f"\t\t\treturn {entidad[0].text}\n\n"

        DAOtextprueba += "#READ ALL\n"

        DAOtextprueba += (
            f"\tdef get_{entidad[0].text}_list(self) -> List[{entidad[0].text}]:\n"
        )
        DAOtextprueba += f"\t\treturn self.db.query({entidad[0].text}).all()\n\n"

        DAOtextprueba += "#READ BY PRIMARY_KEY\n"

        for atributo in atributos:
            tipodedato = ""
            if atributo[0].text in str_types:
                tipodedato = "str"
            elif atributo[0].text in int_types:
                tipodedato = "int"
            elif atributo[0].text in boolean_types:
                tipodedato = "bool"
            elif atributo[0].text == float_types:
                tipodedato = "float"
            elif atributo[0].text == bytes_types:
                tipodedato = "byte"
            if atributo.find("llavePrimaria") is not None:
                DAOtextprueba += f"\tdef get_{entidad[0].text}(self, {atributo[1].text.lower()}: {tipodedato}) -> {entidad[0].text}:\n"
                DAOtextprueba += f"\t\treturn self.db.query({entidad[0].text}).filter({entidad[0].text}.{atributo[1].text.lower()} == {atributo[1].text.lower()}).first()\n\n"
            else:
                DAOtextprueba += f""

        DAOtextprueba += "#READ BY UNIQUE_KEY\n"

        for atributo in atributos:
            
            if atributo.find("llaveUnica") is not None:
                tipodedato = ""
                if atributo[0].text in str_types:
                    tipodedato = "str"
                elif atributo[0].text in int_types:
                    tipodedato = "int"
                elif atributo[0].text in boolean_types:
                    tipodedato = "bool"
                elif atributo[0].text == float_types:
                    tipodedato = "float"
                elif atributo[0].text == bytes_types:
                    tipodedato = "byte"
                DAOtextprueba += f"\tdef get_{entidad[0].text}_{atributo[1].text.lower()}(self, {atributo[1].text.lower()}: {tipodedato}) -> {entidad[0].text}:\n"
                DAOtextprueba += f"\t\treturn self.db.query({entidad[0].text}).filter({entidad[0].text}.{atributo[1].text.lower()} == {atributo[1].text.lower()}).first()\n\n"
            else:
                DAOtextprueba += f""

        DAOtextprueba += "#UPDATE\n"
        
        DAOtextprueba += f"\tdef update_{entidad[0].text}(self, {entidad[0].text.lower()}: {entidad[0].text}) -> {entidad[0].text}:\n"
        DAOtextprueba += "\t\ttry:\n"
        DAOtextprueba += f"\t\t\texisting_{entidad[0].text.lower()} = self.db.query({entidad[0].text}).filter({entidad[0].text}.{atributo[1].text.lower()} == {entidad[0].text.lower()}.{atributo[1].text.lower()}).first()\n"
        DAOtextprueba += f"\t\t\tif not existing_{entidad[0].text.lower()}:\n"
        DAOtextprueba += f'\t\t\t\traise HTTPException(status_code=404, detail="{entidad[0].text} no encontrado")\n'
        DAOtextprueba += f"\t\t\tfor key, value in {entidad[0].text.lower()}.__dict__.items():\n"
        DAOtextprueba += (
            f"\t\t\t\tif key != '_sa_instance_state':\n"+
            f"\t\t\t\t\tsetattr(existing_{entidad[0].text.lower()}, key, value)\n"
        )
        DAOtextprueba += "\t\t\tself.db.commit()\n"
        DAOtextprueba += (
            f"\t\t\tself.db.refresh(existing_{entidad[0].text.lower()})\n"
        )
        DAOtextprueba += "\t\texcept IntegrityError:\n"
        DAOtextprueba += "\t\t\tself.db.rollback()\n"
        DAOtextprueba += f'\t\t\traise HTTPException(status_code=400, detail="Error al actualizar {entidad[0].text}")\n'
        DAOtextprueba += f"\t\treturn existing_{entidad[0].text.lower()}\n"
            

        DAOtextprueba += "#DELETE\n"

        for atributo in atributos:
            tipodedato = ""
            if atributo[0].text in str_types:
                tipodedato = "str"
            elif atributo[0].text in int_types:
                tipodedato = "int"
            elif atributo[0].text in boolean_types:
                tipodedato = "bool"
            elif atributo[0].text == float_types:
                tipodedato = "float"
            elif atributo[0].text == bytes_types:
                tipodedato = "byte"

            if atributo.find("llavePrimaria") is not None:
                DAOtextprueba += f"\tdef delete_{entidad[0].text}(self, {atributo[1].text.lower()}: {tipodedato}):\n"
                DAOtextprueba += "\t\ttry:\n"
                DAOtextprueba += f"\t\t\tdata = self.get_{entidad[0].text}({atributo[1].text.lower()})\n"
                DAOtextprueba += "\t\t\tself.db.delete(data)\n"
                DAOtextprueba += "\t\t\tself.commit()\n"
                DAOtextprueba += "\t\t\treturn True\n"
                DAOtextprueba += "\t\texcept IntegrityError:\n"
                DAOtextprueba += "\t\t\tself.db.rollback()\n"
                DAOtextprueba += f'\t\t\traise HTTPException(status_code=400, detail="Error al eliminar {entidad[0].text}")\n\n'
            else:
                DAOtextprueba += ""
        DAOinit += f"from DAO.{entidad[0].text}DAO import {entidad[0].text}DAO\n"

        file_path = f"{ruta_DAO}/{entidad[0].text}DAO.py"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(DAOtextprueba)

        file_path = f"{ruta_DAO}/__init__.py"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(DAOinit)


def create_controller(ruta, entidades):
    ruta_controller = f"{ruta}/controller"
    os.mkdir(ruta_controller)
    controller = ""
    controllerinit=""

    for entidad in entidades:
        controllertext = controller
        controllertext += f"from fastapi import HTTPException\n"
        controllertext += f"from DAO import {entidad[0].text}DAO\n"
        controllertext += f"from model import {entidad[0].text}\n"
        controllertext += f"from model.Schemas import {entidad[0].text} as schema\n\n"

        controllertext += f"{entidad[0].text.lower()}_DAO = {entidad[0].text}DAO()\n\n"

        controllertext += f"#CREATE\n"

        controllertext += f"def create_{entidad[0].text}(data: schema):\n"
        controllertext += f'\ttry:\n'
        controllertext += f'\t\tcliente = Clientes('

        atributos = entidad.findall("Atributo")
        for i, atributo in enumerate(atributos):
            controllertext += f'{atributo[1].text.lower}=data.{atributo[1].text.lower}\n'
            if i < len(atributos) - 1:
                controllertext += ", "
            else:
                controllertext += ")\n"
        controllertext += f'\t\t{entidad[0].text.lower()}_DAO.create_{entidad[0].text}({entidad[0].text.lower()})\n'
        controllertext += f"\t\treturn 'Exitoso'\n"
        controllertext += f"\texcept Exception as e:\n"
        controllertext += f'\t\traise HTTPException(status_code=400, detail=f"'+'{'+'e}")\n\n'

        controllertext += f"#READ ALL\n"

        controllertext += f"""
def get_{entidad[0].text}():
    return {entidad[0].text.lower()}_DAO.get_{entidad[0].text}_list()\n
        """    
        controllertext += f"#READ BY PRIMARY_KEY\n"

        atributos = entidad.findall("Atributo")
        for atributo in atributos:
            if atributo.find("llavePrimaria") is not None:
                controllertext += f'def get_{entidad[0].text}_{atributo[1].text.lower()}(id):\n'
                controllertext += f'return {entidad[0].text.lower()}_DAO.get_{entidad[0].text}(id)'
            else:
                controllertext += ""
        
        controllertext += f"#READ BY UNIQUE_KEY\n"

        atributos = entidad.findall("Atributo")
        for atributo in atributos:
            tipodedato = ""
            if atributo[0].text in str_types:
                tipodedato = "str"
            elif atributo[0].text in int_types:
                tipodedato = "int"
            elif atributo[0].text in boolean_types:
                tipodedato = "bool"
            elif atributo[0].text == float_types:
                tipodedato = "float"
            elif atributo[0].text == bytes_types:
                tipodedato = "byte"
            if atributo.find("llaveUnica") is not None:
                controllertext += f'def get_{entidad[0].text}_{atributo[1].text.lower()}({atributo[1].text.lower()}: {tipodedato}) -> {entidad[0].text}:\n'
                controllertext += f'return {entidad[0].text.lower()}_DAO.get_{entidad[0].text}_{atributo[1].text.lower()}({atributo[1].text.lower()})\n\n'
            else:
                controllertext += ""

        controllertext += f"#UPDATE BY PRIMARY_KEY\n"

        atributos = entidad.findall("Atributo")
        for atributo in atributos:
            if atributo.find("llavePrimaria") is not None:
                controllertext += f'def update_{entidad[0].text}(data, {atributo[1].text.lower()}):\n'
                controllertext += f'\ttry:\n'
                controllertext += f'\t\t{entidad[0].text.lower()} = {entidad[0].text}(\n'
                controllertext += f'\t\t\t{atributo[1].text.lower()}={atributo[1].text.lower()},\n'
                atributos = entidad.findall("Atributo")
                for i, atributo in enumerate(atributos):
                    controllertext += f'\t\t\t{atributo[1].text.lower()}=data.{atributo[1].text.lower()}\n'
                    if i < len(atributos) - 1:
                        controllertext += ",\n"
                    else:
                        controllertext += "\n)\n"
                controllertext += f'\t\t{entidad[0].text.lower()}_DAO.update_{entidad[0].text}({entidad[0].text.lower()})\n'
                controllertext += f"\t\treturn 'Exitoso'\n"
                controllertext += f'\texcept Exception as e:\n'
                controllertext += f'\t\traise HTTPException(status_code=400, detail=f"'+'{'+'e})\n\n'
            else:
                controllertext += ""

        controllertext += f"#DELETE\n"
        controllertext += f"def delete_{entidad[0].text}(data):\n"
        controllertext += f"\ttry:\n"
        controllertext += f"\t\t{entidad[0].text.lower()}_DAO.delete_{entidad[0].text}(data)\n"
        controllertext += f"\t\treturn 'Exitoso'\n"
        controllertext += f"\texcept Exception as e:\n"
        controllertext += f"\t\treturn 'Error'\n"

        file_path = f"{ruta_controller}/{entidad[0].text}_controller.py"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(controllertext)

       
        controllerinit += f"from DAO.{entidad[0].text}DAO import {entidad[0].text}DAO\n"

        file_path = f"{ruta_controller}/__init__.py"
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(controllerinit)


def create_requirements(ruta):
    """
    Este metodo crea el archivo con las librerias que necesita el proyecto
    """
    requirements = """fastapi
uvicorn
sqlalchemy
pymysql
pydantic
python-dotenv
cryptography  
"""
    file_path = f"{ruta}/requirements.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(requirements)


def create_dotenvs(ruta, root):
    """
    Este metodo se encarga de crear el archivo con las variables de entorno
    """
    env = f"""DB_USER=root
DB_PASSWORD=1234
DB_URL=api-db
DB_PORT=3306
DB_NAME={root.find("Nombre").text}
    """
    file_path = f"{ruta}/.env"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(env)


def crear_api(root, filename):
    """
    Este metodo se encarga de crear toda la api
    """
    ruta = f"api's/{filename[:-4]}/backend"
    os.mkdir(ruta)

    entidades = root.findall("Entidad")

    create_requirements(ruta)
    create_dotenvs(ruta, root)
    create_main(ruta, entidades)
    create_models(ruta, entidades)
    create_connection(ruta)
    create_routes(ruta, entidades)
    create_DAO(ruta, entidades)
    create_controller(ruta, entidades)

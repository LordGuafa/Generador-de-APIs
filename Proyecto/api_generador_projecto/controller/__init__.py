"""
En este archivo se importan todos los metodos accesibles desde otras carpetas
"""
from controller.Lector import leer_xml
from controller.Script_tablas import generate_script
from controller.Crear_Docker import create_docker
from controller.crear_api import crear_api
from controller.crear_docker_xpress import create_dockerXpressSQL
from controller.crear_docker_mongo import create_docker_mongo

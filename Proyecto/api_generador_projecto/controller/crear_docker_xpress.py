"""
Este archivo se encarga de crear los docker donde se desplegara la aplicacion
"""


def create_dockerfile_backend(ruta):
    """
    Este metodo crea el archivo .Dockerfile para el backend
    """
    code = """
FROM node:latest

WORKDIR /app

COPY . .

RUN npm install
RUN npm i -S express mysql2


EXPOSE 8080

CMD ["npm", "start"]
  """
    file_path = f"{ruta}/backend.Dockerfile"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(code)


def create_dockerXpressSQL(root, filename):
    """
    Este metodo crea el docker-compose de la api
    """
    ruta = f"api's/{filename[:-4]}"
    create_dockerfile_backend(ruta)
    code = f"""
version: '3.3'
services:

  api-database:
    image: mysql
    container_name: api-db
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: 1234
      MYSQL_DATABASE: {root.find("Nombre").text}
    ports:
      - "3306:3306"
    volumes:
      - api-data:/var/lib/mysql
      - ./database:/docker-entrypoint-initdb.d
    networks:
      - api-network

  api-backend:
    image: api-backend-xpress
    container_name: api-backend-xpress
    build:
      context: .
      dockerfile: backend.Dockerfile
    ports:
      - "8080:8080"
    depends_on:
      - api-database
    networks:
      - api-network

volumes:
  api-data:
    driver: local

networks:
  api-network:
    driver: bridge"""
    file_path = f"{ruta}/docker-compose.yml"
    with open(file_path, 'w', encoding="utf-8") as file:
        file.write(code)

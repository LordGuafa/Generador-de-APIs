
code = """version: '3.3'
services:

  login-database:
    image: mysql
    container_name: login-db
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: 1234
      MYSQL_DATABASE: Prueba
    ports:
      - "3306:3306"
    volumes:
      - login-data:/var/lib/mysql
      - ./database:/docker-entrypoint-initdb.d
    networks:
      - login-network"""
      
file_path = 'docker-compose.yml'
with open(file_path, 'w') as file:
    file.write(code)
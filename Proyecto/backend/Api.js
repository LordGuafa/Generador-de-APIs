
const express = require("express");
const mysql = require("mysql2");
const bodyParser = require("body-parser");
const fs = require("fs");
clientes=require(clientes.controller.js)
prestamos=require(prestamos.controller.js)
copias=require(copias.controller.js)
peliculas=require(peliculas.controller.js)
const path = require("path");
// Crear una instancia de Express
const app = express();
app.use(express.json());
// Configurar la conexion a la base de datos MySQL
const connection = mysql.createConnection({
  host: "localhost", // Cambia esto a tu host de la base de datos
  user: "root", // Cambia esto a tu usuario de la base de datos
  password: "1234", // Cambia esto a tu contrasena de la base de datos
  database: "Prueba", // Cambia esto a tu base de datos
});

// Conectar a la base de datos
connection.connect((err) => {
  if (err) {
    console.error("Error connecting to the database:", err.stack);
    return;
  }
  console.log("Connected to the database as id " + connection.threadId);
});
//Endpoints para Clientes
app.post("/Clientes",clientes.create);
app.get("/Clientes",clientes.getAll);
app.get("/Clientes/*",clientes.noExist);
app.get("/Clientes/:cod_cliente",clientes.get);
app.put("/Clientes/:cod_cliente",clientes.update);
app.delete("/Clientes/:cod_cliente",clientes.delete);
//---------------------------------------------------------------------
//Endpoints para Prestamos
app.post("/Prestamos",prestamos.create);
app.get("/Prestamos",prestamos.getAll);
app.get("/Prestamos/*",prestamos.noExist);
app.get("/Prestamos/:id_prestamo",prestamos.get);
app.put("/Prestamos/:id_prestamo",prestamos.update);
app.delete("/Prestamos/:id_prestamo",prestamos.delete);
//---------------------------------------------------------------------
//Endpoints para Copias
app.post("/Copias",copias.create);
app.get("/Copias",copias.getAll);
app.get("/Copias/*",copias.noExist);
app.get("/Copias/:n_copia",copias.get);
app.put("/Copias/:n_copia",copias.update);
app.delete("/Copias/:n_copia",copias.delete);
//---------------------------------------------------------------------
//Endpoints para Peliculas
app.post("/Peliculas",peliculas.create);
app.get("/Peliculas",peliculas.getAll);
app.get("/Peliculas/*",peliculas.noExist);
app.get("/Peliculas/:id_pelicula",peliculas.get);
app.put("/Peliculas/:id_pelicula",peliculas.update);
app.delete("/Peliculas/:id_pelicula",peliculas.delete);
//---------------------------------------------------------------------

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});


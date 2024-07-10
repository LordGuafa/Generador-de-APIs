
const express = require("express");
const mysql = require("mysql2/promise"); // Utiliza mysql2/promise para soporte de async/await
const bodyParser = require("body-parser");

const clientes=require('./controllers/clientes.controller.js')
const prestamos=require('./controllers/prestamos.controller.js')
const copias=require('./controllers/copias.controller.js')
const peliculas=require('./controllers/peliculas.controller.js')
const path = require("path");
// Crear una instancia de Express
const app = express();
app.use(express.json());

// Configurar la conexion a la base de datos MySQL
const dbConfig = {
  host: "localhost",
  user: "root",
  password: "1234",
  database: "Prueba",
};

// Middleware para inyectar la conexión de la base de datos en las solicitudes
app.use(async (req, res, next) => {
  try {
    req.db = await mysql.createConnection(dbConfig);
    await req.db.connect();
    next();
  } catch (err) {
    console.error("Error connecting to the database:", err.stack);
    res.status(500).json({ error: "Database connection failed" });
  }
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


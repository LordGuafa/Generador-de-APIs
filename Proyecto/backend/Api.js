
const express = require("express");
const mongoose = require("mongoose");

const clientes=require('./controllers/clientes.controller.js')
const prestamos=require('./controllers/prestamos.controller.js')
const copias=require('./controllers/copias.controller.js')
const peliculas=require('./controllers/peliculas.controller.js')

// Crear una instancia de Express
const app = express();
app.use(express.json());
mongoose.connect(
  "mongodb+srv://Admin:hola1234@cluster0.jefznfs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0" // Cambiar por la url de la base de datos
);
//Endpoints para Clientes
app.post("/Clientes",clientes.create);
app.get("/Clientes",clientes.getAll);
app.get("/Clientes/:cod_cliente",clientes.get);
app.put("/Clientes/:cod_cliente",clientes.update);
app.delete("/Clientes/:cod_cliente",clientes.delete);
app.get("/Clientes/*",clientes.noExist);
//---------------------------------------------------------------------
//Endpoints para Prestamos
app.post("/Prestamos",prestamos.create);
app.get("/Prestamos",prestamos.getAll);
app.get("/Prestamos/:id_prestamo",prestamos.get);
app.put("/Prestamos/:id_prestamo",prestamos.update);
app.delete("/Prestamos/:id_prestamo",prestamos.delete);
app.get("/Prestamos/*",prestamos.noExist);
//---------------------------------------------------------------------
//Endpoints para Copias
app.post("/Copias",copias.create);
app.get("/Copias",copias.getAll);
app.get("/Copias/:n_copia",copias.get);
app.put("/Copias/:n_copia",copias.update);
app.delete("/Copias/:n_copia",copias.delete);
app.get("/Copias/*",copias.noExist);
//---------------------------------------------------------------------
//Endpoints para Peliculas
app.post("/Peliculas",peliculas.create);
app.get("/Peliculas",peliculas.getAll);
app.get("/Peliculas/:id_pelicula",peliculas.get);
app.put("/Peliculas/:id_pelicula",peliculas.update);
app.delete("/Peliculas/:id_pelicula",peliculas.delete);
app.get("/Peliculas/*",peliculas.noExist);
//---------------------------------------------------------------------

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});


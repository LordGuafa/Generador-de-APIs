const express = require("express");
const mysql = require("mysql2");
const bodyParser = require("body-parser");
const fs = require("fs");
const path = require("path");
// Crear una instancia de Express
const app = express();
app.use(express.json());
// Configurar la conexi�n a la base de datos MySQL
const connection = mysql.createConnection({
  host: "localhost", // Cambia esto a tu host de la base de datos
  user: "root", // Cambia esto a tu usuario de la base de datos
  password: "1234", // Cambia esto a tu contrase�a de la base de datos
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

// Definir una ruta simple
app.post("/Clientes", (req, res) => {
  const { dni, nombre, apellido1, apellido2, direccion, email } = req.body;
  const query =
    "INSERT INTO Clientes (  dni, nombre, apellido1, apellido2, direccion, email) VALUES (?, ?, ?,?,?,?)";
  connection.query(
    query,
    [dni, nombre, apellido1, apellido2, direccion, email],
    (error, results) => {
      if (error) {
        return res.status(500).json({ error: error.message });
      }
      res.status(201).json({ dni, nombre, email });
    }
  );
});

// 2. Obtener todos los usuarios
app.get("/Clientes", (req, res) => {
  const query = "SELECT * FROM Clientes";
  connection.query(query, (error, results) => {
    if (error) {
      return res.status(500).json({ error: error.message });
    }
    res.json(results);
  });
});

// 3. Obtener un usuario por ID
app.get("/Clientes/:cod_cliente", (req, res) => {
  const { cod_cliente } = req.params;
  const query = "SELECT * FROM Clientes WHERE cod_cliente = ?";
  connection.query(query, [cod_cliente], (error, results) => {
    if (error) {
      return res.status(500).json({ error: error.message });
    }
    if (results.length === 0) {
      return res.status(404).json({ error: "User not found" });
    }
    res.json(results[0]);
  });
});

// 4. Actualizar un usuario por ID
app.put("/Clientes/:cod_cliente", (req, res) => {
  const { id } = req.params;
  const { name, email } = req.body;
  const query = "UPDATE Clientes SET name = ?, email = ? WHERE id = ?";
  connection.query(query, [name, email, id], (error, results) => {
    if (error) {
      return res.status(500).json({ error: error.message });
    }
    if (results.affectedRows === 0) {
      return res.status(404).json({ error: "User not found" });
    }
    res.json({ id, name, email });
  });
});

// 5. Eliminar un usuario por ID
app.delete("/Clientes/:id", (req, res) => {
  const { id } = req.params;
  const query = "DELETE FROM Clientes WHERE id = ?";
  connection.query(query, [id], (error, results) => {
    if (error) {
      return res.status(500).json({ error: error.message });
    }
    if (results.affectedRows === 0) {
      return res.status(404).json({ error: "User not found" });
    }
    res.status(204).send();
  });
});

// Iniciar el servidor
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

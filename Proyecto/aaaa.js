const mongoose = require("mongoose");

const ClientesSchema = new mongoose.Schema({
  cod_cliente: { type: Number },
  dni: { type: Number, required: true },
  nombre: { type: String, required: true },
  apellido1: { type: String, required: true },
  apellido2: { type: String, required: true },
  direccion: { type: String },
  email: { type: String, required: true },
});

// Middleware para asignar el _id a cod_cliente antes de guardar
ClientesSchema.pre("save", function (next) {
  if (!this.cod_cliente) {
    this.cod_cliente = this._id;
  }
  next();
});

const Clientes = mongoose.model("Clientes", ClientesSchema);

module.exports = Clientes;
const mongoose = require("mongoose");

// const ClientesSchema = new mongoose.Schema({
//   cod_cliente: { type: Number },
//   dni: { type: Number, required: true },
//   nombre: { type: String, required: true },
//   apellido1: { type: String, required: true },
//   apellido2: { type: String, required: true },
//   direccion: { type: String },
//   email: { type: String, required: true },
// });
// ClientesSchema.pre("save", function (next) {
//   if (!this.direccion) {
//     this.direccion = this.id;

//     next();
//   }
// });
// const Clientes = mongoose.model("Clientes", ClientesSchema);
// module.exports = Clientes;

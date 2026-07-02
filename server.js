const express = require("express");
const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static("public"));

const productosRouter = require("./routes/productos");  // ya no hace falta destructuring
const carritoRouter = require("./routes/carrito");

app.use("/productos", productosRouter);
app.use("/carrito", carritoRouter);

app.listen(port, () => {
  console.log(`Servidor corriendo en http://localhost:${port}`);
});
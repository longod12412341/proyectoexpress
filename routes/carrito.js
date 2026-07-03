const express = require("express");
const router = express.Router();
const db = require("../database/db");

// GET carrito - ver contenido con datos del producto
router.get("/", (req, res) => {
  const items = db.prepare(`
    SELECT c.producto_id, c.cantidad, p.nombre, p.precio
    FROM carrito c
    JOIN productos p ON c.producto_id = p.id
  `).all();

  res.json(items);
});

// GET carrito total
router.get("/total", (req, res) => {
  const { total } = db.prepare(`
    SELECT SUM(c.cantidad * p.precio) as total
    FROM carrito c
    JOIN productos p ON c.producto_id = p.id
  `).get();

  res.json({ total: total || 0 });
});

// POST  agregar producto o sumar cantidad si ya existe
router.post("/", (req, res) => {
  const { producto_id, cantidad } = req.body;

  const producto = db.prepare("SELECT * FROM productos WHERE id = ?").get(producto_id);
  if (!producto) {
    return res.status(404).json({ error: "Producto no encontrado" });
  }

  const cantidadAgregar = cantidad || 1;
  const itemExistente = db.prepare("SELECT * FROM carrito WHERE producto_id = ?").get(producto_id);

  if (itemExistente) {
    db.prepare("UPDATE carrito SET cantidad = cantidad + ? WHERE producto_id = ?")
      .run(cantidadAgregar, producto_id);
  } else {
    db.prepare("INSERT INTO carrito (producto_id, cantidad) VALUES (?, ?)")
      .run(producto_id, cantidadAgregar);
  }

  res.status(201).json({ mensaje: "Producto agregado al carrito" });
});

// POST /carrito/:producto_id/decrementar - resta 1; si llega a 0, elimina la fila
router.put("/:producto_id/decrementar", (req, res) => {
  const { producto_id } = req.params;
  const item = db.prepare("SELECT * FROM carrito WHERE producto_id = ?").get(producto_id);
  if (!item) return res.status(404).json({ error: "Producto no encontrado en el carrito" });

  if (item.cantidad <= 1) {
    db.prepare("DELETE FROM carrito WHERE producto_id = ?").run(producto_id);
  } else {
    db.prepare("UPDATE carrito SET cantidad = cantidad - 1 WHERE producto_id = ?").run(producto_id);
  }
  res.json({ mensaje: "Cantidad actualizada" });
});

// DELETE /carrito/:producto_id - eliminar ítem completo
router.delete("/:producto_id", (req, res) => {
  const { producto_id } = req.params;
  const result = db.prepare("DELETE FROM carrito WHERE producto_id = ?").run(producto_id);

  if (result.changes === 0) {
    return res.status(404).json({ error: "Producto no encontrado en el carrito" });
  }

  res.json({ mensaje: "Producto eliminado del carrito" });
});

module.exports = router;
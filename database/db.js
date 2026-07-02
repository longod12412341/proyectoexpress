const Database = require("better-sqlite3");
const path = require("path");

const dbFile = process.env.DB_PATH || path.join(__dirname, "carrito.db");
const db = new Database(dbFile);

db.exec(`
  CREATE TABLE IF NOT EXISTS productos (
    id TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    stock INTEGER NOT NULL
  );

  CREATE TABLE IF NOT EXISTS carrito (
    producto_id TEXT PRIMARY KEY,
    cantidad INTEGER NOT NULL,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
  );
`);

// Seed: carga el catálogo original solo si la tabla está vacía
const { total } = db.prepare("SELECT COUNT(*) as total FROM productos").get();
if (total === 0) {
  const catalogo = [
    { id: "1", nombre: "Notebook", precio: 150000, stock: 1 },
    { id: "2", nombre: "Teclado", precio: 45000, stock: 2 },
    { id: "3", nombre: "Mouse", precio: 30000, stock: 5 },
    { id: "4", nombre: "Monitor", precio: 8000, stock: 3 },
    { id: "5", nombre: "PC GAMER", precio: 30000, stock: 1 },
  ];

  const insert = db.prepare(
    "INSERT INTO productos (id, nombre, precio, stock) VALUES (?, ?, ?, ?)"
  );
  for (const p of catalogo) insert.run(p.id, p.nombre, p.precio, p.stock);

  console.log("Catálogo inicial cargado en SQLite");
}

module.exports = db;
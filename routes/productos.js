const express = require("express");
const router = express.Router();
const db = require("../database/db");

router.get("/", (req, res) => {
  const filas = db.prepare("SELECT * FROM productos").all();

  const catalogo = {};
  filas.forEach((p) => (catalogo[p.id] = p));

  res.json(catalogo);
});

module.exports = router;
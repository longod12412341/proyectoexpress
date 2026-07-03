import pytest
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "carrito.db")

@pytest.fixture(autouse=True)
def vaciar_carrito():
    """Antes de cada test deja el carrito vacío para no arrastrar datos de otro test."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM carrito")
    conn.commit()
    conn.close()
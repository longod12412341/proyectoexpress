import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

BASE_URL = "http://localhost:3000"


@pytest.mark.usefixtures('class_setup')
class TestCarrito:

    @pytest.fixture
    def class_setup(self):
        self.driver = webdriver.Chrome()
        yield
        self.driver.quit()

    def test_ver_productos(self):
        self.driver.get(f"{BASE_URL}/index.html")
        time.sleep(1)  # le da tiempo al fetch de productos

        tarjetas = self.driver.find_elements(By.CLASS_NAME, "producto-card")
        assert len(tarjetas) == 5

    def test_agregar_al_carrito(self):
        self.driver.get(f"{BASE_URL}/index.html")
        time.sleep(1)

        boton = self.driver.find_element(By.CSS_SELECTOR, "button[onclick*=\"agregarAlCarrito('1')\"]")
        boton.click()
        time.sleep(1)

        self.driver.get(f"{BASE_URL}/carrito.html")
        time.sleep(1)

        items = self.driver.find_elements(By.CLASS_NAME, "carrito-item")
        assert len(items) == 1

    def test_total_correcto(self):
        self.driver.get(f"{BASE_URL}/index.html")
        time.sleep(1)

        boton = self.driver.find_element(By.CSS_SELECTOR, "button[onclick*=\"agregarAlCarrito('1')\"]")
        boton.click()
        time.sleep(1)

        self.driver.get(f"{BASE_URL}/carrito.html")
        time.sleep(1)

        total = self.driver.find_element(By.ID, "total-valor").text
        assert "150.000" in total

    def test_eliminar_del_carrito(self):
        self.driver.get(f"{BASE_URL}/index.html")
        time.sleep(1)

        boton = self.driver.find_element(By.CSS_SELECTOR, "button[onclick*=\"agregarAlCarrito('2')\"]")
        boton.click()
        time.sleep(1)

        self.driver.get(f"{BASE_URL}/carrito.html")
        time.sleep(1)

        self.driver.find_element(By.CLASS_NAME, "btn-remove").click()
        time.sleep(1)

        vacio = self.driver.find_element(By.CLASS_NAME, "carrito-vacio")
        assert "vacío" in vacio.text

    def test_persistencia(self):
        self.driver.get(f"{BASE_URL}/index.html")
        time.sleep(1)

        boton = self.driver.find_element(By.CSS_SELECTOR, "button[onclick*=\"agregarAlCarrito('3')\"]")
        boton.click()
        time.sleep(1)

        self.driver.get(f"{BASE_URL}/carrito.html")
        time.sleep(1)
        self.driver.refresh()
        time.sleep(1)

        items = self.driver.find_elements(By.CLASS_NAME, "carrito-item")
        assert len(items) == 1
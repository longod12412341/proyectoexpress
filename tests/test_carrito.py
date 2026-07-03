import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://localhost:3000"


@pytest.mark.usefixtures('class_setup')
class TestCarrito:

    @pytest.fixture
    def class_setup(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 5)
        yield
        self.driver.quit()

    def test_ver_productos(self):
        self.driver.get(f"{BASE_URL}/index.html")

        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "producto-card"))
        )

        tarjetas = self.driver.find_elements(By.CLASS_NAME, "producto-card")
        assert len(tarjetas) == 5

    def test_agregar_al_carrito(self):
        self.driver.get(f"{BASE_URL}/index.html")
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "producto-card"))
        )

        boton = self.driver.find_element(By.CSS_SELECTOR, "button[onclick*=\"agregarAlCarrito('1')\"]")
        boton.click()

        self.wait.until(
            EC.text_to_be_present_in_element((By.ID, "toast"), "agregado al carrito")
        )

        self.driver.get(f"{BASE_URL}/carrito.html")
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "carrito-item"))
        )

        items = self.driver.find_elements(By.CLASS_NAME, "carrito-item")
        assert len(items) == 1

    def test_total_correcto(self):
        self.driver.get(f"{BASE_URL}/index.html")
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "producto-card"))
        )

        boton = self.driver.find_element(By.CSS_SELECTOR, "button[onclick*=\"agregarAlCarrito('1')\"]")
        boton.click()

        self.wait.until(
            EC.text_to_be_present_in_element((By.ID, "toast"), "agregado al carrito")
        )

        self.driver.get(f"{BASE_URL}/carrito.html")
        self.wait.until(
            EC.presence_of_element_located((By.ID, "total-valor"))
        )

        total = self.driver.find_element(By.ID, "total-valor").text
        assert "150.000" in total

    def test_eliminar_del_carrito(self):
        self.driver.get(f"{BASE_URL}/index.html")
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "producto-card"))
        )

        boton = self.driver.find_element(By.CSS_SELECTOR, "button[onclick*=\"agregarAlCarrito('2')\"]")
        boton.click()
        self.wait.until(
            EC.text_to_be_present_in_element((By.ID, "toast"), "agregado al carrito")
        )

        self.driver.get(f"{BASE_URL}/carrito.html")
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "carrito-item"))
        )

        self.driver.find_element(By.CLASS_NAME, "btn-remove").click()

        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "carrito-vacio"))
        )

        vacio = self.driver.find_element(By.CLASS_NAME, "carrito-vacio")
        assert "vacío" in vacio.text

    def test_persistencia(self):
        self.driver.get(f"{BASE_URL}/index.html")
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "producto-card"))
        )

        boton = self.driver.find_element(By.CSS_SELECTOR, "button[onclick*=\"agregarAlCarrito('3')\"]")
        boton.click()
        self.wait.until(
            EC.text_to_be_present_in_element((By.ID, "toast"), "agregado al carrito")
        )

        self.driver.get(f"{BASE_URL}/carrito.html")
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "carrito-item"))
        )

        self.driver.refresh()

        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "carrito-item"))
        )

        items = self.driver.find_elements(By.CLASS_NAME, "carrito-item")
        assert len(items) == 1
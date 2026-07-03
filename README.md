Carrito de Compras — Migración de Flask a Express

Este proyecto es la migración de una API de carrito de compras que originalmente estaba hecha en Flask (Python) a Node.js con Express. Le sumé un frontend tipo SPA en HTML/JS vainilla, persistencia con SQLite y tests E2E con Selenium.

Arquitectura elegida
Organicé el proyecto en tres capas separadas: backend, base de datos y frontend, todas comunicadas a través de una API REST.

Backend: separé las rutas en dos archivos (productos.js y carrito.js), cada uno encargado solamente de su propio recurso, para que el código sea más fácil de leer y mantener.

Base de datos: usé SQLite con la librería better-sqlite3, que me pareció más simple porque su API es síncrona (no tuve que manejar promesas ni callbacks para consultas básicas). 

Armé dos tablas:

productos: el catálogo (id, nombre, precio, stock)

carrito: los ítems agregados (uso producto_id como clave primaria y cantidad)

Elegí producto_id como clave primaria de la tabla carrito para que la propia base de datos me impida tener el mismo producto duplicado en dos filas distintas: si agrego un producto que ya está en el carrito, 
directamente le sumo la cantidad en vez de crear una fila nueva.

Frontend: son dos páginas HTML (index.html y carrito.html) con JavaScript vainilla que se comunican con la API usando fetch. No hay recarga de página al interactuar con productos o el carrito, solo se navega entre las dos vistas.

Carrito : como el proyecto no pide login de usuarios, decidí que el carrito sea único para toda la aplicación. Esto simplifica bastante el modelo de datos porque no tuve que manejar sesiones ni usuarios.


Endpoints

GET/productosDevuelve el catálogo completo

GET/carritoDevuelve los ítems del carrito

GET/carrito/totalDevuelve el total de la compra

POST/carritoAgrega un producto (o suma cantidad si ya estaba)

PUT/carrito/:id/decrementarResta una unidad (elimina el ítem si llega a 0)

DELETE/carrito/:idElimina el ítem completo del carrito


Tecnologías utilizadas:

Node.js + Express para el servidor y la API REST

better-sqlite3 para la persistencia de datos

HTML, CSS y JavaScript vainilla para el frontend, sin frameworks

Python con pytest y Selenium para los tests E2E

Render para el deploy


Dificultades que encontré y cómo las resolví


1. Mi frontend ya estaba armado y probado, y esperaba el catálogo como un array y un campo llamado precio_unitario en los ítems del carrito. Pero mi backend migrado devolvía un objeto (no un array) y usaba el nombre precio. En vez de tocar el backend (que ya tenía andando), decidí adaptar las funciones del frontend para que consuman los datos tal cual los devuelve mi API. Me sirvió para entender que frontend y backend se ponen de
acuerdo en un "contrato" de datos, y que cuando cambiás de framework ese contrato puede variar.
2. Qué método HTTP usar para restar cantidad del carrito.
Restar una unidad de un producto no encaja perfectamente en las operaciones típicas de un CRUD. Lo correcto según REST hubiera sido usar PUT o PATCH, porque es una actualización, pero como en la materia todavía no vimos esos métodos, terminé usando POST para esa acción también.

3. La persistencia en Render se pierde con el tiempo.
Me di cuenta de que el plan gratuito de Render no tiene disco persistente: cuando el servidor se "duerme" por inactividad y se vuelve a levantar, el archivo carrito.db se resetea. Decidí aceptar esta limitación porque el alcance del trabajo es académico y la persistencia sí funciona correctamente en mi entorno local, que es donde valido que el requerimiento se cumple. Una mejora a futuro sería usar un disco persistente (de pago) en Render.

4. Evitar que los tests se pisen entre sí.
Como el carrito es único para toda la app (sin usuarios), me di cuenta de que si corría varios tests seguidos, uno podía dejar datos que afectaran al siguiente. Lo resolví agregando una fixture de pytest que se ejecuta automáticamente antes de cada test y vacía la tabla carrito por SQL, así cada test arranca siempre desde cero.


Cómo correr el proyecto localmente

bashnpm install

node server.js

Después abrir http://localhost:3000 en el navegador.

Cómo correr los tests

Con el servidor corriendo en otra terminal:

bashpip install pytest selenium

pytest tests/test_carrito.py -v

Aplicación web construida a partir del patrón de arquitectura MVC.
Utilizamos Docker para el desarrollo sin la necesidad de montar los servicios necesarios.
Para ello, nos centraremos en construir un #LAMP-like stack modernizado
(Linux + Apache/Nginx + MySQL + Python + Vue.js)

Vamos a estructurar la aplicación a traves de tres servicios principales:
 - #Backend     Flask (Python)      API REST que consulta MySQL y expone endpoints JSON
 - #Frontend    Vue.js (Node)       Interfaz de usuario SPA (Single Page Application)
 - #DataBase    MySQL               Base de datos relacional con tus productos

#Estructura de directorios

tienda_forestal_mvc_vue/
│
├── docker-compose.yml
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── __init__.py
│   │   ├── run.py
│   │   ├── controllers/
│   │   │   └── producto_controller.py
│   │   ├── models/
│   │   │   └── producto_model.py
│   │   └── config.py
│
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.js
│       ├── App.vue
│       ├── components/
│       │   └── Productos.vue
│
└── db/
    └── init.sql

La organizacion por capas en MVC queda de la siguiente forma:
| Capa                         | Carpeta                    | Función                                                                |
| ---------------------------- | -------------------------- | ---------------------------------------------------------------------- |
| **Modelo (Model)**           | `backend/app/models/`      | Gestiona el acceso a la base de datos MySQL y las operaciones CRUD     |
| **Controlador (Controller)** | `backend/app/controllers/` | Gestiona la lógica de negocio y define las rutas de la API REST        |
| **Vista (View)**             | `frontend/src/`            | Renderiza la interfaz de usuario en Vue.js; consume la API del backend |
| **Configuración**            | `backend/app/config.py`    | Variables de entorno y parámetros de la aplicación                     |
| **Base de datos**            | `db/init.sql`              | Scripts SQL para inicializar la base de datos y cargar productos       |


El esquema de flujo de MVC con Vue.js y Flask es el siguiente:
[Usuario / Navegador]
        │
        │ Interacción UI
        ▼
   [Frontend Vue.js]
        │
        │ HTTP Requests / Axios
        ▼
  [Backend Flask (Controlador)]
        │
        ├─ Consulta al Modelo (MySQL)
        │     backend/app/models/producto_model.py
        │
        └─ Devuelve JSON al Frontend
        ▼
   [Frontend Vue.js]
        │
        │ Renderiza la información en componentes
        ▼
[Usuario visualiza productos, búsqueda y filtrado]

Por lo tanto, el MVC adaptado al SPA moderno queda como:
 - #Modelo -> producto_model.py (BD)
 - #Controlador -> producto_controller.py (rutas y lógica)
 - #Vista -> Vue.js (App.vue, Productos.vue)

El esquema Docker general es:
┌────────────────────┐
│    Cliente Web     │
│ (Navegador / SPA) │
└────────┬───────────┘
         │ HTTP (Axios)
         ▼
┌──────────────────────────┐
│   Contenedor Frontend    │
│      (Vue.js / Node)     │
│  Servidor dev / build SPA│
└────────┬────────────────┘
         │ HTTP Requests
         ▼
┌──────────────────────────┐
│   Contenedor Backend     │
│      (Flask / Python)    │
│  Controlador y Modelo    │
└────────┬────────────────┘
         │ TCP 3306
         ▼
┌──────────────────────────┐
│   Contenedor MySQL       │
│ Base de datos Tienda     │
│ (productos, stock, precios) │
└──────────────────────────┘

El resumen de comunicación entre capas y contenedores es el siguiente:
| Componente          | Función                                      | Comunicación                          |
| ------------------- | -------------------------------------------- | ------------------------------------- |
| **Usuario**         | Interactúa con la UI                         | HTTP ↔ Frontend Vue.js                |
| **Frontend Vue.js** | SPA que muestra productos, busca y filtra    | HTTP ↔ Backend Flask (API `/api/...`) |
| **Backend Flask**   | Procesa solicitudes, lógica de negocio, CRUD | SQL ↔ Contenedor MySQL                |
| **MySQL**           | Almacena productos, stock, precios, imágenes | Consultas SQL ↔ Backend Flask         |

Hay que tener en cuenta los siguientes aspectos:
 - El frontend no toca directamente la base de datos;
   todo pasa por el backend -> mantiene la separación de capas. 
 - CORS permite que el fronted (puerto 8080) se comunique con Flask (puerto 5000) en
   Docker;
 - Docker-compose orquesta contenedores y asegura dependencias (depends_on).

**Ejecutar el docker**
docker-compose up --build

 - #Para abrir el frontend (*Vue.js*) -> http://localhost:8080
 - #Para abrir el backend (*Flask API*) -> http://localhost:5000/api/productos
 - #Para abrir la base de datos de MySQL: puerto 3306

**##OTROS**

**Estructura de directorios del proyecto para MVC**
Si el proyecto no quisiesemos separar la parte del backend con el frontend

tienda_forestal_mvc/
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
│
├── app/                        # Código fuente principal
│   ├── __init__.py
│   ├── run.py
│   │
│   ├── models/                 # Modelos (interacción con la BD)
│   │   ├── __init__.py
│   │   └── producto_model.py
│   │
│   ├── views/                  # Vistas (plantillas HTML)
│   │   ├── __init__.py
│   │   ├── layout.html
│   │   └── productos.html
│   │
│   ├── controllers/            # Controladores (lógica de negocio)
│   │   ├── __init__.py
│   │   └── producto_controller.py
│   │
│   └── static/                 # Archivos estáticos (CSS, JS, imágenes)
│       ├── css/
│       ├── js/
│       └── img/
│
└── db/                         # Inicialización de la base de datos
    └── init.sql


**CORS**
CORS (Cross-Origin Resource Sharing) Se trata de un mecanismo de seguridad implementado
en navegadores web. Este mecanismo sirve para controlar las solicitudes HTTP realizadas
desde Javascript con un origen diferente al del servidor (generalmente cuando el dominio de
origen difiere del dominio de destino de la solicitud). Por lo tanto, evita que los
servidores web se usen desde lugares que no est'an autorizados.
Básicamente, lo que hace es:
1. Comprende la política de mismo origen
2. Identifica las necesidades de Cross-Origin Requests
3. Configura el servidor para permitir CORS
4. Añade cabeceras de control de acceso (Access-Control-Allow-Origin;
   Access-Control-Allow-Methods; Access-Control-Headers; Access-Control-Allow-Credentials)
5. Gestiona solicitudes simples y Preflight Requests
6. Verifica la seguridad y las excepciones
7. Prueba y valida la configuración de CORS


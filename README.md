# API Stand Tests
 
Este es un proyecto que armé para practicar pruebas automatizadas de API con Python, usando `pytest` y `requests`. Lo hice como parte de mi aprendizaje en QA, así que lo documenté con detalle para mí mismo/a — tanto para no perderme si lo retomo después, como para que quede claro el razonamiento detrás de cada parte.
 
La API de prueba (stand) tiene endpoints para crear usuarios y crear "kits" de productos, y algunos endpoints requieren autenticación con un token.
 
## 📋 Requisitos previos
 
- Python 3.x
- pip
## ⚙️ Instalación
 
1. Clona o descarga este repositorio.
2. (Recomendado) Crea y activa un entorno virtual:
```bash
   python -m venv .venv
```
 
   En Windows (PowerShell):
```bash
   .venv\Scripts\activate
```

## 📁 Estructura del proyecto
 
```
├── .gitignore
├── configuration.py   # URLs base y rutas (paths) de los endpoints
├── data.py             # Datos de prueba: headers y bodies base (usuario, kit)
├── sender_stand_request.py   # Funciones que envían las solicitudes HTTP a la API
├── create_kit_name_kit_test.py   # Pruebas relacionadas con la creación de kits
└── README.md
```
 
### `configuration.py`
Aquí guardo la URL base del servicio (`URL_SERVICE`) y las rutas de cada endpoint (`CREATE_USER_PATH`, `KITS_PATH`, etc.), separadas del resto del código para no tener URLs "quemadas" repetidas por todos lados.
 
### `data.py`
Los diccionarios base que uso como plantilla en las solicitudes:
- `headers`: encabezados por defecto (ej. `Content-Type`).
- `user_body`: cuerpo base para crear un usuario.
- `kit_body`: cuerpo base para crear un kit.
 
### `sender_stand_request.py`
Las funciones que realmente mandan las solicitudes HTTP (`post_new_user`, `post_new_kit`, etc.) usando `requests`. 
 
### Archivos de test (`*_test.py`)
Cada archivo de test tiene tres tipos de funciones:
- **Funciones auxiliares** (`get_user_body`, `get_kit_body`, `get_headers`) que arman los bodies y headers que necesito para cada solicitud.
- **Funciones de aserción reutilizables** (`positive_assert`, `negative_assert`) que agrupan el flujo que se repite en varias pruebas: crear usuario → sacar el `authToken` de la respuesta → armar los headers con ese token → probar el endpoint que me interesa.
- **Funciones de prueba** (`test_...`), que son las que `pytest` reconoce y corre automáticamente.
## 🔑 Flujo de autenticación
 
Algunos endpoints, como crear un kit, necesitan que estés "autenticado". El token no se manda a mano ni se guarda fijo en ningún lado — se genera cada vez que creas un usuario nuevo. El flujo que sigo es:
 
1. Creo un usuario con `post_new_user`.
2. De la respuesta (`201`), saco el token: `response.json()["authToken"]`.
3. Armo un diccionario de headers nuevo, copiando los headers base y agregando `Authorization: Bearer <token>`.
4. Uso ese diccionario de headers en la siguiente solicitud (por ejemplo, crear el kit)
 
## ▶️ Cómo ejecutar las pruebas
 
Ejecutar todas las pruebas del proyecto:
 
```bash
pytest
```
 
Ejecutar un archivo específico:
 
```bash
pytest create_kit_name_kit_test.py
```
 
Ejecutar con más detalle (modo verbose):
 
```bash
pytest -v
```
 

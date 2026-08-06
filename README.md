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
 
   En macOS/Linux:
```bash
   source .venv/bin/activate
```
 
3. Instala las dependencias:
```bash
   pip install pytest requests
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
Algo que aprendí haciendo este proyecto: en las funciones auxiliares siempre copio estos diccionarios con `.copy()` antes de modificarlos. Si no lo hago, estaría modificando el diccionario original de `data.py`, y eso rompería otras pruebas que corran después y esperen los valores originales.
 
### `sender_stand_request.py`
Las funciones que realmente mandan las solicitudes HTTP (`post_new_user`, `post_new_kit`, etc.) usando `requests`. La idea es que mis archivos de test no llamen a `requests` directamente, sino que pasen por aquí — así si algo del endpoint cambia, solo lo ajusto en un lugar.
 
### Archivos de test (`*_test.py`)
Cada archivo de test tiene tres tipos de funciones:
- **Funciones auxiliares** (`get_user_body`, `get_kit_body`, `get_headers`) que arman los bodies y headers que necesito para cada solicitud.
- **Funciones de aserción reutilizables** (`positive_assert`, `negative_assert`) que agrupan el flujo que se repite en varias pruebas: crear usuario → sacar el `authToken` de la respuesta → armar los headers con ese token → probar el endpoint que me interesa.
- **Funciones de prueba** (`test_...`), que son las que `pytest` reconoce y corre automáticamente.
## 🔑 Flujo de autenticación (esto me costó entenderlo al principio)
 
Algunos endpoints, como crear un kit, necesitan que estés "autenticado". El token no se manda a mano ni se guarda fijo en ningún lado — se genera cada vez que creas un usuario nuevo. El flujo que sigo es:
 
1. Creo un usuario con `post_new_user`.
2. De la respuesta (`201`), saco el token: `response.json()["authToken"]`.
3. Armo un diccionario de headers nuevo, copiando los headers base y agregando `Authorization: Bearer <token>`.
4. Uso ese diccionario de headers en la siguiente solicitud (por ejemplo, crear el kit).
Al principio intenté mandar el token como argumento directo de `requests.post()` (algo como `Authorization=auth_token`) y no funcionó — el token va **dentro del diccionario de headers**, no como parámetro suelto de la función.
 
## ▶️ Cómo ejecutar las pruebas
 
**Nota para mi yo del futuro:** las pruebas se corren con `pytest`, NO con `python archivo.py`. La primera vez que corrí el archivo directo con Python, no pasó nada (exit code 0) — porque `def test_...` solo *define* la función, no la ejecuta. `pytest` es quien busca automáticamente todas las funciones que empiezan con `test_` y las corre.
 
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
 
## ✅ Convenciones de nombres
 
- Toda función de prueba tiene que empezar con `test_`, si no, `pytest` la ignora por completo (ni la cuenta, ni la corre).
- Trato de que el nombre describa el escenario y el resultado esperado, por ejemplo:
  - `test_create_kit_user_1_letter_in_name_get_success_response` → nombre válido de 1 carácter, espero éxito (`201`).
  - `test_create_kit_user_512_letter_in_name_get_failure_response` → nombre fuera del límite permitido, espero error (`400`).
> ⚠️ Ya me pasó poner `..._get_success_response` en una prueba que en realidad comprobaba un `400` (usando `negative_assert` por dentro). El test pasaba igual, pero el nombre mentía sobre lo que probaba — y eso confunde muchísimo al leer el reporte de pytest. Ahora reviso siempre que el nombre y el `assert` final digan lo mismo.
 
## 🧪 Casos de prueba que cubrí
 
- Kit con nombre de longitud mínima (1 caracter) y máxima válida (511 caracteres).
- Kit con nombre vacío.
- Kit con nombre que excede el límite permitido (512 caracteres).
- Kit con caracteres especiales, espacios y números en el nombre.
- Kit sin el parámetro `name` en el body (usando `del` sobre el diccionario copiado, no solo un string vacío).
Para los casos de límite (511 vs 512) generé el string con `"a" * 511` en vez de escribirlo a mano — más rápido y sin riesgo de contar mal los caracteres.
 
## 📝 Notas para mí mismo/a
 
- `configuration.py` apunta a un stand específico que puede expirar o cambiar de URL — si algo deja de responder, ese es el primer lugar a revisar.
- Todavía tengo que confirmar en la documentación (`/docs/`) si el formato correcto del header es `Bearer <token>` o algo distinto, y cuál es el límite real de caracteres para `name` — por ahora lo fui probando a base de prueba y error.
- Pendiente: revisar si conviene mover `positive_assert` / `negative_assert` a un archivo compartido si termino teniendo más archivos de test, para no duplicar código.

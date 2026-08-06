import sender_stand_request
import data

# esta función cambia los valores en el parámetro "firstName"
def get_user_body():
    # el diccionario que contiene el cuerpo de solicitud se copia del archivo "data" (datos) para conservar los datos del diccionario de origen
    current_body = data.user_body.copy()
    # Se devuelve un nuevo diccionario con el valor firstName requerido
    return current_body

# Esta función cambia los valores en el parámetro "name"
def get_kit_body(name):
    # El diccionario que contiene el cuerpo de solicitud se copia del archivo "data" (datos) para conservar los datos del diccionario de origen
    current_body = data.kit_body.copy()
    # Se cambia el valor del parámetro name
    current_body["name"] = name
    # Se devuelve un nuevo diccionario con el valor name requerido
    return current_body

# Esta función captura el authToken después de haberse creado un usuario
def get_headers(auth_token):
    # El diccionario que contiene el header de solicitud se copia del archivo "data" (datos) para conservar los datos del diccionario de origen
    current_headers = data.headers.copy()
    # Se agrega "Authorization" con el authToken al diccionario
    current_headers["Authorization"] = f"Bearer {auth_token}"
    # Se devuelve un nuevo diccionario con el authToken
    return current_headers

# Función de prueba positiva
def positive_assert(name):
    # El cuerpo de la solicitud se guarda en la variable user_body
    user_body = get_user_body()
    # El resultado de la solicitud para crear un nuevo usuario o usuaria se guarda en la variable response
    user_response = sender_stand_request.post_new_user(user_body)
    # Comprueba si el código de estado es 201
    assert user_response.status_code == 201
    # El authToken generado al crear un usuario o usuaria se guarda en la variable auth_token
    auth_token = user_response.json()["authToken"]
    # El cuerpo de la solicitud actualizada se guarda en la variable kit_body
    kit_body = get_kit_body(name)
    # El cuerpo de la solicitud actualizada se guarda en la variable headers
    headers = get_headers(auth_token)
    # El resultado de la solicitud para crear un kit se guarda en la variable response
    kit_response = sender_stand_request.post_new_kit(kit_body,headers)
    # Comprueba si el código de estado es 201
    assert kit_response.status_code == 201

# Función de prueba positiva
def negative_assert(name):
    # El cuerpo de la solicitud se guarda en la variable user_body
    user_body = get_user_body()
    # El resultado de la solicitud para crear un nuevo usuario o usuaria se guarda en la variable response
    user_response = sender_stand_request.post_new_user(user_body)
    # Comprueba si el código de estado es 201
    assert user_response.status_code == 201
    # El authToken generado al crear un usuario o usuaria se guarda en la variable auth_token
    auth_token = user_response.json()["authToken"]
    # El cuerpo de la solicitud actualizada se guarda en la variable kit_body
    kit_body = get_kit_body(name)
    # El cuerpo de la solicitud actualizada se guarda en la variable headers
    headers = get_headers(auth_token)
    # El resultado de la solicitud para crear un kit se guarda en la variable response
    kit_response = sender_stand_request.post_new_kit(kit_body,headers)
    # Comprueba si el código de estado es 400
    assert kit_response.status_code == 400

# Esta función elimina el parámetro "name" del cuerpo de la solicitud
def get_kit_body_without_name():
    # El diccionario que contiene el cuerpo de solicitud se copia del archivo "data" (datos) para conservar los datos del diccionario de origen
    current_body = data.kit_body.copy()
    # Se elimina la llave "name" del diccionario
    del current_body["name"]
    # Se devuelve el diccionario sin el parámetro "name"
    return current_body

# Prueba 1. Kit creado con éxito. El parámetro name contiene 1 caracter
def test_create_kit_user_1_letter_in_name_get_success_response():
    positive_assert("a")

# Prueba 2. Kit creado con éxito. El parámetro name contiene 511 caracter
def test_create_kit_user_511_letter_in_name_get_success_response():
    positive_assert("a"*511)

# Prueba 3. Error. El parámetro name está vacio
def test_create_kit_user_empty_name_get_error_response():
    negative_assert("")

# Prueba 4. Error. El parámetro name contiene 512 caracter
def test_create_kit_user_512_letter_in_name_get_error_response():
     negative_assert("a"*512)

# Prueba 5. Kit creado con éxito. El parámetro name contiene un string de caracteres especiales
def test_create_kit_user_has_special_symbol_in_name_get_error_response():
     negative_assert("№%@,")

# Prueba 6. Kit creado con éxito. El parámetro name contiene espacio en el string
def test_create_kit_user_with_space_in_name_get_success_response():
    positive_assert("A Aaa")

# Prueba 7. Kit creado con éxito. El parámetro name contiene numeros en el string
def test_create_kit_user_with_numbers_in_string_in_name_get_success_response():
    positive_assert("123")

# Prueba 8. Error. El parámetro name no está presente en el cuerpo de la solicitud
def test_create_kit_user_without_name_get_error_response():
    negative_assert(get_kit_body_without_name())

# Prueba 9. Error. El parámetro name contiene numeros
def test_create_kit_user_with_numbers_in_name_get_error_response():
    negative_assert(123)
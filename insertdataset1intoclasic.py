import redis
import json

# Conexión a Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Ruta del archivo JSON
file_path = "/home/felipe/Escritorio/Tarea1SD/Proyecto/filtered_data.json"

# Leer el archivo JSON
with open(file_path, 'r') as f:
    try:
        data = json.load(f)  # Cargar el contenido JSON
        
        if not isinstance(data, list):  # Verificar que sea una lista
            print("El archivo JSON no contiene una lista de diccionarios.")
        else:
            for item in data:
                if "EventId" in item and "Type" in item:  # Asegurar que los campos clave existen
                    key = item["COLLISION_ID"]
                    value = item["CRASH DATE"]
                    r.set(key, value)  # Insertar en Redis
                else:
                    print(f"Elemento problemático: {item}")  # Notificar si falta un campo clave
    except json.JSONDecodeError as e:
        print(f"Error decodificando JSON: {e}")


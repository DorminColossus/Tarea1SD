import redis
import json

# Conexión a Redis
r = redis.Redis(host='localhost', port=6380, db=0)  # Ajusta el puerto si es diferente

# Ruta del archivo JSON
file_path = "/home/felipe/Escritorio/Tarea1SD/Proyecto/filtered_data2.json"

# Leer el archivo JSON
with open(file_path, 'r') as f:
    try:
        data = json.load(f)  # Cargar el contenido JSON
        
        if isinstance(data, dict) and "results" in data:
            results = data["results"]  # Extraer la lista de resultados
            for item in results:
                if "COLLISION_ID" in item and "CRASH DATE" in item:
                    key = item["COLLISION_ID"]
                    value = item["CRASH DATE"]
                    r.set(key, value)  # Guardar en Redis
                else:
                    print(f"Elemento con campos faltantes: {item}")  # Advertencia por campos faltantes
        else:
            print("El formato del archivo JSON no es el esperado.")  # Advertencia por formato incorrecto

    except json.JSONDecodeError as e:
        print(f"Error decodificando JSON: {e}")  # Error de decodificación JSON


import redis
import zlib  # Para la función CRC32
import json  # Para trabajar con archivos JSON

# Función para obtener el índice de partición
def get_partition(key, num_partitions):
    # Calcula el hash de la clave utilizando CRC32
    hash_value = zlib.crc32(key.encode('utf-8'))
    # Determina el índice de la partición
    partition_index = hash_value % num_partitions
    return partition_index

# Conexión a las instancias de Redis
redis_connections = [
    redis.Redis(host='localhost', port=6381),  # Partición 1
    redis.Redis(host='localhost', port=6382),  # Partición 2
    redis.Redis(host='localhost', port=6383),  # Partición 3
]

# Ruta del archivo JSON
file_path = "/home/felipe/Escritorio/Tarea1SD/Proyecto/filtered_data.json"

# Leer el archivo JSON
with open(file_path, 'r') as f:
    data = json.load(f)  # Cargar el contenido JSON

# Asignar cada elemento del dataset a su partición correspondiente
for item in data:
    if "EventId" in item and "Type" in item:
        key = str(item["EventId"])  # Clave
        value = item["Type"]  # Valor
        # Obtener la partición utilizando la función hash
        partition_index = get_partition(key, len(redis_connections))
        redis_instance = redis_connections[partition_index]
        # Insertar clave-valor en la partición correspondiente
        redis_instance.set(key, value)  # Almacenar clave-valor
        print(f"Inserted key {key} with value {value} into partition {partition_index}")


import json
from PIL import Image
from pdf417decoder import PDF417Decoder

# Cargar la base de datos de DNIs desde el archivo JSON
with open("dni_registrados.json", "r", encoding="utf-8") as file:
    dni_db = json.load(file)

# Ruta de la imagen del DNI
image_path = "front.jpg"  # Cambia esto por la ruta real

# Cargar la imagen
image = Image.open(image_path)

# Crear el decodificador
decoder = PDF417Decoder(image)

# Intentar decodificar la imagen
barcode_count = decoder.decode()

# Mostrar los resultados
if barcode_count > 0:
    for i in range(barcode_count):
        decoded_text = decoder.barcode_data_index_to_string(i)
        print(f"Mensaje decodificado ({i + 1}): {decoded_text}")

        # Separar los datos del código de barras (asumiendo que están separados por "@")
        datos = decoded_text.split("@")
        dni_decodificado = datos[0] if len(datos) > 0 else None  # El primer dato debería ser el DNI

        if dni_decodificado and dni_decodificado in dni_db:
            print(f"✅ DNI {dni_decodificado} encontrado en la base de datos.")
        else:
            print(f"❌ DNI {dni_decodificado} no compatible.")
else:
    print("No se encontraron códigos de barras PDF417 en la imagen.")

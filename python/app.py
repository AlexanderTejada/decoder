import json
import streamlit as st
from PIL import Image
from pdf417decoder import PDF417Decoder

# Cargar la base de datos de DNIs
with open("dni_registrados.json", "r", encoding="utf-8") as file:
    dni_db = json.load(file)

# Configurar la página con modo oscuro
st.set_page_config(page_title="Verificación de DNI", layout="centered")

# Estilos personalizados con MODO OSCURO
st.markdown("""
    <style>
        .stApp { background-color: #0e1117; color: white; }
        .title { font-size: 28px; font-weight: bold; text-align: center; color: #ffffff; }
        .subtitle { font-size: 18px; text-align: center; color: #aaaaaa; margin-bottom: 20px; }
        .valid-dni { background-color: #198754; color: white; padding: 10px; border-radius: 5px; text-align: center; }
        .invalid-dni { background-color: #dc3545; color: white; padding: 10px; border-radius: 5px; text-align: center; }
        .data-box { background-color: #1e222a; padding: 15px; border-radius: 5px; border: 1px solid #2a2f38; margin-top: 10px; color: white; }
        .stFileUploader label { font-size: 18px !important; font-weight: bold !important; background-color: #1e88e5 !important; color: white !important; padding: 10px !important; border-radius: 8px !important; text-align: center !important; display: block !important; cursor: pointer !important; }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<p class="title">Verificación de DNI PDF417</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Sube una imagen con un código de barras PDF417 y verifica si el DNI es válido</p>', unsafe_allow_html=True)

# Subir imagen
uploaded_file = st.file_uploader("📤 **Selecciona una imagen del DNI**", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Mostrar la imagen cargada con el parámetro corregido
    image = Image.open(uploaded_file)
    st.image(image, caption="🖼️ Imagen subida", use_container_width=True)

    # Decodificar código de barras
    decoder = PDF417Decoder(image)
    barcode_count = decoder.decode()

    if barcode_count > 0:
        st.markdown(f"<p class='data-box'>📌 Se encontraron {barcode_count} código(s) de barras en la imagen.</p>", unsafe_allow_html=True)

        for i in range(barcode_count):
            decoded_text = decoder.barcode_data_index_to_string(i)
            st.markdown(f"<p class='data-box'><strong>📜 Mensaje decodificado:</strong><br>{decoded_text}</p>", unsafe_allow_html=True)

            # Separar los datos del código de barras
            datos = decoded_text.split("@")
            dni_real = datos[4] if len(datos) > 4 else None  # El DNI está en la posición 4

            # **Corrección**: Buscar el DNI dentro de los valores del JSON
            dni_encontrado = None
            for tramite, info in dni_db.items():
                if info["dni"] == dni_real:
                    dni_encontrado = info
                    break

            # Verificar si el DNI está en la base de datos
            if dni_encontrado:
                st.markdown(f"<p class='valid-dni'>✅ <strong>DNI {dni_real} es válido.</strong></p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p class='invalid-dni'>❌ <strong>DNI {dni_real} no es válido.</strong></p>", unsafe_allow_html=True)
    else:
        st.markdown('<p class="invalid-dni">⚠ No se encontraron códigos de barras PDF417 en la imagen.</p>', unsafe_allow_html=True)

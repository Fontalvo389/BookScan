import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

import streamlit as st
import tempfile
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
from langchain_ollama import ChatOllama

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# pytesseract.pytesseract.tesseract_cmd = r'C:\Archivos de programa\Tesseract-OCR\tesseract.exe'

st.set_page_config(page_title="DocuScan", layout="centered")
st.title("📰 BookScan - Clasificador de Libros")

st.write("Sube una imagen o PDF, extraeré el texto y clasificaré el libro por categoría, te dire el autor y responderé preguntas acerca del libro.")

#configuracion de los modelos
with st.sidebar:
    st.header("⚙️ Configuración del modelo")
    modelo_seleccionado = st.selectbox(
        "Modelo:", ["gemma3:4b", "llama3:latest", "llama3.2:latest"],
        index=1
    )
    temperatura = st.slider("Temperatura", 0.0, 1.0, 0.5)
    max_tokens = st.slider("Máx. tokens", 64, 4096, 256)

llm = ChatOllama(
    model=modelo_seleccionado,
    temperature=temperatura,
    num_predict=max_tokens,
)

# chat inicio
with st.chat_message("assistant"):
    st.markdown("👋 Sube un PDF o imagen de un libro para clasificarlo automaticamente.")

uploaded_file = st.file_uploader("📁 Archivo PDF o imágen", type=["pdf", "png", "jpg", "jpeg"])
texto_extraido = ""
titulo = ""

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    if uploaded_file.type == "application/pdf":
        pages = convert_from_path(tmp_path)
        st.image(pages[0], caption="Vista previa PDF", use_container_width=True)
        texto_extraido = pytesseract.image_to_string(pages[0], lang="spa")
    else:
        img = Image.open(tmp_path)
        st.image(img, caption="Imagen cargada", use_column_width=True)
        texto_extraido = pytesseract.image_to_string(img, lang="spa")

    st.subheader("📝 Texto detectado:")
    st.text_area("Texto OCR", value=texto_extraido, height=300)

    lineas = texto_extraido.strip().split('\n')
    titulo = next((line for line in lineas if len(line.strip()) > 30), lineas[0] if lineas else "")


#Clasificacion del libro
if titulo and st.button("Clasificar y detectar título/autor"):
    prompt = f"""
Eres un asistente que analiza portadas de libros. A partir del siguiente texto detectado por OCR, extrae lo siguiente:
1. Título del libro.
2. Nombre del autor o autores, si están presentes.
3. Clasificación temática del libro. Elige una sola categoría entre:
- Política
- Economía
- Deportes
- Internacional
- Salud
- Tecnología
- Novela
- Autoayuda
- Historia
- Ciencia
- Biografía
- Fantasía
- Ciencia ficción

Texto detectado:
\"\"\"{texto_extraido}\"\"\"

Responde en el siguiente formato:
Título: <título detectado>
Autor: <autor detectado o "No disponible">
Categoría: <una categoría>
"""

    with st.spinner("Analizando..."):
        try:
            respuesta = llm.invoke([{"role": "user", "content": prompt}]).content.strip()
            st.session_state.resultado_clasificacion = respuesta
            st.success("✅ Análisis completado")
            st.markdown("### 📚 Resultado del análisis:")
            st.markdown(f"```\n{respuesta}\n```")
        except Exception as e:
            st.error(f"❌ Error al procesar la clasificación: {e}")
            
            
if "resultado_clasificacion" in st.session_state:
    st.markdown("### 📚 Resultado del análisis (anterior):")
    st.markdown(f"```\n{st.session_state.resultado_clasificacion}\n```")           



#chat libro

if titulo and texto_extraido:
    st.divider()
    st.subheader("💬 Chat sobre el libro")

    if "chat_historial" not in st.session_state:
        st.session_state.chat_historial = []

    user_input = st.chat_input("Haz tu pregunta:")

    if user_input:
        #prompt para solo el libro tipo embeding
        system_prompt = f"""
Eres un experto literario. Solo puedes responder preguntas relacionadas con el siguiente libro:

Título: {titulo}
Texto extraído por OCR (fragmento):
\"\"\"{texto_extraido[:2000]}\"\"\"

No respondas preguntas fuera de este contexto. Si no sabes la respuesta, simplemente di "No tengo suficiente información en el texto para responder eso".
"""

        with st.chat_message("user"):
            st.write(user_input)

        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ]

            with st.spinner("🧠 El modelo está pensando..."):
                response = llm.invoke(messages)

                
                st.session_state.chat_historial.append({
                    "role": "user",
                    "content": user_input
                })
                st.session_state.chat_historial.append({
                    "role": "assistant",
                    "content": response.content
                })

                
                with st.chat_message("assistant"):
                    st.write(response.content)

        except Exception as e:
            st.error(f"Error al responder: {e}")

  
    for msg in st.session_state.chat_historial:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])




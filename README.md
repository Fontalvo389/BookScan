📚 BookScan
BookScan es una aplicación interactiva basada en Streamlit que permite:

Subir una imagen o PDF de la portada de un libro.

Aplicar OCR con Tesseract para extraer el texto.

Clasificar el libro automáticamente usando modelos LLM locales vía Ollama.

Detectar título y autor.

Chatear sobre el contenido del libro.

🚀 ¿Cómo funciona?
Subida del archivo (imagen o PDF) mediante la interfaz Streamlit.

OCR: Se extrae texto con pytesseract.

Clasificación automática: Se construye un prompt y se consulta un LLM (como llama3) mediante langchain_ollama.

Chat: Puedes hacer preguntas relacionadas con el contenido extraído.

🧠 Modelos compatibles
Seleccionables desde la interfaz:

gemma3:4b

llama3:latest

llama3.2:latest

(Ollama debe tenerlos instalados previamente en tu máquina).

🛠️ Requisitos
Python 3.11+

Tesseract OCR instalado localmente (ej. en C:\Program Files\Tesseract-OCR\tesseract.exe)

Ollama instalado con los modelos cargados

Librerías de Python:

bash
Copiar
Editar
uv pip install streamlit pillow pdf2image pytesseract langchain langchain_ollama
📂 Estructura del proyecto
csharp
Copiar
Editar
📁 taller1/
├── 📁 backend/
│   └── clasificador.py
├── Makefile
├── pyproject.toml
├── uv.lock
⚠️ El directorio .venv/ no se debe subir a GitHub. Asegúrate de incluirlo en .gitignore.

▶️ Ejecución
Para lanzar la aplicación:

bash
Copiar
Editar
make clasi
Asegúrate de que el puerto 8502 esté libre.

O manualmente:

bash
Copiar
Editar
uv run streamlit run backend/clasificador.py --server.port 8502
🧼 Limpieza antes de subir a GitHub
✅ Elimina el directorio .venv/

✅ Incluye un .gitignore con al menos:

csharp
Copiar
Editar
.venv/
__pycache__/
*.pyc
uv.lock
✅ No incluyas archivos grandes o innecesarios.

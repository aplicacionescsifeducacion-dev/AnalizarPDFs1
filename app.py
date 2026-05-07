from flask import Flask, request, jsonify
import fitz
import re
from collections import defaultdict
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

REGEX_ESPECIALIDAD = re.compile(r"ESPECIALIDAD\s*:\s*(.+)", re.IGNORECASE)
REGEX_SI = re.compile(r"\b(04)\b", re.IGNORECASE)

@app.route('/')
def index():
    return jsonify({"status": "API funcionando"})

@app.route('/analizar', methods=['POST'])
def analizar():
    try:
        if request.headers.get("API-KEY") != "12345":
            return jsonify({"error": "No autorizado"}), 403

        if 'pdf' not in request.files:
            return jsonify({"error": "No PDF recibido"}), 400

        archivo = request.files['pdf']
        pdf_bytes = archivo.read()

        resultados = defaultdict(lambda: {"total": 0, "admitidos": 0})
        especialidad_actual = None

        with fitz.open(stream=pdf_bytes, filetype="pdf") as pdf:
            for i, pagina in enumerate(pdf):
                texto = pagina.get_text()

                if not texto:
                    print(f"Página {i} sin texto")
                    continue

                for linea in texto.split("\n"):
                    linea = linea.strip()

                    # DEBUG 👇 (puedes quitar luego)
                    print("LINEA:", linea)

                    match = REGEX_ESPECIALIDAD.search(linea)
                    if match:
                        especialidad_actual = match.group(1).strip()
                        print("Especialidad detectada:", especialidad_actual)
                        continue

                    if REGEX_SI.search(linea):
                        if especialidad_actual:
                            resultados[especialidad_actual]["total"] += 1
                            resultados[especialidad_actual]["admitidos"] += 1

        return jsonify(resultados)

    except Exception as e:
        return jsonify({
            "error": str(e),
            "type": type(e).__name__
        }), 500

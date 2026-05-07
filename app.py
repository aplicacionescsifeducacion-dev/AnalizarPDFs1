from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "API activa"

@app.route("/analizar", methods=["POST"])
def analizar():
    return jsonify({"ok": True})
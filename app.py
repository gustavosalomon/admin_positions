



# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

# --- Configuración de MongoDB Atlas ---
# REEMPLAZA con tu URI de Mongo Atlas
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["smart_parking_web"]
collection = db["admin_positions"]

# --- Guardar posiciones (POST) ---
@app.route("/api/admin/save-positions", methods=["POST"])
def save_positions():
    try:
        data = request.json
        if not isinstance(data, list):
            return jsonify({"error": "Formato inválido, se esperaba una lista"}), 400
        # Limpiamos la colección y guardamos nuevas posiciones
        collection.delete_many({})
        collection.insert_many(data)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Obtener posiciones (GET) ---
@app.route("/api/admin/get-positions", methods=["GET"])
def get_positions():
    try:
        docs = list(collection.find({}, {"_id": 0}))
        return jsonify(docs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Ejecutar ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

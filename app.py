from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

# Conexión a Mongo Atlas
MONGO_URI = os.environ.get("MONGO_URI")  # Configura en Render
client = MongoClient(MONGO_URI)
db = client.smartparking
collection = db.admin_positions

# Guardar posiciones
@app.route("/api/admin/save-positions", methods=["POST"])
def save_positions():
    data = request.json
    if not data.get("positions"):
        return jsonify({"error": "No se recibieron posiciones"}), 400

    # Limpiar colección antes de guardar
    collection.delete_many({})
    collection.insert_one({"positions": data["positions"]})
    return jsonify({"ok": True})

# Obtener posiciones
@app.route("/api/admin/get-positions", methods=["GET"])
def get_positions():
    doc = collection.find_one()
    return jsonify(doc if doc else {"positions": []})

if __name__ == "__main__":
    app.run(debug=True)

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError("❌ Falta definir la variable de entorno MONGO_URI en Render")

client = MongoClient(MONGO_URI)
db = client["smart_parking_web"]
col = db["admin_positions"]

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "🛠️ Admin Positions API funcionando correctamente"})

# Obtener todas las posiciones
@app.route("/api/admin/get-positions", methods=["GET"])
def get_positions():
    positions = list(col.find({}, {"_id": 0}))  # Excluir _id para evitar conflictos en el cliente
    return jsonify(positions)

# Guardar múltiples posiciones (actualiza si ya existen por id + collection)
@app.route("/api/admin/save-positions", methods=["POST"])
def save_positions():
    data = request.get_json()
    if not isinstance(data, list):
        return jsonify({"success": False, "error": "Formato inválido: se esperaba una lista"}), 400

    for pos in data:
        if not all(k in pos for k in ("id", "lat", "lng", "collection")):
            return jsonify({"success": False, "error": "Faltan campos en algunas posiciones"}), 400
        
        # Buscar y actualizar por combinación única: id + collection
        col.update_one(
            {"id": pos["id"], "collection": pos["collection"]},
            {"$set": {
                "nombre": pos.get("nombre", pos["id"]),
                "lat": pos["lat"],
                "lng": pos["lng"]
            }},
            upsert=True
        )

    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


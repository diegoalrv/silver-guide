from flask import Flask, request, jsonify
from flask_cors import CORS  # Importar CORS

app = Flask(__name__)
CORS(app)  # Inicializar CORS con la app de Flask

# Estado inicial
movement_data = {
    "new_movement": False,
    "axis": None,
    "steps": 0
}

# Endpoint para consultar el movimiento
@app.route('/get_movement', methods=['GET'])
def get_movement():
    global movement_data
    response = movement_data
    movement_data["new_movement"] = False
    return jsonify(response)

# Endpoint para actualizar el movimiento
@app.route('/update_movement', methods=['POST'])
def update_movement():
    global movement_data
    data = request.json
    movement_data = {
        "new_movement": True,
        "axis": data["axis"],
        "steps": data["steps"]
    }
    return jsonify({"message": "Movement updated"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

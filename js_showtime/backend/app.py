from flask import Flask, request, jsonify
from flask_cors import CORS  # Importar CORS

app = Flask(__name__)
CORS(app)  # Inicializar CORS con la app de Flask

new_movement = {'state': False}

# Estado inicial
movement_data = {
    "axis": None,
    "steps": 0
}

@app.route('/is_new_movement', methods=['GET'])
def is_new_movement():
    global new_movement
    return jsonify(new_movement)

@app.route('/move_applied', methods=['POST'])
def move_applied():
    global new_movement
    new_movement['state'] = False
    return jsonify(new_movement)

# Endpoint para consultar el movimiento
@app.route('/get_movement', methods=['GET'])
def get_movement():
    global movement_data
    response = movement_data
    return jsonify(response)

# Endpoint para actualizar el movimiento
@app.route('/update_movement', methods=['POST'])
def update_movement():
    global movement_data, new_movement
    data = request.json
    movement_data = {
        "axis": data["axis"],
        "steps": data["steps"],
        
    }
    new_movement['state'] = True
    return jsonify({"message": "Movement updated"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

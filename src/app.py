"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()
    
    # Validaciones básicas
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    required = ['first_name', 'age', 'lucky_numbers']
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400
    
    # Validar tipos de datos
    if not isinstance(data['first_name'], str):
        return jsonify({"error": "first_name must be a string"}), 400
        
    if not isinstance(data['age'], int) or data['age'] <= 0:
        return jsonify({"error": "age must be a positive integer"}), 400
        
    if not isinstance(data['lucky_numbers'], list):
        return jsonify({"error": "lucky_numbers must be a list"}), 400
    
    # Agregar el miembro
    new_member = jackson_family.add_member(data)
    return jsonify(new_member), 200

# CAMBIO IMPORTANTE: Cambiar '/member/<int:member_id>' por '/members/<int:member_id>'
@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"error": "Member not found"}), 404

# CAMBIO IMPORTANTE: Cambiar '/member/<int:member_id>' por '/members/<int:member_id>'
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = jackson_family.get_member(member_id)
    if not member:
        return jsonify({"error": "Member not found"}), 404
        
    jackson_family.delete_member(member_id)
    return jsonify({"done": True}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

from flask import request, jsonify
from app.models import db, Inventory
from . import inventory_bp
from .schemas import inventory_schema, inventories_schema
from marshmallow import ValidationError

@inventory_bp.route('/', methods=['POST'])
def add_inventory():
    try:
        data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    part = Inventory(**data)
    db.session.add(part)
    db.session.commit()
    return inventory_schema.jsonify(part), 201

@inventory_bp.route('/', methods=['GET'])
def get_inventory():
    parts = Inventory.query.all()
    return inventories_schema.jsonify(parts), 200

@inventory_bp.route('/<int:part_id>', methods=['GET'])
def get_inventory_by_id(part_id):
    part = Inventory.query.get(part_id)
    if not part:
        return jsonify({"error": "Part not found"}), 404
    return inventory_schema.jsonify(part), 200

@inventory_bp.route('/<int:part_id>', methods=['PUT'])
def update_inventory(part_id):
    part = Inventory.query.get(part_id)
    if not part:
        return jsonify({"error": "Part not found"}), 404
    try:
        data = inventory_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400
    for key, value in data.items():
        setattr(part, key, value)
    db.session.commit()
    return inventory_schema.jsonify(part), 200

@inventory_bp.route('/<int:part_id>', methods=['DELETE'])
def delete_inventory(part_id):
    part = Inventory.query.get(part_id)
    if not part:
        return jsonify({"error": "Part not found"}), 404
    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": "Part deleted"}), 200
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select, func
from app.models import db, Mechanic, ServiceMechanic
from . import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema

# Create a new Mechanic
@mechanics_bp.route('/', methods=['POST'])
def add_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_mechanic = Mechanic(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201

# Get all Mechanics
@mechanics_bp.route('/', methods=['GET'])
def get_mechanics():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(mechanics)

# Get Mechanic by ID
@mechanics_bp.route('/<int:id>', methods=['GET'])
def get_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    return mechanic_schema.jsonify(mechanic), 200

# Update Mechanic by ID
@mechanics_bp.route('/<int:id>', methods=['PUT'])
def update_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    try:
        mechanic_data = mechanic_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200

# Delete Mechanic by ID
@mechanics_bp.route('/<int:id>', methods=['DELETE'])
def delete_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": "Mechanic deleted successfully"}), 200


# Most active Mechanics
@mechanics_bp.route('/most-active', methods=['GET'])
def most_active_mechanics():
    results = (
        db.session.query(Mechanic, func.count(ServiceMechanic.ticket_id).label('ticket_count'))
        .outerjoin(ServiceMechanic, Mechanic.id == ServiceMechanic.mechanic_id)
        .group_by(Mechanic.id)
        .order_by(func.count(ServiceMechanic.ticket_id).desc())
        .all()
    )
    mechanics = [row[0] for row in results]
    return mechanics_schema.jsonify(mechanics), 200
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import db, ServiceTicket, Mechanic, Inventory, ServiceMechanic
from . import service_tickets_bp
from .schemas import service_ticket_schema, service_tickets_schema

# Create a new Service Ticket
@service_tickets_bp.route('/', methods=['POST'])
def add_service_ticket():
    try:
        ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_ticket = ServiceTicket(**ticket_data)
    db.session.add(new_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_ticket), 201

# Assign Mechanic to Service Ticket
@service_tickets_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not ticket or not mechanic:
        return jsonify({"error": "Ticket or Mechanic not found"}), 404

    if mechanic not in [sm.mechanic for sm in ticket.mechanics]:
        from app.models import ServiceMechanic
        ticket.mechanics.append(ServiceMechanic(mechanic=mechanic))
        db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200

# Remove Mechanic from Service Ticket
@service_tickets_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    # Find the ServiceMechanic association
    service_mechanic = next((sm for sm in ticket.mechanics if sm.mechanic_id == mechanic_id), None)
    if not service_mechanic:
        return jsonify({"error": "Mechanic not assigned to this ticket"}), 404

    # Remove the association from the session
    db.session.delete(service_mechanic)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200

# Get all Service Tickets
@service_tickets_bp.route('/', methods=['GET'])
def get_service_tickets():
    query = select(ServiceTicket)
    tickets = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(tickets)

# Inventory Management for Service Tickets
@service_tickets_bp.route('/<int:ticket_id>/add-part/<int:part_id>', methods=['PUT'])
def add_part_to_ticket(ticket_id, part_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    part = db.session.get(Inventory, part_id)
    if not ticket or not part:
        return jsonify({"error": "Ticket or part not found"}), 404
    return jsonify({"message": "Part added to ticket"}), 200

@service_tickets_bp.route('/<int:ticket_id>/edit', methods=['PUT'])
def edit_ticket_mechanics(ticket_id):
    data = request.json
    add_ids = data.get('add_ids', [])
    remove_ids = data.get('remove_ids', [])

    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    # Remove mechanics
    for mech_id in remove_ids:
        assoc = next((sm for sm in ticket.mechanics if sm.mechanic_id == mech_id), None)
        if assoc:
            db.session.delete(assoc)

    # Add mechanics
    for mech_id in add_ids:
        mechanic = db.session.get(Mechanic, mech_id)
        if mechanic and not any(sm.mechanic_id == mech_id for sm in ticket.mechanics):
            ticket.mechanics.append(ServiceMechanic(mechanic=mechanic))

    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200
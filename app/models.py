from app.extensions import db

# --- Customer Model ---
class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    tickets = db.relationship("ServiceTicket", back_populates="customer")

# --- ServiceTicket Model ---
class ServiceTicket(db.Model):
    __tablename__ = 'service_ticket'
    id = db.Column(db.Integer, primary_key=True)
    VIN = db.Column(db.String(50), nullable=False)
    service_date = db.Column(db.DateTime, nullable=False)
    service_desc = db.Column(db.String(255), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    customer = db.relationship("Customer", back_populates="tickets")
    mechanics = db.relationship("ServiceMechanic", back_populates="ticket")
    parts = db.relationship('Inventory', secondary='service_part', back_populates='tickets')

# --- Mechanic Model ---
class Mechanic(db.Model):
    __tablename__ = 'mechanic'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    tickets = db.relationship("ServiceMechanic", back_populates="mechanic")

# --- ServiceMechanic Junction Table ---
class ServiceMechanic(db.Model):
    __tablename__ = 'service_mechanic'
    ticket_id = db.Column(db.Integer, db.ForeignKey('service_ticket.id'), primary_key=True)
    mechanic_id = db.Column(db.Integer, db.ForeignKey('mechanic.id'), primary_key=True)
    ticket = db.relationship("ServiceTicket", back_populates="mechanics")
    mechanic = db.relationship("Mechanic", back_populates="tickets")

# --- ServicePart Junction Table ---
class ServicePart(db.Model):
    __tablename__ = 'service_part'
    service_ticket_id = db.Column(db.Integer, db.ForeignKey('service_ticket.id'), primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), primary_key=True)

# --- Inventory Model ---
class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    tickets = db.relationship(
        'ServiceTicket',
        secondary='service_part',
        back_populates='parts'
    )
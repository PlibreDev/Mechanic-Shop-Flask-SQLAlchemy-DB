from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from marshmallow import ValidationError, schema, fields
from sqlalchemy import select


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:pj627129@localhost:3306/mechanic_db'


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
ma = Marshmallow()
db.init_app(app)
ma.init_app(app)

class Customer(Base):
    __tablename__ = 'customer'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.VARCHAR(50), nullable=False)
    email: Mapped[str] = mapped_column(db.VARCHAR(100), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(db.VARCHAR(15), nullable=False)
    tickets: Mapped[list["ServiceTicket"]] = relationship("ServiceTicket", back_populates="customer")

class ServiceTicket(Base):
    __tablename__ = 'service_ticket'
    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[str] = mapped_column(db.VARCHAR(50), nullable=False)
    service_date: Mapped[str] = mapped_column(db.DateTime, nullable=False)
    service_desc: Mapped[str] = mapped_column(db.VARCHAR(255), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customer.id'), nullable=False)
    customer: Mapped["Customer"] = relationship("Customer", back_populates="tickets")
    mechanics: Mapped[list["ServiceMechanic"]] = relationship("ServiceMechanic", back_populates="ticket")

class Mechanic(Base):
    __tablename__ = 'mechanic'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.VARCHAR(50), nullable=False)
    email: Mapped[str] = mapped_column(db.VARCHAR(100), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(db.VARCHAR(15), nullable=False)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)
    tickets: Mapped[list["ServiceMechanic"]] = relationship("ServiceMechanic", back_populates="mechanic")

class ServiceMechanic(Base):
    __tablename__ = 'service_mechanic'
    ticket_id: Mapped[int] = mapped_column(db.ForeignKey('service_ticket.id'), primary_key=True)
    mechanic_id: Mapped[int] = mapped_column(db.ForeignKey('mechanic.id'), primary_key=True)
    ticket: Mapped["ServiceTicket"] = relationship("ServiceTicket", back_populates="mechanics")
    mechanic: Mapped["Mechanic"] = relationship("Mechanic", back_populates="tickets")

with app.app_context():
    db.create_all()

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

@app.route('/customers', methods=['POST'])  
def add_customer():
    if not request.json:
        return jsonify({"message": "No input data provided"}), 400
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Customer).where(Customer.email == customer_data.email)
    existing_customer = db.session.execute(query).scalars().all()
    if existing_customer:
        return jsonify({"message": "Customer already exists"}), 400

    db.session.add(customer_data)
    db.session.commit()
    return jsonify(customer_schema.dump(customer_data)), 201

app.run()
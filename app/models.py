from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)



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



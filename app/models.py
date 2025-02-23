from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from sqlalchemy import Date, cast, extract, func
from datetime import datetime
from fasthtml.common import *

from app.database import Base, session, engine

@dataclass
class Tickets(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    fechacreacion = Column(DateTime, default=datetime.utcnow)
    fechamodificacion = Column(DateTime, default=datetime.utcnow)
    titulo = Column(String)
    descripcion = Column(String)
    prioridad = Column(String)
    step = Column(Integer, default=0)
    departmento = Column(String)

def get_all_tickets():
    result = session.query(Tickets).with_entities(
        Tickets.id.label('id'),
        Tickets.titulo.label('title'),
        Tickets.descripcion.label('description'),
        Tickets.prioridad.label('prioridad'),
        Tickets.step.label('step'),
        Tickets.departmento.label('department'),
        Tickets.fechacreacion.label('fechacreacion'),
        Tickets.fechamodificacion.label('fechamodificacion')
        ).order_by(Tickets.id.desc()).all()
    valores = []
    for i in range(len(result)):
        valores.append({
            'id': 'TK-' + "{:03d}".format(result[i][0]), 
            'title': result[i][1],
            'description': result[i][2],
            'prioridad': result[i][3],
            'step': int(result[i][4]),
            'department': result[i][5],
            'fechacreacion': result[i][6],
            'fechamodificacion': result[i][7],
            })
    return(valores)

def new_ticket(valores):
    ticket = Tickets(
        titulo = valores['titulo'],
        descripcion = valores['descripcion'],
        prioridad = valores['prioridad'],
        departmento = valores['departmento'],
        ) 
    session.add(ticket)
    session.commit()

def update_ticket(valores):
    ticket = session.query(Tickets).filter(Tickets.id == valores['id']).one()
    ticket.titulo = valores['titulo']
    ticket.descripcion = valores['descripcion']
    ticket.prioridad = valores['prioridad']
    ticket.step = valores['step']
    ticket.departmento = valores['departmento']
    ticket.fechamodificacion = valores['fechamodificacion']
    session.commit()

def delete_ticket(valores):
    ticket = session.query(Tickets).filter(Tickets.id == valores['id']).one()
    session.delete(ticket)
    session.commit()
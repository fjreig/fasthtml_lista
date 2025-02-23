from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from sqlalchemy import Date, cast, extract, func
from datetime import datetime
from fasthtml.common import *

from app.database import Base, session, engine

@dataclass
class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    fechacreacion = Column(DateTime, default=datetime.utcnow)
    fechamodificacion = Column(DateTime, default=datetime.utcnow)
    selected = Column(String)
    titulo = Column(String)
    estado = Column(String)
    prioridad = Column(String)

def get_all_tasks():
    result = session.query(Tasks).with_entities(
        Tasks.id.label('id'),
        Tasks.selected.label('selected'),
        Tasks.titulo.label('title'),
        Tasks.estado.label('status'),
        Tasks.prioridad.label('priority'),
        Tasks.fechacreacion.label('fechacreacion'),
        Tasks.fechamodificacion.label('fechamodificacion')
        ).order_by(Tasks.id.asc()).all()
    valores = []
    for i in range(len(result)):
        valores.append({
            'id': result[i][0], 
            'selected': result[i][1], 
            'title': result[i][2],
            'status': result[i][3],
            'priority': result[i][4],
            'fechacreacion': result[i][5],
            'fechamodificacion': result[i][6],
            })
    return(valores)

def get_count_priority_tasks():
    result = session.query(Tasks.prioridad, 
        func.count(Tasks.prioridad)).group_by(Tasks.prioridad).all()
    valores = []
    for i in result:
        valores.append({'priority': i[0], 'count': i[1] })
    return(valores)

def get_count_status_tasks():
    result = session.query(Tasks.estado, 
        func.count(Tasks.estado)).group_by(Tasks.estado).all()
    valores = []
    for i in result:
        valores.append({'status': i[0], 'count': i[1] })
    return(valores)

def get_count_rows():
    result = session.query(func.count(Tasks.id)).all()
    return(result[0][0])

def new_task(valores):
    ticket = Tasks(
        selected = valores['selected'],
        titulo = valores['titulo'],
        estado = valores['estado'],
        prioridad = valores['prioridad'],
        ) 
    session.add(ticket)
    session.commit()

def update_task(valores):
    ticket = session.query(Tasks).filter(Tasks.id == valores['id']).one()
    ticket.titulo = valores['titulo']
    ticket.descripcion = valores['descripcion']
    ticket.prioridad = valores['prioridad']
    ticket.step = valores['step']
    ticket.departmento = valores['departmento']
    ticket.fechamodificacion = valores['fechamodificacion']
    session.commit()

def delete_task(valores):
    ticket = session.query(Tasks).filter(Tasks.id == valores['id']).one()
    session.delete(ticket)
    session.commit()
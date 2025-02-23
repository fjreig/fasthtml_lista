from fasthtml import FastHTML
from pathlib import Path
from fasthtml.common import *
from monsterui.all import *
from datetime import datetime

from app.database import  session
from app.models import new_task, update_task, delete_task
from app.lista import page_heading, tasks_ui, CreateTaskModal

hdrs = (Theme.blue.headers())
app, rt = fast_app(hdrs=hdrs)

@dataclass
class New_Task:
    selected: str
    titulo: str
    estado: str
    prioridad: str

@dataclass
class Update_Task:
    id: str
    titulo: str
    departmento: str
    prioridad: str
    step: str
    descripcion: str

@dataclass
class Delete_Task:
    id: str

@rt('/')
def index():
    return Container(page_heading, tasks_ui, CreateTaskModal())

@rt("/register")
def post(ticket: New_Task):
    valores = ticket.__dict__
    new_task(valores)
    return Redirect(f"/")

@rt("/update")
def post(ticket: Update_Task):
    valores = ticket.__dict__
    valores.update(id=int(valores['id'].removeprefix('TK-')))
    valores.update(step=list(valor_status.keys())[list(valor_status.values()).index(valores['step'])])
    valores.update(fechamodificacion=datetime.now())
    update_task(valores)
    return Redirect(f"/")

@rt("/borrar")
def post(ticket: Delete_Task):
    valores = ticket.__dict__
    valores.update(id=int(valores['id'].removeprefix('TK-')))
    delete_task(valores)
    return Redirect(f"/")

serve()
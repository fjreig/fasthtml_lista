
from fasthtml.common import *
from monsterui.all import *

from app.models import get_all_tickets

valor_status = {0: "Creado", 1: "Asignado", 2: "En revisión", 3: "En proceso", 4: "Resuelto"}

app, rt = fast_app(hdrs=Theme.blue.headers(daisy=True))

def TicketSteps(step):
    return Steps(
        LiStep("Asignado", data_content="📝",
               cls=StepT.success if step > 0 else StepT.primary if step == 0 else StepT.neutral),
        LiStep("En revisión", data_content="🔎",
               cls=StepT.success if step > 1 else StepT.primary if step == 1 else StepT.neutral),
        LiStep("En proceso", data_content="⚙️",
               cls=StepT.success if step > 2 else StepT.primary if step == 2 else StepT.neutral),
        LiStep("Resuelto", data_content="✅",
               cls=StepT.success if step > 3 else StepT.primary if step == 3 else StepT.neutral),
        cls="w-full")

def StatusBadge(status):
    styles = {'Alta': AlertT.error, 'Media': AlertT.warning,'Baja': AlertT.info}
    alert_type = styles.get(status, AlertT.info)
    return Alert(f"Prioridad {status.title()}", cls=(alert_type,"w-32 shadow-sm"))

def TicketCard(id, title, description, prioridad, step, department, fechacreacion, fechamodificacion):
    return Card(
        CardHeader(
            DivFullySpaced(
                Div(H3(f"#{id}", cls=TextT.muted, name="id_ticket"), 
                    H4(title), 
                    cls='space-y-2'),
                StatusBadge(prioridad))),
        CardBody(
            P(description, cls=(TextT.muted, "mb-6")),
            DividerSplit(cls="my-6"),
            TicketSteps(step),
            DividerSplit(cls="my-6"), 
            DivFullySpaced(
                Div(Strong("Departmento"),
                    P(department),
                    cls=('space-y-3', TextPresets.muted_sm)),
                Div(Strong("Fecha Creación"),
                    P(fechacreacion),
                    cls=('space-y-2', TextPresets.muted_sm)),
                Div(Strong("Fecha Actualizacion"),
                    P(fechamodificacion),
                    cls=('space-y-2', TextPresets.muted_sm)),
                Div(
                    Button("Editar", cls=ButtonT.primary, data_uk_toggle="target: #update-ticket"),
                    Button("Borrar", cls=ButtonT.secondary, data_uk_toggle="target: #delete-ticket"),
                ),
                cls='mt-6'),
            UpdateTicketModal(id, title, description, prioridad, step, department),
            DeleteTicketModal(id)),
            Loading(htmx_indicator=True, type=LoadingT.dots, cls="fixed top-0 right-0 m-4"),
        cls=CardT.hover)

def NewTicketModal():
    return Modal(
        ModalHeader(H3("Crear nuevo ticket de Soporte")),
        ModalBody(
            Form(
                Grid(LabelInput("Titulo", id="title", placeholder="Breve descripción de la averia", name="titulo", required=True),
                    LabelSelect(*map(Option,("IT Support", "HR", "Facilities", "Finance")), placeholder="Selecciona un departamento", label="Departamento",  id="department", name="departmento", required=True)),
                    LabelSelect(*map(Option,("Baja", "Media", "Alta")), placeholder="Selecciona un nivel de Prioridad", label="Nivel de Prioridad", id="priority", name="prioridad", required=True),
                    LabelTextArea("Descripcion", id="description", placeholder="Descripcion detallada de la averia", name="descripcion", required=True),
                    DivRAligned(
                        #Button("Cancelar", cls=ButtonT.ghost),
                        Button("Crear", cls=ButtonT.primary, data_uk_toggle="target: #success-toast; target: #new-ticket")
                ),
            hx_post="/register",
            cls='space-y-8')),
        id="new-ticket")

def UpdateTicketModal(id, title, description, prioridad, step, department):
    return Modal(
        ModalHeader(H3(f"Actualizar ticket de Soporte: {id}")),
        ModalBody(
            Form(
                Grid(LabelInput("ID_Ticket", id="id", placeholder="Breve descripción de la averia", name="id", value=id, readonly=True),
                    LabelInput("Titulo", id="title", placeholder="Breve descripción de la averia", name="titulo", value=title),
                    LabelSelect(*map(Option,("IT Support", "HR", "Facilities", "Finance")), placeholder="Selecciona un departamento", label="Departamento",  id="department", name="departmento", value=department)),
                Grid(   
                    LabelSelect(*map(Option,("Baja", "Media", "Alta")), placeholder="Selecciona un nivel de Prioridad", label="Nivel de Prioridad", id="priority", name="prioridad", value=prioridad),
                    LabelSelect(*map(Option,("Creado","Asignado","En revisión","En proceso","Resuelto")), placeholder="Estado del Ticket", label="Estado del ticket", id="step", name="step", value=valor_status[step])),
                    LabelTextArea("Descripcion", id="description", placeholder="Descripcion detallada de la averia", name="descripcion", value=description),
                    DivRAligned(
                        #Button("Cancelar", cls=ButtonT.ghost),
                        Button("Actualizar", cls=ButtonT.primary, data_uk_toggle="target: #success-toast; target: #update-ticket")
                ),
            hx_post="/update",
            cls='space-y-8')),
        id="update-ticket")

def DeleteTicketModal(id):
    return Modal(
        ModalHeader(H3(f"Eliminar ticket de Soporte: {id}")),
        ModalBody(
            H5("¿Seguro que quieres eliminar este ticket?"),
            Form(
                Grid(
                    LabelInput("ID_Ticket", id="id", placeholder="Breve descripción de la averia", name="id", value=id, readonly=True),
                    DivRAligned(
                        #Button("Cancelar", cls=ButtonT.ghost),
                        Button("Eliminar", cls=ButtonT.primary, data_uk_toggle="target: #success-toast; target: #delete-ticket")
                ),),
            hx_post="/borrar",
            cls='space-y-8')),
        id="delete-ticket")

def consultar_tickets():
    tickets = get_all_tickets()
    return Title("Tablero gestion de Tickets"), Container(
        Section(
            DivFullySpaced(
                H2("Tickets Activos"),
                Button(UkIcon("plus-circle", cls="mr-2"), "Nuevo Ticket", cls=ButtonT.primary, data_uk_toggle="target: #new-ticket"),
                cls='mb-8'),
            Grid(*[TicketCard(**ticket) for ticket in tickets], cols=1),
            cls="my-6"),
        NewTicketModal(),
        #Toast(DivLAligned(UkIcon('check-circle', cls='mr-2'), "Ticket submitted successfully! Our team will review it shortly."), id="success-toast", alert_cls=AlertT.success, cls=(ToastHT.end, ToastVT.bottom)),
        Loading(htmx_indicator=True, type=LoadingT.dots, cls="fixed top-0 right-0 m-4"),
        cls="mx-auto max-w-7xl"
    )   
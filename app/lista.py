from fasthtml.common import *
from monsterui.all import *
from fasthtml.svg import *
import json

from app.models import (
    get_all_tasks, 
    get_count_priority_tasks, 
    get_count_status_tasks,
    get_count_rows
)

app, rt = fast_app(hdrs=Theme.blue.headers())

num_row = get_count_rows()
data = get_all_tasks()
priority_dd = get_count_priority_tasks()
status_dd = get_count_status_tasks()

def LAlignedCheckTxt(txt): 
    return DivLAligned(UkIcon(icon='check'), P(txt, cls=TextPresets.muted_sm))

def _create_tbl_data(d):
    return {'Done': d['selected'], 'Task': d['id'], 'Title': d['title'], 
            'Status'  : d['status'], 'Priority': d['priority'] }
    
data = [_create_tbl_data(d)  for d in data]
page_size = 15
current_page = 0
paginated_data = data[current_page*page_size:(current_page+1)*page_size]

def CreateTaskModal():
    return Modal(
        Div(cls='p-6')(
            ModalTitle('Crear Nueva Tarea'),
            P('Fill out the information below to create a new task', cls=TextPresets.muted_sm),
            Br(),
            Form(cls='space-y-6')(
                Grid(Div(Select(*map(Option,('Documentation', 'Bug', 'Feature')), label='Task Type', id='task_type')),
                     Div(Select(*map(Option,('In Progress', 'Backlog', 'Todo', 'Cancelled', 'Done')), label='Status', id='task_status')),
                     Div(Select(*map(Option, ('Low', 'Medium', 'High')), label='Priority', id='task_priority'))),
                TextArea(label='Title', placeholder='Please describe the task that needs to be completed'),
                DivRAligned(
                    ModalCloseButton('Cancel', cls=ButtonT.ghost),
                    ModalCloseButton('Submit', cls=ButtonT.primary),
                    hx_post="/register",
                    cls='space-x-5'))),
        id='TaskForm')

page_heading = DivFullySpaced(cls='space-y-2')(
    Div(cls='space-y-2')(
        H2('Lista de tareas pendientes!'),P("Aqui tienes una lista con las tareas a realizar!", cls=TextPresets.muted_sm)),
    )

table_controls =(Input(cls='w-[250px]',placeholder='Filtro Tareas'),
     Button("Estado"),
     DropDownNavContainer(map(NavCloseLi,[A(DivFullySpaced(P(a['status']), P(a['count'])),cls='capitalize') for a in status_dd])), 
     Button("Prioridad"),
     DropDownNavContainer(map(NavCloseLi,[A(DivFullySpaced(LAlignedCheckTxt(a['priority']), a['count']),cls='capitalize') for a in priority_dd])),
     Button("Ver"),
     DropDownNavContainer(map(NavCloseLi,[A(LAlignedCheckTxt(o)) for o in ['Title','Status','Priority']])),
     Button('Crear',cls=(ButtonT.primary, TextPresets.bold_sm), data_uk_toggle="target: #TaskForm"))

def task_dropdown():
    return Div(Button(UkIcon('ellipsis')),
               DropDownNavContainer(
                   map(NavCloseLi,[
                       *map(A,('Edit', 'Make a copy', 'Favorite')),
                        A(DivFullySpaced(*[P(o, cls=TextPresets.muted_sm) for o in ('Delete', '⌘⌫')]))])))
def header_render(col):
    match col:
        case "Done":    return Th(CheckboxX(), shrink=True)
        case 'Actions': return Th("",          shrink=True)
        case _:         return Th(col,         expand=True)

def cell_render(col, val):
    def _Td(*args,cls='', **kwargs): return Td(*args, cls=f'p-2 {cls}',**kwargs)
    match col:
        case "Done": return _Td(shrink=True)(CheckboxX(selected=val))
        case "Task":  return _Td(val, cls='uk-visible@s')  # Hide on small screens
        case "Title": return _Td(val, cls='font-medium', expand=True)
        case "Status" | "Priority": return _Td(cls='uk-visible@m uk-text-nowrap capitalize')(Span(val))
        case "Actions": return _Td(task_dropdown(), shrink=True)
        case _: raise ValueError(f"Unknown column: {col}")

task_columns = ["Done", 'Task', 'Title', 'Status', 'Priority', 'Actions']

tasks_table = Div(cls='mt-4')(
    TableFromDicts(
        header_data=task_columns,
        body_data=paginated_data,
        body_cell_render=cell_render,
        header_cell_render=header_render,
        sortable=True,
        cls=(TableT.responsive, TableT.sm, TableT.divider)))

def footer():
    total_pages = (len(data) + page_size - 1) // page_size
    return DivFullySpaced(
        Div(f'1 of {num_row} row(s) selected.', cls=TextPresets.muted_sm),
        DivLAligned(
            DivCentered(f'Page {current_page + 1} of {total_pages}', cls=TextT.sm),
            DivLAligned(*[UkIconLink(icon=i,  button=True) for i in ('chevrons-left', 'chevron-left', 'chevron-right', 'chevrons-right')])))

tasks_ui = Div(DivFullySpaced(DivLAligned(table_controls), cls='mt-8'), tasks_table, footer())
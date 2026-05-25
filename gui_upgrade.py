import functions
import FreeSimpleGUI as sg
import os
import sys

def resource_path(relative_path):
    """Garante que os arquivos funcionem tanto no .py quanto no .exe"""
    try:
        base_path = sys._MEIPASS  # usado pelo PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Caminho do arquivo de tarefas
TODO_FILE = resource_path("todos.txt")

# Cria o arquivo caso não exista
if not os.path.exists(TODO_FILE):
    with open(TODO_FILE, "w") as file:
        pass

sg.theme("DarkTeal12")

# --- COLUNA DA ESQUERDA (Input e Exibição de Dados) ---
coluna_esquerda = [
    [sg.Text("Type in a to-do", text_color='white')],
    [sg.InputText(tooltip="Enter todo", key="todo", size=(46, 11))],
    [sg.Listbox(values=functions.get_todos(TODO_FILE), key='todos',
                enable_events=True, size=(45, 11))] # Ajustado o tamanho para alinhar visualmente com os botões
]

# --- COLUNA DA DIREITA (Todos os botões empilhados em linha) ---
coluna_direita = [
    [sg.Text("")], # Espaço em branco para pular a linha do label "Type in a to-do"
    [sg.Button(size=10, image_source=resource_path("add.png"), mouseover_colors='grey', tooltip="Add Todo", key='Add')],
    [sg.Button(size=10, image_source=resource_path("edit.png"), mouseover_colors='grey', tooltip="Edit Now", key='Edit')],
    [sg.Button(size=10, image_source=resource_path("complete.png"), mouseover_colors='grey', tooltip="Go Complete", key='Complete')],
    [sg.VPush()], # Cria o espaço em branco jogando o botão Exit para o final
    [sg.Button("Exit", size=3)]
]

# --- LAYOUT PRINCIPAL (Une as duas colunas lado a lado) ---
layout = [
    [
        sg.Column(coluna_esquerda, vertical_alignment='top'), 
        sg.Column(coluna_direita, vertical_alignment='top', expand_y=True, element_justification='center')
    ]
]

window = sg.Window('My To-Do App', layout=layout, font=('Helvetica', 12))

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "Exit":
        break

    match event:
        case "Add":
            todos = functions.get_todos(TODO_FILE)
            new_todo_item = values['todo'].strip()
            if new_todo_item:
                todos.append(new_todo_item)
                functions.write_todos(todos, TODO_FILE)
                window['todos'].update(values=todos)
                window['todo'].update('')

        case "Edit":
            try:
                if values['todos']:
                    todo_to_edit = values['todos'][0]
                    new_todo_item = values['todo'].strip()
                    if new_todo_item:
                        todos = functions.get_todos(TODO_FILE)
                        index = todos.index(todo_to_edit)
                        todos[index] = new_todo_item
                        functions.write_todos(todos, TODO_FILE)
                        window['todos'].update(values=todos)
                else:
                    sg.popup("Please select an item first.", font=("Helvetica", 12))
            except (IndexError, KeyError):
                sg.popup("Please select an item first.", font=("Helvetica", 12))

        case "Complete":
            try:
                if values['todos']:
                    todo_to_complete = values['todos'][0]
                    todos = functions.get_todos(TODO_FILE)
                    todos.remove(todo_to_complete)
                    functions.write_todos(todos, TODO_FILE)
                    window['todos'].update(values=todos)
                    window['todo'].update(value='')
                else:
                    sg.popup("Please select an item first.", font=("Helvetica", 12))
            except (IndexError, KeyError):
                sg.popup("Please select an item first.", font=("Helvetica", 12))

        case 'todos':
            if values['todos']:
                window['todo'].update(value=values['todos'][0])

window.close()

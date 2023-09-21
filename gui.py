import tkinter as tk
from tkinter import ttk, filedialog
from flask import Flask, request, jsonify
import pyautogui
import time
import threading
import json

app = Flask(__name__)

mock_data = {
    "parameter": None,
    "value": None,
    "response_type": None,
    "response_content": None,
    "request_method": None
}

@app.route('/api', methods=['GET', 'POST', 'PUT', 'DELETE'])
def mock_endpoint():
    if request.method != mock_data["request_method"]:
        return "Método de solicitud no permitido para este mock", 405
    
    if request.method == "GET":
        param_value = request.args.get(mock_data["parameter"])
    else:
        if not request.json:
            return "Se espera datos en formato JSON", 415
        param_value = request.json.get(mock_data["parameter"])

    if param_value == mock_data["value"]:
        if mock_data["response_type"] == "JSON":
            return jsonify(eval(mock_data["response_content"]))
        else:
            return mock_data["response_content"]

    if param_value == mock_data["value"]:
        if mock_data["response_type"] == "JSON":
            try:
                response_data = json.loads(mock_data["response_content"])
                return jsonify(response_data)
            except json.JSONDecodeError:
                return "Error: El contenido de la respuesta no es un JSON válido.", 400
        else:
            return mock_data["response_content"]
    return "No coincide", 400




def start_mock_api(param_name, param_value, response_type, response_content, request_method, port):
    mock_data["parameter"] = param_name
    mock_data["value"] = param_value
    mock_data["response_type"] = response_type
    mock_data["response_content"] = response_content
    mock_data["request_method"] = request_method

    # Usamos threading para evitar que la GUI se quede pegada
    t = threading.Thread(target=lambda: app.run(port=port))
    t.start()

def setup_api_tab(tab):
    ttk.Label(tab, text="Método de Solicitud:").grid(column=0, row=0)
    methods = ["GET", "POST", "PUT", "DELETE"]
    request_method = ttk.Combobox(tab, values=methods)
    request_method.grid(column=1, row=0)

    ttk.Label(tab, text="Nombre del Parámetro:").grid(column=0, row=1)
    param_name = ttk.Entry(tab)
    param_name.grid(column=1, row=1)

    ttk.Label(tab, text="Valor:").grid(column=0, row=2)
    param_value = ttk.Entry(tab)
    param_value.grid(column=1, row=2)

    ttk.Label(tab, text="Tipo de Respuesta:").grid(column=0, row=3)
    response_types = ["XML", "JSON", "Texto"]
    response_type = ttk.Combobox(tab, values=response_types)
    response_type.grid(column=1, row=3)

    ttk.Label(tab, text="Contenido de Respuesta:").grid(column=0, row=4)
    response_content = tk.Text(tab, width=25, height=5)
    response_content.grid(column=1, row=4)

    start_button = ttk.Button(tab, text="Iniciar API", command=lambda: start_mock_api(param_name.get(), param_value.get(), response_type.get(), response_content.get("1.0", tk.END), request_method.get(), 5000))
    start_button.grid(column=0, row=5, columnspan=2)

def load_commands_from_file(text_widget):
    filepath = filedialog.askopenfilename()
    if filepath:
        with open(filepath, 'r') as file:
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, file.read())

def execute_commands(commands):
    lines = commands.strip().split('\n')
    for line in lines:
        cmd, *args = line.split()
        if cmd == 'open':
            pyautogui.hotkey('win', 'r')
            pyautogui.write(args[0])
            pyautogui.press('enter')
        elif cmd == 'type':
            pyautogui.write(' '.join(args))
        elif cmd == 'press':
            pyautogui.press(args[0])
        elif cmd == 'wait':
            time.sleep(float(args[0]))

def setup_keyboard_mouse_tab(tab):
    instructions = ttk.Label(tab, text="Enter keyboard and mouse commands:")
    instructions.grid(column=0, row=0, columnspan=3)

    action_content = tk.Text(tab, width=50, height=20)
    action_content.grid(column=0, row=1, columnspan=3)

    load_button = ttk.Button(tab, text="Load from file", command=lambda: load_commands_from_file(action_content))
    load_button.grid(column=0, row=2)

    start_button = ttk.Button(tab, text="Execute Commands", command=lambda: execute_commands(action_content.get("1.0", tk.END)))
    start_button.grid(column=1, row=2, columnspan=2)

def main():
    root = tk.Tk()
    root.title("Mockup Tool")

    tabControl = ttk.Notebook(root)

    tab1 = ttk.Frame(tabControl)
    tabControl.add(tab1, text='API Mockup')
    setup_api_tab(tab1)

    tab2 = ttk.Frame(tabControl)
    tabControl.add(tab2, text='Keyboard & Mouse Emulation')
    setup_keyboard_mouse_tab(tab2)

    tabControl.pack(expand=1, fill="both")

    root.mainloop()

if __name__ == "__main__":
    main()
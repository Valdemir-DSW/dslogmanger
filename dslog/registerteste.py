import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
import threading
import time
from datetime import datetime

class LoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Logger App")

        self.log_entries = []
        self.time_counter = 0
        self.running = True

        self.num_variables = self.ask_num_variables()
        self.variable_names = self.ask_variable_names(self.num_variables)
        
        self.create_widgets()
        self.start_time_counter()

        self.start_time = datetime.now()

    def ask_num_variables(self):
        num_vars = simpledialog.askinteger("Input", "Quantas variáveis deseja (entre 2 e 8)?", minvalue=2, maxvalue=8)
        if num_vars is None:
            num_vars = 2  # Valor padrão se o usuário cancelar
        return num_vars

    def ask_variable_names(self, num_vars):
        var_names = []
        for i in range(1, num_vars + 1):
            var_name = simpledialog.askstring("Input", f"Nome da variável {i}:")
            if not var_name:
                var_name = f"Variável {i}"
            var_names.append(var_name)
        return var_names

    def create_widgets(self):
        # Frame para os slides e mensagens
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        # Criar slides para as variáveis dinamicamente
        self.scales = []
        for i in range(self.num_variables):
            tk.Label(frame, text=self.variable_names[i]).pack()
            scale = tk.Scale(frame, from_=0, to=100, orient=tk.HORIZONTAL)
            scale.pack()
            self.scales.append(scale)

        # Entrada de texto para a mensagem do log
        self.log_entry = tk.Entry(frame, width=50)
        self.log_entry.pack(pady=10)

        # Botão para salvar logs
        self.save_logs_button = tk.Button(self.root, text="Salvar Logs", command=self.save_logs)
        self.save_logs_button.pack(pady=10)

    def start_time_counter(self):
        def log_values():
            while self.running:
                self.add_log()
                time.sleep(1)
        threading.Thread(target=log_values).start()

    def add_log(self):
        var_values = [scale.get() for scale in self.scales]
        log_message = self.log_entry.get()
        log_entry = {
            "time": self.time_counter,
            **{f"variable{i + 1}": var_values[i] for i in range(len(var_values))},
            "message": log_message
        }
        self.log_entries.append(log_entry)
        self.time_counter += 1
        self.log_entry.delete(0, tk.END)

    def save_logs(self):
        if self.log_entries:
            file_path = "logs.dslog"
            log_data = {
                "creation_date": self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "start_time": self.start_time.strftime("%H:%M:%S"),
                "num_variables": self.num_variables,
                "variable_names": self.variable_names,
                "log_entries": self.log_entries
            }
            with open(file_path, 'w') as file:
                json.dump(log_data, file, indent=4)
            messagebox.showinfo("Info", f"Logs salvos com sucesso em {file_path}")
        else:
            messagebox.showwarning("Aviso", "Não há logs para salvar!")

    def on_close(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoggerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()

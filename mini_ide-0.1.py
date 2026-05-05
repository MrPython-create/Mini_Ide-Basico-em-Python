# ---------- Mini_Projeto-por_MR_Phytonzinho ----------

from tkinter import filedialog
import tkinter as tk
from tkinter import scrolledtext
import keyword
import re
import sys
import io
current_file = None
# ---------- Função de execução ----------
def run_code():
    code = code_input.get("1.0", tk.END)

    output_box.delete("1.0", tk.END)
    error_box.delete("1.0", tk.END)

    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()

    try:
        exec(code)
        output_box.insert(tk.END, sys.stdout.getvalue(), "ok")
    except Exception as e:
        error_box.insert(tk.END, str(e), "error")
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr


# ---------- Destaque de sintaxe ----------
def highlight_code(event=None):
    code = code_input.get("1.0", tk.END)

    # limpar tags antigas
    for tag in code_input.tag_names():
        code_input.tag_remove(tag, "1.0", tk.END)

    # Palavras-chave (if, else, etc.)
    for kw in keyword.kwlist:
        for match in re.finditer(rf"\b{kw}\b", code):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            code_input.tag_add("keyword", start, end)

    # Strings
    for match in re.finditer(r'".*?"|\'.*?\'', code):
        start = f"1.0+{match.start()}c"
        end = f"1.0+{match.end()}c"
        code_input.tag_add("string", start, end)

    # Números
    for match in re.finditer(r"\b\d+\b", code):
        start = f"1.0+{match.start()}c"
        end = f"1.0+{match.end()}c"
        code_input.tag_add("number", start, end)

def new_file():
    global current_file
    code_input.delete("1.0", "end")
    current_file = None


def open_file():
    global current_file
    file_path = filedialog.askopenfilename(
        filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
    )
    if file_path:
        with open(file_path, "r") as f:
            code_input.delete("1.0", "end")
            code_input.insert("1.0", f.read())
        current_file = file_path


def save_file():
    global current_file
    if current_file:
        with open(current_file, "w") as f:
            f.write(code_input.get("1.0", "end"))
    else:
        save_as_file()


def save_as_file():
    global current_file
    file_path = filedialog.asksaveasfilename(
        defaultextension=".py",
        filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
    )
    if file_path:
        with open(file_path, "w") as f:
            f.write(code_input.get("1.0", "end"))
        current_file = file_path
# ---------- Interface ----------
root = tk.Tk()

menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Novo", command=new_file)
file_menu.add_command(label="Abrir", command=open_file)
file_menu.add_command(label="Salvar", command=save_file)
file_menu.add_command(label="Salvar como", command=save_as_file)

menu_bar.add_cascade(label="Arquivo", menu=file_menu)

root.config(menu=menu_bar)
root.title("Mini_IDE_Python-PRO+😎")
root.geometry("900x500")

frame = tk.Frame(root)

frame.pack(fill="both", expand=True)

# Área de código
code_input = scrolledtext.ScrolledText(frame, width=60, bg="#1e1e1e", fg="white", insertbackground="white")
code_input.pack(side="left", fill="both", expand=True)

# Lado direito
right_frame = tk.Frame(frame)
right_frame.pack(side="right", fill="both")

# Erros
error_label = tk.Label(right_frame, text="Erros", fg="red")
error_label.pack()

error_box = scrolledtext.ScrolledText(
    right_frame,
    height=10,
    bg="#1e1e1e",
    fg="red",
    insertbackground="white"
)
error_box.pack(fill="both")

# Saída
output_label = tk.Label(right_frame, text="Saída")
output_label.pack()

output_box = scrolledtext.ScrolledText(
    right_frame,
    height=10,
    bg="#1e1e1e",
    fg="white",
    insertbackground="white"
)
output_box.pack(fill="both", expand=True)

# Botão
run_button = tk.Button(root, text="Executar ▶ ", command=run_code)
run_button.pack(fill="x")

# ---------- Cores ----------
code_input.tag_config("keyword", foreground="cyan")
code_input.tag_config("string", foreground="green")
code_input.tag_config("number", foreground="orange")

output_box.tag_config("ok", foreground="green")
error_box.tag_config("error", foreground="red")

# Evento ao digitar
code_input.bind("<KeyRelease>", highlight_code)

# Código inicial
code_input.insert(tk.END, '''condition = -5

print("Hellor world")

Crier seu Projeto! Aqui. IOIOIO <--- Apague
''')

highlight_code()

root.mainloop()

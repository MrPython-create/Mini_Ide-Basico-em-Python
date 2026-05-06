
from tkinter import filedialog
import tkinter as tk
from tkinter import scrolledtext
import keyword
import re
import sys
import io
import traceback
import ast
current_file = None
root = tk.Tk()
root.title("Mini IDE PRO 0.2")
root.geometry("1020x720")
auto_mode = tk.BooleanVar(value=False)
auto_button = tk.Checkbutton(
    root,
    text="Auto executar",
    variable=auto_mode,
    onvalue=True,
    offvalue=False
)
auto_button.pack()


frame = tk.Frame(root)
frame.pack(fill="both", expand=True)
line_numbers = tk.Text(
    frame,
    width=4,
    bg="#2b2b2b",
    fg="gray",
    state="disabled"
)
line_numbers.pack(side="left", fill="y")

code_input = scrolledtext.ScrolledText(
    frame,
    width=60,
    bg="#1e1e1e",
    fg="white",
    insertbackground="white",
    font=("DejaVu Sans Mono", 12)
)
code_input.pack(side="left", fill="both", expand=True)

right_frame = tk.Frame(frame)
right_frame.pack(side="right", fill="both")

error_label = tk.Label(right_frame, text="Erros", fg="red")
error_label.pack()

error_box = scrolledtext.ScrolledText(
    right_frame,
    height=18,
    bg="#1e1e1e",
    fg="red",
    insertbackground="white"
)
error_box.pack(fill="both")
error_box.config(state="disabled")

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
output_box.config(state="disabled")

def update_title():
    if current_file:
        root.title(f"Mini IDE - {current_file}")
    else:
        root.title("Mini IDE - Novo arquivo")

def highlight_code(event=None):
    code = code_input.get("1.0", tk.END)

    for tag in code_input.tag_names():
        code_input.tag_remove(tag, "1.0", tk.END)

    for kw in keyword.kwlist:
        for match in re.finditer(rf"\b{kw}\b", code):
            code_input.tag_add("keyword", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

    for match in re.finditer(r'".*?"|\'.*?\'', code):
        code_input.tag_add("string", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

    for match in re.finditer(r"\b\d+\b", code):
        code_input.tag_add("number", f"1.0+{match.start()}c", f"1.0+{match.end()}c")

def update_line_numbers(event=None):
    line_numbers.config(state="normal")
    line_numbers.delete("1.0", "end")

    total_lines = int(code_input.index("end-1c").split(".")[0])

    for i in range(1, total_lines + 1):
        line_numbers.insert("end", str(i) + "\n")

    line_numbers.config(state="disabled")

def on_key_release(event=None):
    highlight_code()
    update_line_numbers()
    check_syntax()
    
def new_file():
    global current_file
    code_input.delete("1.0", "end")
    current_file = None
    update_title()

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
        update_title()
        update_line_numbers()
        highlight_code()

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
        update_title()
        
def write_output(text, tag=None):
    output_box.config(state="normal")
    output_box.insert(tk.END, text, tag)
    output_box.config(state="disabled")
    output_box.see(tk.END)

def write_error(text):
    error_box.config(state="normal")
    error_box.insert(tk.END, text)
    error_box.config(state="disabled")
    error_box.see(tk.END)

def clear_console():
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.config(state="disabled")

    error_box.config(state="normal")
    error_box.delete("1.0", tk.END)
    error_box.config(state="disabled")
def run_code():
    code = code_input.get("1.0", tk.END)

    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.config(state="disabled")

    error_box.config(state="normal")
    error_box.delete("1.0", tk.END)
    error_box.config(state="disabled")

    old_stdout = sys.stdout
    old_stderr = sys.stderr

    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()

    try:
        exec(code, {})

        output = sys.stdout.getvalue()
        error = sys.stderr.getvalue()

        if output:
            write_output(output)
        else:
            write_output("✔ Sem saída\n", "ok")

        if error:
            write_error(error)

        write_output("\n✔ Executado com sucesso\n", "ok")

    except Exception:
        write_error(traceback.format_exc())

    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

def auto_run(event=None):
    if auto_mode.get():
        run_code()
        
def check_syntax():
    code = code_input.get("1.0", tk.END)

    # remove erro antigo
    code_input.tag_remove("syntax_error", "1.0", tk.END)

    try:
        ast.parse(code)
    except SyntaxError as e:
        if e.lineno:
            line = e.lineno
            code_input.tag_add(
                "syntax_error",
                f"{line}.0",
                f"{line}.end"
            )

menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Salvar   (Ctrl+S)", command=save_file)
file_menu.add_command(label="Abrir    (Ctrl+O)", command=open_file)
file_menu.add_command(label="Novo     (Ctrl+N)", command=new_file)
file_menu.add_command(label="Executar (F5)", command=run_code)

menu_bar.add_cascade(label="Arquivo", menu=file_menu)
root.config(menu=menu_bar)

run_button = tk.Button(root, text="Executar ▶", command=run_code).pack(fill="x")

tk.Button(root, text="Limpar Console 🧹", command=clear_console).pack(fill="x")

code_input.tag_config("keyword", foreground="cyan")
code_input.tag_config("string", foreground="green")
code_input.tag_config("number", foreground="orange")
code_input.tag_config("syntax_error", background="#5a1a1a")

output_box.tag_config("ok", foreground="green")
error_box.tag_config("error", foreground="red")

root.bind("<Control-s>", lambda e: save_file())
root.bind("<Control-o>", lambda e: open_file())
root.bind("<Control-n>", lambda e: new_file())
root.bind("<F5>", lambda e: run_code())

#code_input.bind("<KeyRelease>", on_key_release)
code_input.bind("<KeyRelease>", lambda e: (on_key_release(e), auto_run(e)))

code_input.insert(tk.END, '''print("Hello world")

# Comece seu projeto aqui <------ Apague tudo ok...
''')

highlight_code()
update_line_numbers()

root.mainloop()

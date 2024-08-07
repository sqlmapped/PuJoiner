import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import TkinterDnD
from PIL import Image, ImageTk, ImageFont, ImageDraw
import os


files = []

def select_file(file_type):
    file_path = filedialog.askopenfilename(
        filetypes=[("All Files", "*.*"), ("Executable Files", "*.exe")]
    )
    if file_path:
        file_info = {
            "path": file_path,
            "name": os.path.basename(file_path),
            "size": os.path.getsize(file_path),
            "type": "Payload" if file_type == "payload" else "File"
        }
        files.append(file_info)
        update_file_list()

def update_file_list():
    for i in file_list.get_children():
        file_list.delete(i)
    for file in files:
        file_list.insert('', 'end', values=(file['name'], file['size'], file['type']))

def build_files():
    if not files:
        messagebox.showwarning("Warning", "No files to combine.")
        return
    output_path = filedialog.asksaveasfilename(defaultextension=".exe",
                                            filetypes=[("Executable Files", "*.exe")])
    if not output_path:
        return
    with open(output_path, 'wb') as output_file:
        for file in files:
            with open(file['path'], 'rb') as f:
                output_file.write(f.read())
    messagebox.showinfo("Success", f"Files combined successfully into {output_path}")

def clear_files():
    global files
    files = []
    update_file_list()

def copy_info():
    if not files:
        messagebox.showwarning("Warning", "No files to copy info from.")
        return
    info = "\n".join(f"{file['name']} ({file['type']}) - {file['size']} bytes" for file in files)
    root.clipboard_clear()
    root.clipboard_append(info)
    messagebox.showinfo("Info Copied", "File information copied to clipboard.")
# by sqlmapped
def set_dark_theme():
    style.configure('Treeview', background='#2e2e2e', foreground='white', fieldbackground='#2e2e2e')
    style.configure('Treeview.Heading', background='#4b4b4b', foreground='white', relief='flat')
    root.configure(bg='#2e2e2e')
    button_frame.configure(bg='#2e2e2e')
    for button in button_frame.winfo_children():
        button.configure(bg='#4b4b4b', fg='white', relief=tk.RAISED, borderwidth=2, padx=10, pady=5, font=('CustomFont', 10))
    file_list.heading("Name", text="File Name", anchor=tk.W)
    file_list.heading("Size", text="Size", anchor=tk.W)
    file_list.heading("Type", text="Type", anchor=tk.W)
    footer_label.configure(bg='#2e2e2e', fg='white')

def create_rounded_button(frame, text, command):
    button = tk.Button(frame, text=text, command=command, relief=tk.RAISED, borderwidth=2, font=('CustomFont', 10))
    button.pack(side=tk.LEFT, padx=5, pady=5)
    return button

root = TkinterDnD.Tk()
root.title("PuJoiner")


try:
    custom_font = ImageFont.truetype("font.ttf", 12)  # Убедитесь, что font.ttf находится в том же каталоге
    root.option_add('*Font', ('CustomFont', 12))
except IOError:
    print("Custom font not found. Using default font.")


try:
    icon = Image.open("icon.png")
    root.iconphoto(False, ImageTk.PhotoImage(icon))
except FileNotFoundError:
    pass


style = ttk.Style(root)

frame = tk.Frame(root)
frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

file_list = ttk.Treeview(frame, columns=("Name", "Size", "Type"), show='headings', style='Treeview')
file_list.heading("Name", text="File Name")
file_list.heading("Size", text="Size")
file_list.heading("Type", text="Type")
file_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


style.configure('Treeview.Heading', font=('CustomFont', 12, 'bold'))

button_frame = tk.Frame(root)
button_frame.pack(pady=10)


buttons = [
    ("Add File", lambda: select_file("file")),
    ("Add Payload", lambda: select_file("payload")),
    ("Build", build_files),
    ("Clear", clear_files),
    ("Copy Info from Program", copy_info)
]

for text, command in buttons:
    create_rounded_button(button_frame, text, command)


footer_label = tk.Label(root, text="Coded by sqlmapped (Yaroslav)", font=('CustomFont', 10), bg='#2e2e2e', fg='white')
footer_label.pack(side=tk.BOTTOM, pady=10)


set_dark_theme()

root.mainloop()

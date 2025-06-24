import tkinter as tk
from tkinter import filedialog,ttk
import sv_ttk
import subprocess
import os
python_env=""
idf_py=""
path=""
def select_esp_file():
    esp_path=filedialog.askdirectory(title="Select IDF Path")
    global python_env, idf_py,label,frame1
    python_env = os.path.join(esp_path, "python_env", "idf5.4_py3.11_env", "Scripts", "python.exe")
    idf_py = os.path.join(esp_path,"frameworks","esp-idf-v5.4.1","tools", "idf.py")
    label.config(text=""+esp_path,font=("Courier",13,"underline"))
def open_file():
    global path
    path = filedialog.askdirectory(title="Select ESP-IDF Project Folder")     
    label1.config(text=""+path,font=("Courier",10,"underline"))
def flash():
    subprocess.run([python_env, idf_py,"build"], cwd=path)
    subprocess.run([python_env, idf_py,"flash"], cwd=path)
    subprocess.run([python_env, idf_py,"monitor"], cwd=path)
root = tk.Tk()
root.geometry("800x200")
frame1 = tk.Frame(root)
frame1.pack(anchor="w", pady=5, padx=10)
frame2 = tk.Frame(root)
frame2.pack(anchor="w", pady=15, padx=10)
button1 = ttk.Button(frame1,text="Select Esp_Path",command=select_esp_file)
button1.pack(side="left")
button = ttk.Button(frame2, text="Open ESP-IDF Project", command=open_file)
button.pack(side="left")
button2 = ttk.Button(root,text="Flash",command=flash)
button2.pack(side="top",anchor="w",pady=15,padx=10)
label = ttk.Label(frame1, text="")
label.pack(side="left",padx=10)
label1=ttk.Label(frame2,text="")
label1.pack(side="left",padx=10)
sv_ttk.set_theme("dark")
root.mainloop()

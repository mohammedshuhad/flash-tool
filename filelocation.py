import tkinter as tk
from tkinter import filedialog,ttk
import sv_ttk
import subprocess
import os
python_env=""
idf_py=""
path=""
root = tk.Tk()
x=tk.BooleanVar()
y=tk.BooleanVar()
def pulsator():
    global x   
    a=0
    with open("C:/Users/user/Documents/UI/hello_world/sdkconfig",'r')as file:
        lines=file.readlines()
    for line in lines:
     if line.strip()=="CONFIG_DEVICE_PULSATOR=y":
         a+=1
    if a==1:
        y.set(False)
        x.set(True)   
    else:
        x.set(False)
        chant()  
def chant():
    global y
    a=0
    with open("C:/Users/user/Documents/UI/hello_world/sdkconfig",'r')as file:
        lines=file.readlines()
    for line in lines:
     if line.strip()=="CONFIG_DEVICE_CHANT=y":
         a+=1
    if a==1:
        x.set(False)
        y.set(True)   
    else:
        y.set(False)
def select_esp_file():
    esp_path=filedialog.askdirectory(title="Select IDF Path")
    global python_env, idf_py,label,frame1
    python_env = os.path.join(esp_path, "python_env", "idf5.4_py3.11_env", "Scripts", "python.exe")
    idf_py = os.path.join(esp_path,"frameworks","esp-idf-v5.4.1","tools", "idf.py")
    label.config(text=""+esp_path,font=("Courier",13,"underline"))
def open_file():
    global path
    path = filedialog.askdirectory(title="Select ESP-IDF Project Folder")  
    pulsator()   
    label1.config(text=""+path,font=("Courier",10,"underline"))
def flash():
    subprocess.run([python_env, idf_py,"build"], cwd=path)
    subprocess.run([python_env, idf_py,"flash"], cwd=path)
    subprocess.run([python_env, idf_py,"monitor"], cwd=path)
def change_pulsator():
    global x
    y.set(False)
    if x.get()== True:
        with open("C:/Users/user/Documents/UI/hello_world/sdkconfig",'r')as file:
            lines=file.readlines()
            updated_lines=[]
            for line in lines:
                if line.strip()=="CONFIG_DEVICE_CHANT=y":
                    updated_lines.append("CONFIG_DEVICE_PULSATOR=y\n") 
                else:
                    updated_lines.append(line)    
        with open("C:/Users/user/Documents/UI/hello_world/sdkconfig", 'w') as file:
            file.writelines(updated_lines)         
def change_chant():
    global y
    x.set(False)
    if y.get()== True:
        with open("C:/Users/user/Documents/UI/hello_world/sdkconfig",'r')as file:
            lines=file.readlines()
            updated_lines=[]
            for line in lines:
                if line.strip()=="CONFIG_DEVICE_PULSATOR=y":
                    updated_lines.append("CONFIG_DEVICE_CHANT=y\n") 
                else:
                    updated_lines.append(line)    
        with open("C:/Users/user/Documents/UI/hello_world/sdkconfig", 'w') as file:
            file.writelines(updated_lines)                         
root.geometry("1000x400")
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
checkbutton1=ttk.Checkbutton(root,text="Pulsator",variable=x,onvalue=1,offvalue=0,command=change_pulsator)
checkbutton1.pack(side="left",anchor="w",pady=5,padx=10)
checkbutton2=ttk.Checkbutton(root,text="Chant",variable=y,onvalue=1,offvalue=0,command=change_chant)
checkbutton2.pack(side="left",anchor="w",pady=5,padx=10)
sv_ttk.set_theme("dark")
root.mainloop()
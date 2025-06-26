import tkinter as tk
from tkinter import filedialog,ttk,messagebox
import sv_ttk
import subprocess
import os,shutil
path=""
config_path=""
base_json_path=""
esp_path=""
root = tk.Tk()
x=tk.BooleanVar()
y=tk.BooleanVar()
z=tk.BooleanVar()
def pulsator():
    global x ,config_path 
    a=0
    config_path=os.path.join(path,"sdkconfig")
    with open(config_path,'r')as file:
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
    with open(config_path,'r')as file:
        lines=file.readlines()
    for line in lines:
     if line.strip()=="CONFIG_DEVICE_CHANT=y":
         a+=1
    if a==1:
        x.set(False)
        y.set(True) 
    else:
        y.set(False)
def wifi():
    global z
    a=0
    with open(config_path,'r')as file:
        Lines=file.readlines()
        for line in Lines:
            if line.strip()=="CONFIG_WIFI_MENU_DISABLE=y" :  
               a+=1     
        if a==1:
            z.set(False)  
        else:
            z.set(True)   
            change_password()  
def menu():
    with open(config_path,'r')as file:
        Lines=file.readlines()
        for line in Lines:
            if line.strip().startswith("CONFIG_SETTINGS_MENU_PASSWORD="):
               menupassword=int(line.split("=")[1])
               entry3.insert(0,menupassword)
def select_esp_file():
    global esp_path
    esp_path=filedialog.askdirectory(title="Select IDF Path")
    label.config(text=""+esp_path,font=("Courier",13,"underline"))
def enable_checkbutton():
    global checkbutton1,checkbutton2,checkbutton3
    if os.path.exists(path):
        checkbutton1.config(state="normal") 
        checkbutton2.config(state="normal")
        checkbutton3.config(state="normal")
def open_file():
    global path
    path = filedialog.askdirectory(title="Select ESP-IDF Project Folder")  
    pulsator()   
    wifi()
    enable_checkbutton()
    menu()
    label1.config(text=""+path,font=("Courier",10,"underline"))
def flash():
    json_path=os.path.join(path,"main\\utility\\json","pulsator.json" if x.get() else "chant.json")
    print(base_json_path)
    print(json_path)
    shutil.copyfile(base_json_path, json_path)         
    script_path=os.path.normpath(os.path.join(path,"main\\utility\\json","script.py"))   
    abcd=os.path.join(path,"main\\utility\\json")
    subprocess.run(["python",script_path],cwd=abcd)
    export_script = os.path.join(esp_path, "export") 
    command = f'"{export_script}" && cd /d "{path}" && idf.py flash'
    try:
        subprocess.run(command, shell=True, check=True)
        print("Flash and monitor completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Flash command failed with return code: {e.returncode}")
    except Exception as e:
        print(f"An error occurred: {e}") 
def change_pulsator():
    global x
    y.set(False)
    if x.get()== True:
        with open(config_path,'r')as file:
            lines=file.readlines()
            updated_lines=[]
            for line in lines:
                if line.strip()=="CONFIG_DEVICE_CHANT=y":
                    updated_lines.append("CONFIG_DEVICE_PULSATOR=y\n") 
                else:
                    updated_lines.append(line)    
        with open(config_path, 'w') as file:    
            file.writelines(updated_lines)     
def change_chant():
    global y
    x.set(False)
    if y.get()== True:
        with open(config_path,'r')as file:
            lines=file.readlines()
            updated_lines=[]
            for line in lines:
                if line.strip()=="CONFIG_DEVICE_PULSATOR=y":
                    updated_lines.append("CONFIG_DEVICE_CHANT=y\n") 
                else:
                    updated_lines.append(line)    
        with open(config_path, 'w') as file:
            file.writelines(updated_lines)  
def change_password():
    global label2, entry, label3, entry1, button4
    if z.get()==False:
        with open(config_path,'r')as file:
            lines=file.readlines()
            updated_lines=[]
            for line in lines:
                if line.strip()=="# CONFIG_WIFI_MENU_DISABLE is not set":
                    updated_lines.append("CONFIG_WIFI_MENU_DISABLE=y\n")
                else:
                    updated_lines.append(line)      
        with open (config_path,'w')as file:
            file.writelines(updated_lines)      
        try:
           label2.destroy()
        except NameError:
           pass
        try:
           entry.destroy()
        except NameError:
           pass
        try:
           label3.destroy()
        except NameError:
           pass
        try:
           entry1.destroy()
        except NameError:
            pass
        try:
            button4.destroy()
        except NameError:
            pass
        return
    else:      
      label2 = ttk.Label(root, text="Enter SSID Name", font=("Courier", 10 ,))
      label2.pack(side="top", anchor="w", padx=10, pady=(10, 0))
      entry = ttk.Entry(root)      
      label3 = ttk.Label(root, text="Enter Password", font=("Courier", 10,))
      entry1 = ttk.Entry(root)
      with open(config_path,'r')as file:
          lines=file.readlines()
          for line in lines:
            line = line.strip()
            if line.startswith("CONFIG_WIFI_SSID="):
               entry.insert(0, line.split("=", 1)[1].strip('"'))
            elif line.startswith("CONFIG_WIFI_PASSWORD="):
                entry1.insert(0,line.split("=", 1)[1].strip('"'))
      entry.pack(side="top", anchor="w", padx=10, pady=(0, 10)) 
      label3.pack(side="top", anchor="w", padx=10, pady=(10, 0))
      entry1.pack(side="top", anchor="w", padx=10, pady=(0, 10)) 
      entry1.bind("<FocusIn>", on_password_focus_in)
      entry1.bind("<FocusOut>", on_password_focus_out)
      entry.bind("<FocusIn>", on_ssid_focus_in)
      entry.bind("<FocusOut>", on_ssid_focus_out)
def accept():   
        name=entry.get()
        pas=entry1.get()
        with open(config_path,'r')as file:
            lines=file.readlines()
            updated_lines=[]
            for line in lines:
                if line.strip()=="CONFIG_WIFI_MENU_DISABLE=y":
                    updated_lines.append("# CONFIG_WIFI_MENU_DISABLE is not set\n")
                elif line.strip().startswith("#CONFIG_WIFI_SSID="):
                    updated_lines.append(f"CONFIG_WIFI_SSID=\"{name}\"\n")
                elif line.strip().startswith("#CONFIG_WIFI_PASSWORD="):
                    updated_lines.append(f"CONFIG_WIFI_PASSWORD=\"{pas}\"\n")
                elif line.strip().startswith("CONFIG_WIFI_SSID=") : 
                    updated_lines.append(f"CONFIG_WIFI_SSID=\"{name}\"\n")  
                elif line.strip().startswith("CONFIG_WIFI_PASSWORD=") :
                    updated_lines.append(f"CONFIG_WIFI_PASSWORD=\"{pas}\"\n")   
                else:
                    updated_lines.append(line)
        with open(config_path, 'w') as file:
            file.writelines(updated_lines)       
def menu_config(event=None):
    k=int(entry3.get())
    if k<0 or k>10000:
        label4=ttk.Label(root,text="Invalid Input")
        label4.pack()
        root.after(2000,lambda:label4.destroy())
    else:
        with open(config_path,'r')as file:
            lines=file.readlines()
            updated_lines=[]
            for line in lines:
                if line.strip().startswith("CONFIG_SETTINGS_MENU_PASSWORD="):
                    updated_lines.append(f"CONFIG_SETTINGS_MENU_PASSWORD={k}\n")
                else:
                    updated_lines.append(line)   
        with open(config_path,'w')as file:
            file.writelines(updated_lines)   
entry1_has_focus = [False]
entry_has_focus = [False]
def on_password_focus_in(event):
    entry1_has_focus[0] = True
def on_password_focus_out(event):
    entry1_has_focus[0] = False
    root.after(100, lambda: check_password_focus())
def on_ssid_focus_in(event):
    entry_has_focus[0] = True
def check_ssid_focus():
    if not entry_has_focus[0] and root.focus_get() != entry1:
        accept()
def on_ssid_focus_out(event):
    entry_has_focus[0] = False
    root.after(100, lambda: check_ssid_focus())
def check_password_focus():
    if not entry1_has_focus[0] and root.focus_get() != entry:
        accept()
def jsonsearch():
    global base_json_path
    base_json_path=filedialog.askopenfilename(
        title="Open JSON FILE",
        filetypes=[("JSON Files","*json")]
    )
    label5.config(text="Copied from:"+base_json_path,font=("Courier",10,"underline"))    
root.geometry("1000x1000")
frame1 = tk.Frame(root)
frame1.pack(anchor="w", pady=5, padx=10)
frame2 = tk.Frame(root)
frame2.pack(anchor="w", pady=15, padx=10)
frame4=tk.Frame(root)
frame4.pack(anchor="w", pady=15, padx=10)
button1 = ttk.Button(frame1,text="Select Esp_Path",command=select_esp_file)
button1.pack(side="left")
button = ttk.Button(frame2, text="Open ESP-IDF Project", command=open_file)
button.pack(side="left")
button2 = ttk.Button(root,text="Flash",command=flash)
button2.pack(side="top",anchor="w",pady=15,padx=10)
checkbutton3=ttk.Checkbutton(root,text="Enable wifi",command=change_password,variable=z,onvalue=1,offvalue=0,state="disabled")
checkbutton3.pack(side="top",anchor="w",pady=5,padx=10)
label = ttk.Label(frame1, text="")
label.pack(side="left",padx=10)
label1=ttk.Label(frame2,text="")
label1.pack(side="left",padx=10)
checkbutton1=ttk.Checkbutton(root,text="Pulsator",variable=x,onvalue=1,offvalue=0,command=change_pulsator,state="disabled")
checkbutton1.pack(side="left",anchor="w",pady=5,padx=10)
checkbutton2=ttk.Checkbutton(root,text="Chant",variable=y,onvalue=1,offvalue=0,command=change_chant,state="disabled")
checkbutton2.pack(side="left",anchor="w",pady=5,padx=10)
frame3 = tk.Frame(root)
frame3.pack(side="top",padx=10, pady=10, fill="x") 
entry3 = ttk.Entry(frame3)
entry3.pack(side="left", padx=10,pady=10)
entry3_has_focus = [False]
def on_entry_focus_in(event):
    entry3_has_focus[0] = True
def on_entry_focus_out(event):
    entry3_has_focus[0] = False
    root.after(100, menu_config)
def global_click(event):
    if entry3_has_focus[0] and event.widget != entry3:
        dummy_focus_widget.focus_set()
    if entry1_has_focus[0] and event.widget not in [entry, entry1]:
        dummy_focus_widget.focus_set()
        accept()
    if entry_has_focus[0] and event.widget not in [entry, entry1]:
        dummy_focus_widget.focus_set()
        accept()
dummy_focus_widget = ttk.Entry(root)
dummy_focus_widget.place(x=-100, y=-100)   
entry3.bind("<FocusIn>", on_entry_focus_in)
entry3.bind("<FocusOut>", on_entry_focus_out)
root.bind("<Button-1>", global_click)
button5=ttk.Button(frame4,text="Select JSON File",command=jsonsearch)
button5.pack(side="top",anchor="w",pady=15,padx=10)
label5=ttk.Label(frame4,text="")
label5.pack(side="left",padx=10)
sv_ttk.set_theme("dark")
root.mainloop()
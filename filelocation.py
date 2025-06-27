import tkinter as tk
from tkinter import filedialog,ttk
import sv_ttk
import subprocess
import os,shutil
path=""
config_path=""
base_json_path=""
esp_path=""
root = tk.Tk()
pulsator_value=tk.BooleanVar()
chant_value=tk.BooleanVar()
wifi_value=tk.BooleanVar()
def pulsator():
    global pulsator_value ,config_path 
    a=0
    config_path=os.path.join(path,"sdkconfig")
    with open(config_path,'r')as file:
        lines=file.readlines()
    for line in lines:
     if line.strip()=="CONFIG_DEVICE_PULSATOR=y":
         a+=1
    if a==1:
        chant_value.set(False)
        pulsator_value.set(True)   
    else:
        pulsator_value.set(False)
        chant()  
def chant():
    global chant_value
    a=0
    with open(config_path,'r')as file:
        lines=file.readlines()
    for line in lines:
     if line.strip()=="CONFIG_DEVICE_CHANT=y":
         a+=1
    if a==1:
        pulsator_value.set(False)
        chant_value.set(True) 
    else:
        chant_value.set(False)
def wifi():
    global wifi_value
    a=0
    with open(config_path,'r')as file:
        Lines=file.readlines()
        for line in Lines:
            if line.strip()=="CONFIG_WIFI_MENU_DISABLE=y" :  
               a+=1     
        if a==1:
            wifi_value.set(False)  
        else:
            wifi_value.set(True)   
            change_password()  
def menu():
    with open(config_path,'r')as file:
        Lines=file.readlines()
        for line in Lines:
            if line.strip().startswith("CONFIG_SETTINGS_MENU_PASSWORD="):
               menupassword=int(line.split("=")[1])
               Setting_menu_password_entryfield.insert(0,menupassword)
def select_esp_file():
    global esp_path
    esp_path=filedialog.askdirectory(title="Select IDF Path")
    Esp_file_path_label.config(text=""+esp_path,font=("Courier",13,"underline"))
def enable_checkbutton():
    global pulsator_checkbutton,chant_checkbutton,wifi_checkbutton
    if os.path.exists(path):
        pulsator_checkbutton.config(state="normal") 
        chant_checkbutton.config(state="normal")
        wifi_checkbutton.config(state="normal")
def open_file():
    global path
    path = filedialog.askdirectory(title="Select ESP-IDF Project Folder")  
    pulsator()   
    wifi()
    enable_checkbutton()
    menu()
    file_path_label.config(text=""+path,font=("Courier",10,"underline"))
def flash():
    Checklabelfor_paths = ttk.Label(root)
    if not esp_path:
        Checklabelfor_paths.config(text="Invalid ESP_IDF Path")
        Checklabelfor_paths.pack(anchor="w", padx=10)
        root.after(2000, lambda: Checklabelfor_paths.destroy())
    elif not path:
        Checklabelfor_paths.config(text="Invalid File Path")
        Checklabelfor_paths.pack(anchor="w", padx=10)
        root.after(2000, lambda: Checklabelfor_paths.destroy())
    else:
        json_path = os.path.join(path, "main\\utility\\json", "................pulsator.json" if pulsator_value.get() else "chant.json")
        script_path = os.path.normpath(os.path.join(path, "main\\utility\\json", "script.py"))
        abcd = os.path.join(path, "main\\utility\\json")
        try:
            shutil.copyfile(base_json_path, json_path)
        except Exception as e:
            Checklabelfor_paths.config(text="Select JSON File")
            Checklabelfor_paths.pack(anchor="w", padx=10)
            root.after(2000, lambda: Checklabelfor_paths.destroy())
            return
        if not os.path.isfile(json_path) or not json_path.endswith(".json"):
            Checklabelfor_paths.config(text="Invalid json file Path")
            Checklabelfor_paths.pack(anchor="w", padx=10)
            root.after(2000, lambda: Checklabelfor_paths.destroy())
        elif not os.path.isfile(script_path):
            Checklabelfor_paths.config(text="Invalid script file Path")
            Checklabelfor_paths.pack(anchor="w", padx=10)
            root.after(2000, lambda: Checklabelfor_paths.destroy())
        elif pulsator_value.get() == 0 and chant_value.get() == 0:
            Checklabelfor_paths.config(text="Choose chant or pulsator")
            Checklabelfor_paths.pack(anchor="w", padx=10)
            root.after(2000, lambda: Checklabelfor_paths.destroy())
        else:
            subprocess.run(["python", script_path], cwd=abcd)
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
    global pulsator_value
    chant_value.set(False)
    if pulsator_value.get() == True:
        with open(config_path, 'r') as file:
            lines = file.readlines()
            updated_lines = []
            for line in lines:
                if line.strip() == "CONFIG_DEVICE_CHANT=y":
                    updated_lines.append("CONFIG_DEVICE_PULSATOR=y\n")
                else:
                    updated_lines.append(line)
        with open(config_path, 'w') as file:
            file.writelines(updated_lines)
    else:
        chant_value.set(True)
        change_chant()
def change_chant():
    global chant_value
    pulsator_value.set(False)
    if chant_value.get() == True:
        with open(config_path, 'r') as file:
            lines = file.readlines()
            updated_lines = []
            for line in lines:
                if line.strip() == "CONFIG_DEVICE_PULSATOR=y":
                    updated_lines.append("CONFIG_DEVICE_CHANT=y\n")
                else:
                    updated_lines.append(line)
        with open(config_path, 'w') as file:
            file.writelines(updated_lines)
    else:
        pulsator_value.set(True)
        change_pulsator()
def change_password():
    global ssid_label,ssid_entry_field,password_label, entry1
    try:
        for widget in frame_wifi.winfo_children():
            widget.destroy()
    except:
        pass
    if wifi_value.get() == False:
        with open(config_path, 'r') as file:
            lines = file.readlines()
            updated_lines = []
            for line in lines:
                if line.strip() == "# CONFIG_WIFI_MENU_DISABLE is not set":
                    updated_lines.append("CONFIG_WIFI_MENU_DISABLE=y\n")
                else:
                    updated_lines.append(line)
        with open(config_path, 'w') as file:
            file.writelines(updated_lines)
        return
    else:
        ssid_label = ttk.Label(frame_wifi, text="Enter SSID Name", font=("Courier", 10))
        ssid_label.grid(row=0, column=0, sticky="w", pady=(5, 0))
        ssid_entry_field = ttk.Entry(frame_wifi)
        ssid_entry_field.grid(row=0, column=1, padx=5, pady=(5, 0))
        password_label = ttk.Label(frame_wifi, text="Enter Password", font=("Courier", 10))
        password_label.grid(row=1, column=0, sticky="w", pady=(5, 0))
        entry1 = ttk.Entry(frame_wifi)
        entry1.grid(row=1, column=1, padx=5, pady=(5, 0))
        with open(config_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith("CONFIG_WIFI_SSID="):
                    ssid_entry_field.insert(0, line.split("=", 1)[1].strip('"'))
                elif line.startswith("CONFIG_WIFI_PASSWORD="):
                    entry1.insert(0, line.split("=", 1)[1].strip('"'))
        entry1.bind("<FocusIn>", on_password_focus_in)
        entry1.bind("<FocusOut>", on_password_focus_out)
        ssid_entry_field.bind("<FocusIn>", on_ssid_focus_in)
        ssid_entry_field.bind("<FocusOut>", on_ssid_focus_out)
def accept():
    name = ssid_entry_field.get()
    pas = ssid_entry_field.get()
    with open(config_path, 'r') as file:
        lines = file.readlines()
        updated_lines = []
        for line in lines:
            if line.strip() == "CONFIG_WIFI_MENU_DISABLE=y":
                updated_lines.append("# CONFIG_WIFI_MENU_DISABLE is not set\n")
            elif line.strip().startswith("#CONFIG_WIFI_SSID="):
                updated_lines.append(f"CONFIG_WIFI_SSID=\"{name}\"\n")
            elif line.strip().startswith("#CONFIG_WIFI_PASSWORD="):
                updated_lines.append(f"CONFIG_WIFI_PASSWORD=\"{pas}\"\n")
            elif line.strip().startswith("CONFIG_WIFI_SSID="):
                updated_lines.append(f"CONFIG_WIFI_SSID=\"{name}\"\n")
            elif line.strip().startswith("CONFIG_WIFI_PASSWORD="):
                updated_lines.append(f"CONFIG_WIFI_PASSWORD=\"{pas}\"\n")
            else:
                updated_lines.append(line)
    with open(config_path, 'w') as file:
        file.writelines(updated_lines)
def menu_config(event=None):
    password_validity = int(Setting_menu_password_entryfield.get())
    if password_validity < 0 or password_validity > 10000:
        password_validity_label = ttk.Label(root, text="Invalid Input")
        password_validity_label.pack(anchor="w", padx=10)
        root.after(2000, lambda: password_validity_label.destroy())
    else:
        with open(config_path, 'r') as file:
            lines = file.readlines()
            updated_lines = []
            for line in lines:
                if line.strip().startswith("CONFIG_SETTINGS_MENU_PASSWORD="):
                    updated_lines.append(f"CONFIG_SETTINGS_MENU_PASSWORD={password_validity}\n")
                else:
                    updated_lines.append(line)
        with open(config_path, 'w') as file:
            file.writelines(updated_lines)
entry1_has_focus = [False]
ssid_entry_field_has_focus = [False]
def on_password_focus_in(event):
    entry1_has_focus[0] = True
def on_password_focus_out(event):
    entry1_has_focus[0] = False
    root.after(100, lambda: check_password_focus())
def on_ssid_focus_in(event):
    ssid_entry_field_has_focus[0] = True
def check_ssid_focus():
    if not ssid_entry_field_has_focus[0] and root.focus_get() != entry1:
        accept()
def on_ssid_focus_out(event):
    ssid_entry_field_has_focus[0] = False
    root.after(100, lambda: check_ssid_focus())
def check_password_focus():
    if not entry1_has_focus[0] and root.focus_get() !=ssid_entry_field :
        accept()
def jsonsearch():
    global base_json_path
    base_json_path = filedialog.askopenfilename(
        title="Open JSON FILE",
        filetypes=[("JSON Files", "*json")]
    )
    json_file_label.config(text="Copied from: " + base_json_path,font=("Courier",10,"underline"))
root.geometry("600x600")
logo= tk.PhotoImage(file="logo.png") 
logo_label = tk.Label(root, image=logo)
logo_label.pack(side="top",anchor="center")
esp_file_path_frame = tk.Frame(root)
esp_file_path_frame.pack(anchor="w", pady=5, padx=30)
file_path_frame = tk.Frame(root)
file_path_frame.pack(anchor="w", pady=5, padx=30)
json_file_frame= tk.Frame(root)
json_file_frame.pack(anchor="w", pady=5, padx=30)
wifi_row_frame = tk.Frame(root)
wifi_row_frame.pack(anchor="w", pady=5, padx=30)
frame_wifi = tk.Frame(wifi_row_frame)
frame_wifi.grid(row=0, column=1, sticky="nw", pady=5)
Select_esp_file_button = ttk.Button(esp_file_path_frame, text="Select Esp_Path", command=select_esp_file)
Select_esp_file_button.pack(side="left")
Esp_file_path_label= ttk.Label(esp_file_path_frame, text="")
Esp_file_path_label.pack(side="left", padx=10)
file_path_button = ttk.Button(file_path_frame, text="Open ESP-IDF Project", command=open_file)
file_path_button.pack(side="left")
file_path_label = ttk.Label(file_path_frame, text="")
file_path_label.pack(side="left", padx=10)
json_file_button = ttk.Button(json_file_frame, text="Select JSON File", command=jsonsearch)
json_file_button.pack(side="left")
json_file_label = ttk.Label(json_file_frame, text="")
json_file_label.pack(side="left", padx=10)
wifi_checkbutton = ttk.Checkbutton(wifi_row_frame,text="Enable wifi", command=change_password, variable=wifi_value, onvalue=1, offvalue=0, state="disabled")
wifi_checkbutton.grid(row=0, column=0, sticky="nw", padx=(0, 10), pady=5)
pulsator_checkbutton = ttk.Checkbutton(root, text="Pulsator", variable=pulsator_value, onvalue=1, offvalue=0, command=change_pulsator, state="disabled")
pulsator_checkbutton.pack(side="top", anchor="w", pady=5, padx=30)
chant_checkbutton = ttk.Checkbutton(root, text="Chant", variable=chant_value, onvalue=1, offvalue=0, command=change_chant, state="disabled")
chant_checkbutton.pack(side="top", anchor="w", pady=5, padx=30)
settings_menu_frame = tk.Frame(root)
settings_menu_frame.pack(anchor="w", pady=10, padx=30)
Settings_menu_password_label = ttk.Label(settings_menu_frame, text="Menu Settings Password", font=("Courier", 10))
Settings_menu_password_label.pack(side="left", padx=(0, 5))
Setting_menu_password_entryfield = ttk.Entry(settings_menu_frame)
Setting_menu_password_entryfield .pack(side="left")
Setting_menu_password_entryfield_has_focus = [False]
def on_entry_focus_in(event):
    Setting_menu_password_entryfield[0] = True
def on_entry_focus_out(event):
    Setting_menu_password_entryfield[0] = False
    root.after(100, menu_config)
Setting_menu_password_entryfield .bind("<FocusIn>", on_entry_focus_in)
Setting_menu_password_entryfield .bind("<FocusOut>", on_entry_focus_out)
def global_click(event):
    if Setting_menu_password_entryfield[0] and event.widget != Setting_menu_password_entryfield :
        dummy_focus_widget.focus_set()
    if entry1_has_focus[0] and event.widget not in [ssid_entry_field, entry1]:
        dummy_focus_widget.focus_set()
        accept()
    if ssid_entry_field_has_focus[0] and event.widget not in [ssid_entry_field, entry1]:
        dummy_focus_widget.focus_set()
        accept()
dummy_focus_widget = ttk.Entry(root)
dummy_focus_widget.place(x=-100, y=-100)
root.bind("<Button-1>", global_click)
flash_button = ttk.Button(root, text="Flash", command=flash)
flash_button.pack(side="bottom", anchor="e", pady=15, padx=30)
sv_ttk.set_theme("dark")
root.title("Flash Tool")
root.mainloop()
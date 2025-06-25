import tkinter as tk
root=tk.Tk()
root.title("To-Do List")
root.geometry("1000x800")
x=tk.IntVar()
y=tk.IntVar()
def list():
    if x.get()==1:
        print("Drank 1 glass of water")
    else:    
        print("Did not drink 1 glass of water")
def list1():
    if int(y.get)==1:
        print("Ate 1 carrot")
    else:
        print("Did not eat a carrot")        
checkbutton=tk.Checkbutton(root,text="Drink 1 glass of water",font=("Ink Free",20),variable=x,onvalue=1,offvalue=0)
checkbutton1=tk.Checkbutton(root,text="Eat 1 carrot",font=("Ink Free",20),variable=y,onvalue=1,offvalue=0,command=list1)
checkbutton.pack()
checkbutton1.pack()
root.mainloop()
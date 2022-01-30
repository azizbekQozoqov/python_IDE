from tkinter import *
from tkinter.messagebox import showinfo, askquestion, showwarning
import sys
import subprocess, webbrowser, pickle
from tkinter.filedialog import askopenfilename, asksaveasfilename

# app
root = Tk()
root.configure(bg="#000")
if sys.platform == "linux":
    root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='/home/developer/Documents/tkinter/icon.png'))

def execute():
    if get()['path_name']:
        r1 = subprocess.run(['python3', get()['path_name']], capture_output=True, text=True)
        code_output.insert('end', r1.stdout)
        code_output.insert('end', r1.stderr, 'error')
    else:
        result = askquestion('Warn!', 'File is not saved yet!\nDo you want save it?')
        if result == 'yes':
            save_as()
            execute()
        else:
            return

# Menu
menu = Menu(root, bg="#148F77", fg="#fff", font="Bold")

filenenu = Menu(menu, tearoff=0, activebackground="#fff", activeforeground="#27AE60", bg="#148F77", font="Bold 13")
filenenu.add_command(label="Open file",command=lambda : open_file())
filenenu.add_command(label="New file",command=lambda : create_file())
filenenu.add_separator()
filenenu.add_command(label="Save as",command=lambda : save_as())
filenenu.add_command(label="Save",command=lambda : save())
filenenu.add_separator()
filenenu.add_command(label="Exit", command=exit)
menu.add_cascade(menu=filenenu, label="File")

runmenu = Menu(menu, tearoff=0, activebackground="#fff", activeforeground="#27AE60", bg="#148F77", font="Bold 13")
runmenu.add_command(label="Run", command=lambda: execute())
menu.add_cascade(menu=runmenu, label="Run")

helpmenu = Menu(menu,  tearoff=0, activebackground="#fff", activeforeground="#27AE60", bg="#148F77", font="Bold 13")
helpmenu.add_command(label='Keyboard Shortcuts', command=lambda : showinfo('Shortcuts', f'Ctrl + s - Save file\n'))
helpmenu.add_command(label='About this app', command=lambda : showinfo('Info', f'Version 1.0.0\nMade by AzizbekDeveloper'))
helpmenu.add_command(label='Open in Browser', command=lambda : open_browser("https://www.github.com/azizbekQozoqov"))

menu.add_cascade(menu=helpmenu, label='Help')
# editor
editor = Text(root, selectbackground="#148F77", selectforeground="#ffffff", height=16, width=100)
editor.pack(fill=BOTH)



code_output = Text(root, selectbackground="#148F77", selectforeground="#ffffff", height=10, bg='#F7CAC9', fg="#000", font='Monospace 20')
code_output.pack(expand=True, fill=BOTH)
code_output.tag_config('error', foreground="red")

# filemanu commands
def open_file():
    try:
        path = askopenfilename(filetypes=[("Python files", "*.py")])
        update(path)
        with open( get()["path_name"], 'r') as f:
            editor.delete('1.0', END)
            editor.insert('1.0', f.read())
    except :
        showinfo("Info", "Method cancelled")
def create_file():
    try:
        path = asksaveasfilename(filetypes=[("Python files", "*.py")])
        update(path)
        editor.delete("1.0", END)
    except:
        showinfo("Info", "Method cancelled")

def save_as():
    try:
        path = asksaveasfilename(filetypes=[("Python files", "*.py")])
        update(path)
        if path:
            showwarning('Info', f"Current file path changed to\n{path}")
        with open(get()['path_name'], 'w') as f:
            f.write(editor.get("1.0", END))
    except:
        showinfo("Info", "Method cancelled")


def save():
    if not get()['path_name']:
        save_as()
    else:
        with open(get()['path_name'], 'w') as f:
            f.write(editor.get("1.0", END))
def open_browser(url):
    webbrowser.open_new_tab(url)


# others
def update(path):
    with open('./paths.db', 'wb') as f:
        pickle.dump({"path_name":path}, f)
        root.title(path)
def get():
    with open('./paths.db', 'rb') as f:
        return pickle.load(f)



def save_by_keyboard(e):
    if e.state == 4 and e.keysym == 's':
        save()
editor.bind('<Key>', save_by_keyboard)


def t():
    if get()['path_name']:
        try:
            with open(get()['path_name'], 'r') as f:
                editor.insert('1.0', f.read())
                root.title(get()['path_name'])
        except:
            showinfo('Please create a new file!!!', "You have to create new file!")
            path = asksaveasfilename(filetypes=[("Python files", "*.py")])
            if path:
                update(path)
            else:
                t()
t()
# run
root.config(menu=menu)
if __name__ == '__main__':
    root.mainloop()


# <Enter>
# <Leave>
# <Button-1>
# <Button-2>
# <Button-3>
# <FocusIn>
# <FocusOut>
# <Return> - Enter button
# <Key> - All keys
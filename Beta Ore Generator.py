import tkinter as tk
from tkinter import colorchooser
import numpy as np

ore_color = "66ffff"
bgcolor = "606060"
square_len = 16
ore_len = 25
rare = 2
default_values = {
    "ore_color": ("66ffff", "HEX color for ore"),
    "bgcolor": ("606060", "HEX color for stone"),
    "ore_len": (25, "square number for the side"),
    "rare": (2, "ore rareness number"),
    "square_len": (16, "pixel number for the square side")
}

root = tk.Tk()

wn = 0
space = 0
anim = tk.BooleanVar()
optimize = tk.BooleanVar()

def generate():
    global ore_color, bgcolor, ore_len, rare, square_len
    
    if check():
        if optimize.get():
            canvas.config(width=ore_len, height=ore_len)
        else:
            canvas.config(width=ore_len * square_len, height=ore_len * square_len)

        ore_gen()

def check():
    global objects, default_values
    for name,(entry, label) in list(objects.items())[:2]:
        text = entry.get()
        if len(text) != 6:
            label.config(text="HEX color should contain 6 characters", fg="darkred")
            return False
        try:
            int(text, 16)
        except:
            label.config(text=f"Enter valid {default_values[name][1]}", fg="darkred")
            return False

        label.config(text=default_values[name][1], fg="black")

        globals()[name] = text
    
    for name, (entry, label) in list(objects.items())[2:]:
        try:
            num = int(''.join(filter(lambda x: x.isdigit(), entry.get())))
        except:
            label.config(text="", fg="darkred")
            return False

        globals()[name] = num
    
    return True

def color_picker(name):
    global objects, default_values

    rgb, color = colorchooser.askcolor(title=f"{default_values[name][1]}")

    objects[name][0].delete(0, tk.END)
    objects[name][0].insert(0, color[1:])

    globals()[name] = color[1:]

def clear():
    canvas.delete("all")

def advanced():
    global wn
    if wn == 1:
        wn -= 1
        root.geometry(f"{root.winfo_width() - 250}x{root.winfo_height()}")
        adv_settings.pack_forget()
    else:
        wn += 1
        root.geometry(f"{root.winfo_width() + 250}x{root.winfo_height()}")
        adv_settings.pack(side="left", fill="both")

def ore_or_not():           # border=True
    global ore_len, ore_color, bgcolor
    # if border:
    #     border = ore_len // 9
    
    squares = np.random.randint(0, 100, size=(ore_len, ore_len))
    seed = np.random.choice(range(100), size=rare, replace=False)

    sq_color = np.vectorize(lambda x: ore_color if x in seed else bgcolor)
    squares = sq_color(squares)
    return squares

def draw_square(x, y, color):
    global square_len

    x0, y0 = (x * square_len, y * square_len) if not optimize.get() else (x, y)
    x1, y1 = (x0 + square_len, y0 + square_len) if not optimize.get() else (x + 1, y + 1)
    
    canvas.create_rectangle(x0, y0, x1, y1, fill=f"#{color}", outline="")

def scale_canvas():
    global square_len
    if optimize.get() and square_len > 1:
        canvas.scale("all", 0, 0, square_len, square_len)
        canvas.config(width=ore_len * square_len, height=ore_len * square_len)

def ore_gen():
    global squares, square_len
    squares = ore_or_not()
    if anim.get():
        draw_next_square(0, 0)
    else:
        for (x, y), color in np.ndenumerate(squares):
            draw_square(x, y, color)
        scale_canvas()

def draw_next_square(x, y):
    global squares
    if y >= ore_len:
        scale_canvas()
        return
    if x >= ore_len:
        draw_next_square(0, y + 1)
        return
    
    color = squares[y][x]
    draw_square(x, y, color)
    root.after(1, draw_next_square, x + 1, y)

def entryMove(event):
    global objects, space
    entry = [value[0] for value in objects.values()]

    space = entry.index(root.focus_get())

    if space == len(entry)-1:
        space = 0
    else:
        space += 1

    entry[space].focus_set()
    entry[space].select_range(0, tk.END)

    return "break"


root.title("Ore Generator")
root.geometry(f"{ore_len * square_len + 250}x{ore_len * square_len}")

picture = tk.Frame(root,                                                #frame for canvas
    width=ore_len,
    height=ore_len)
picture.pack(side="left", fill="both", expand=True)

settings = tk.Frame(root,                                               #frame for settings
    width=250,
    height=ore_len * square_len,
    # background="lightblue"
    )
settings.pack(side="left", fill="both")

canvas = tk.Canvas(picture,                                             #canvas
    width=ore_len,
    height=ore_len,
    bg='white')
canvas.place(relx=0.5, rely=0.5, anchor="center")

adv_settings = tk.Frame(root,                                           #frame for advanced settings
    width=250,
    height=ore_len * square_len,)

label = tk.Label(settings,                                              #label for the title
    text="Ore Generator",
    font=("Helvetica", 16, "bold"))
label.place(relx=0.5, rely=0.07, anchor="center")

oreColor = tk.Label(settings,                                           #label for ore color
    text="HEX color for ore",
    font=("", 10))
oreColor.place(relx=0.5, rely=0.15, anchor="center")

choose_ore_color = tk.Button(settings,                                  #button to open ore color picker
    text="🖌",
    command=lambda: color_picker("ore_color"))
choose_ore_color.place(relx=0.1, rely=0.2, anchor="center")

ore_color_entry = tk.Entry(settings,                                    #entry for ore color
    justify="center")
ore_color_entry.insert(0, default_values["ore_color"][0])
ore_color_entry.place(relx=0.45, rely=0.2, anchor="center")

ore_color_default = tk.Button(settings,                                 #button for setting ore color to default
    text="default",
    command=lambda: default("ore_color"))
ore_color_default.place(relx=0.85, rely=0.2, anchor="center")

bgColor = tk.Label(settings,                                            #label for bgcolor
    text="HEX color for stone",
    font=("", 10))
bgColor.place(relx=0.5, rely=0.26, anchor="center")

choose_bgcolor = tk.Button(settings,                                  #button to open bgcolor picker
    text="🖌",
    command=lambda: color_picker("bgcolor"))
choose_bgcolor.place(relx=0.1, rely=0.31, anchor="center")

bg_color_entry = tk.Entry(settings,                                     #entry for bgcolor
    justify="center")
bg_color_entry.insert(0, default_values["bgcolor"][0])
bg_color_entry.place(relx=0.45, rely=0.31, anchor="center")

bg_color_default = tk.Button(settings,                                  #button for setting bg color to default
    text="default",
    command=lambda: default("bgcolor"))
bg_color_default.place(relx=0.85, rely=0.31, anchor="center")

oreLen = tk.Label(settings,                                             #label for ore_len
    text="square number for the side",
    font=("", 10))
oreLen.place(relx=0.5, rely=0.37, anchor="center")

ore_len_entry = tk.Entry(settings,                                      #entry for ore_len
    justify="center")
ore_len_entry.insert(0, default_values["ore_len"][0])
ore_len_entry.place(relx=0.37, rely=0.42, anchor="center")

ore_len_default = tk.Button(settings,                                   #button for setting ore len to default
    text="default",
    command=lambda: default("ore_len"))
ore_len_default.place(relx=0.8, rely=0.42, anchor="center")

Rare = tk.Label(settings,                                               #label for rare
    text="Enter rareness of ore appearance",
    font=("", 10))
Rare.place(relx=0.5, rely=0.48, anchor="center")

rare_entry = tk.Entry(settings,                                         #entry for rare
    justify="center")
rare_entry.insert(0, default_values["rare"][0])
rare_entry.place(relx=0.37, rely=0.53, anchor="center")

rare_default = tk.Button(settings,                                      #button for setting rare to default
    text="default",
    command=lambda: default("rare"))
rare_default.place(relx=0.8, rely=0.53, anchor="center")

squareLen = tk.Label(settings,                                          #label for square_len
    text="pixel number for the square side",
    font=("", 10))
squareLen.place(relx=0.5, rely=0.59, anchor="center")

square_len_entry = tk.Entry(settings,                                   #entry for square_len
    justify="center")
square_len_entry.insert(0, default_values["square_len"][0])
square_len_entry.place(relx=0.37, rely=0.64, anchor="center")

square_len_default = tk.Button(settings,                                #button for setting square len to default
    text="default",
    command=lambda: default("square_len"))
square_len_default.place(relx=0.8, rely=0.64, anchor="center")

anim_check = tk.Checkbutton(settings,                                   #checkbutton for animation
    text="animate generation",
    font=("Helvetica", 10),
    variable=anim)
anim_check.place(relx=0.5, rely=0.71, anchor="center")

optimize_check = tk.Checkbutton(settings,                                   #checkbutton for optimisation
    text="optimize",
    font=("Helvetica", 10),
    variable=optimize)
optimize_check.place(relx=0.5, rely=0.76, anchor="center")

adv_settings_button = tk.Button(settings,                               #button for adv_settings
    text="Advanced settings",
    font=("Helvetica", 11),
    command=advanced)
adv_settings_button.place(relx=0.5, rely=0.84, anchor="center")

clear_button = tk.Button(settings,                                      #button for canvas clearness
    text="Clear",
    font=("Helvetica", 13, "italic"),
    command=clear)
clear_button.place(relx=0.72, rely=0.94, anchor="center")

gen_button = tk.Button(settings,                                        #button for ore generation
    text="Generate!",
    font=("Helvetica", 16, "italic"),
    command=generate)
gen_button.place(relx=0.36, rely=0.94, anchor="center")

root.bind('<Return>', lambda event: generate())
root.bind('<Tab>', entryMove)

objects = {
    # "variable": (entry, label)
    "ore_color": (ore_color_entry, oreColor),
    "bgcolor": (bg_color_entry, bgColor),
    "ore_len": (ore_len_entry, oreLen),
    "rare": (rare_entry, Rare),
    "square_len": (square_len_entry, squareLen)
}

def default(entry):
    global default_values, objects
    objects[entry][0].delete(0, tk.END)
    objects[entry][0].insert(0, default_values[entry][0])

root.mainloop()

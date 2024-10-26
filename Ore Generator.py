import tkinter as tk
import numpy as np

bgcolor = "606060"
d_bgcolor = "606060"
ore_color = "66ffff"
d_ore_color = "66ffff"
square_len = 16
d_square_len = 16
ore_len = 25
d_ore_len = 25
rare = 2
d_rare = 2

root = tk.Tk()

wn = 0
space = 0
anim = tk.BooleanVar()
optimize = tk.BooleanVar()

def generate():
    global ore_color, bgcolor, ore_len, rare, square_len
    try:
        entry = ore_color_entry.get()
        a = int(entry, 16)
        if a <= 16777215 and a >= 0 and len(entry) == 6:
            oreColor.config(text="Enter RGB color for ore", fg="black")
    except:
        oreColor.config(text="Enter valid HEX color for ore", fg="red")

    try:
        entry = bg_color_entry.get()
        a = int(entry, 16)
        if a <= 16777215 and a >= 0 and len(entry) == 6:
            bgColor.config(text="Enter RGB color for stone", fg="black")
    except:
        bgColor.config(text="Enter valid HEX color for ore", fg="red")

    ore_color = ore_color_entry.get()
    bgcolor = bg_color_entry.get()
    ore_len = int(ore_len_entry.get())
    rare = int(rare_entry.get())
    square_len = int(square_len_entry.get())

    if optimize.get():
        canvas.config(width=ore_len, height=ore_len)
    else:
        canvas.config(width=ore_len * square_len, height=ore_len * square_len)
    if ore_color and bgcolor:
        ore_gen()

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
    
    squares = np.random.randint(0, 25, size=(ore_len, ore_len))
    seed = np.random.choice(range(25), size=rare, replace=False)

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
    global squares, drawTime, drawStart, allTime
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
    global space
    entry = [ore_color_entry, bg_color_entry, ore_len_entry, rare_entry, square_len_entry]

    entry[space].focus_set()
    entry[space].select_range(0, tk.END)

    if space == len(entry)-1:
        space = 0
    else:
        space += 1
    
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
    text="Enter RGB color for ore",
    font=("", 10))
oreColor.place(relx=0.5, rely=0.15, anchor="center")

ore_color_entry = tk.Entry(settings,                                    #entry for ore color
    justify="center")
ore_color_entry.insert(0, d_ore_color)
ore_color_entry.place(relx=0.37, rely=0.2, anchor="center")

ore_color_default = tk.Button(settings,                                 #button for setting ore color to default
    text="default",
    command=lambda: default("ore_color"))
ore_color_default.place(relx=0.8, rely=0.2, anchor="center")

bgColor = tk.Label(settings,                                            #label for bgcolor
    text="Enter RGB color for stone",
    font=("", 10))
bgColor.place(relx=0.5, rely=0.26, anchor="center")

bg_color_entry = tk.Entry(settings,                                     #entry for bgcolor
    justify="center")
bg_color_entry.insert(0, d_bgcolor)
bg_color_entry.place(relx=0.37, rely=0.31, anchor="center")

bg_color_default = tk.Button(settings,                                  #button for setting bg color to default
    text="default",
    command=lambda: default("bgcolor"))
bg_color_default.place(relx=0.8, rely=0.31, anchor="center")

oreLen = tk.Label(settings,                                             #label for ore_len
    text="Enter square number for the side",
    font=("", 10))
oreLen.place(relx=0.5, rely=0.37, anchor="center")

ore_len_entry = tk.Entry(settings,                                      #entry for ore_len
    justify="center")
ore_len_entry.insert(0, d_ore_len)
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
rare_entry.insert(0, d_rare)
rare_entry.place(relx=0.37, rely=0.53, anchor="center")

rare_default = tk.Button(settings,                                      #button for setting rare to default
    text="default",
    command=lambda: default("rare"))
rare_default.place(relx=0.8, rely=0.53, anchor="center")

squareLen = tk.Label(settings,                                          #label for square_len
    text="Enter pixel number for the pixel side",
    font=("", 10))
squareLen.place(relx=0.5, rely=0.59, anchor="center")

square_len_entry = tk.Entry(settings,                                   #entry for square_len
    justify="center")
square_len_entry.insert(0, d_square_len)
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

d_entries = {
    # "parameter": (entry, default_value)
    "ore_color": (ore_color_entry, d_ore_color),
    "bgcolor": (bg_color_entry, d_bgcolor),
    "ore_len": (ore_len_entry, d_ore_len),
    "rare": (rare_entry, d_rare),
    "square_len": (square_len_entry, d_square_len)
}

def default(entry):
    global d_entries
    d_entries[entry][0].delete(0, tk.END)
    d_entries[entry][0].insert(0, d_entries[entry][1])

root.mainloop()

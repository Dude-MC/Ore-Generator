import tkinter as tk
import random as rd

bgcolor = "606060"
d_bgcolor = "606060"
ore_color = "66ffff"
d_ore_color = "66ffff"
square_len = 16
d_square_len = 16
ore_len = 25
d_ore_len = 25
rare = 4
d_rare = 4
wn = 0

def generate():
    global ore_color, bgcolor, ore_len, rare, square_len
    try:
        entry = ore_color_entry.get()
        a = int(entry, 16)
        if a <= 16777215 and a >= 0 and len(entry) == 6:                    # check this
            ore_color = True
    except:
        oreColor.config(text="Enter valid HEX color for ore", fg="red")     # print return to end the func
    else:
        oreColor.config(text="Enter RGB color for ore", fg="black")

    try:
        entry = bg_color_entry.get()
        a = int(entry, 16)
        if a <= 16777215 and a >= 0 and len(entry) == 6:                    # check this
            bgcolor = True
    except:
        bgColor.config(text="Enter valid HEX color for ore", fg="red")      # print return to end the func
    else:
        bgColor.config(text="Enter RGB color for stone", fg="black")
    ore_color = ore_color_entry.get()
    bgcolor = bg_color_entry.get()
    ore_len = int(ore_len_entry.get())
    rare = int(rare_entry.get())
    square_len = int(square_len_entry.get())

    canvas.config(width=ore_len * square_len,
                       height=ore_len * square_len)
    if ore_color and bgcolor:
        ore_gen()

def clear():
    canvas.delete("all")
    # ore_color_entry.delete(0, tk.END)
    # bg_color_entry.delete(0, tk.END)
    # ore_len_entry.delete(0, tk.END)
    # rare_entry.delete(0, tk.END)
    # square_len_entry.delete(0, tk.END)

def default(entry):
    if entry == "ore_color":
        ore_color_entry.delete(0, tk.END)
        ore_color_entry.insert(0, d_ore_color)
    elif entry == "bgcolor":
        bg_color_entry.delete(0, tk.END)
        bg_color_entry.insert(0, d_bgcolor)
    elif entry == "ore_len":
        ore_len_entry.delete(0, tk.END)
        ore_len_entry.insert(0, d_ore_len)
    elif entry == "rare":
        rare_entry.delete(0, tk.END)
        rare_entry.insert(0, d_rare)
    elif entry == "square_len":
        square_len_entry.delete(0, tk.END)
        square_len_entry.insert(0, d_square_len)

def advanced():
    if wn == 1:
        wn -= 1
        root.geometry(f"{root.winfo_width() - 250}x{root.winfo_height()}")
        adv_settings.pack_forget()
    else:
        wn += 1
        root.geometry(f"{root.winfo_width() + 250}x{root.winfo_height()}")
        adv_settings.pack(side="left", fill="both")

def ore_or_not(border=True):
    if border:
        border = ore_len // 9
    # add else statement, changing border to int
    squares = {}
    a = int("1"+"0"*(ore_len-1))
    b = int("9"*ore_len)
    for y in range(ore_len):
        seed = str(rd.randint(a, b))
        for x in range(ore_len):
            if int(seed[x]) % 2 == 0:
                squares[(x, y)] = ore_color
            else:
                squares[(x, y)] = bgcolor
    
    return squares


    # for y in range(ore_len):
    #     for x in range(ore_len):
    #         is_ore = rd.randint(1, rare) == 1
    #         color = ore_color if is_ore else bgcolor
    #         squares[(x, y)] = color
                
        #         will be deleted


# def processing1():
#     for (x, y), color in squares.items():
#         if color == ore_color:
#             r = rd.randint(1, 3) == 1

#             func processing is in creation progress

def draw_square(x, y, color):
    x0 = x * square_len
    y0 = y * square_len
    x1 = x0 + square_len
    y1 = y0 + square_len
    canvas.create_rectangle(x0, y0, x1, y1,
                                 fill=f"#{color}", outline="")

def ore_gen():
    for (x, y), color in ore_or_not().items():
        draw_square(x, y, color)

root = tk.Tk()
root.title("Ore Generator")
root.geometry(f"{ore_len * square_len + 250}x{ore_len * square_len}")

picture = tk.Frame(root,                                                #frame for canvas
    width=ore_len * square_len,
    height=ore_len * square_len)
picture.pack(side="left", fill="both", expand=True)

settings = tk.Frame(root,                                               #frame for settings
    width=250,
    height=ore_len * square_len,)
settings.pack(side="left", fill="both")

canvas = tk.Canvas(picture,                                             #canvas
    width=ore_len * square_len,
    height=ore_len * square_len,
    bg='white')
canvas.place(relx=0.5, rely=0.5, anchor="center")

adv_settings = tk.Frame(root,                                           #frame for advanced settings
    width=250,
    height=ore_len * square_len,)

label = tk.Label(settings,                                              #label for the title
    text="Ore Generator 3.0",
    font=("Helvetica", 16, "bold"))
label.place(relx=0.5, rely=0.1, anchor="center")

oreColor = tk.Label(settings,                                           #label for ore color
    text="Enter RGB color for ore",
    font=("", 10))
oreColor.place(relx=0.5, rely=0.17, anchor="center")

ore_color_entry = tk.Entry(settings,                                    #entry for ore color
    justify="center")
ore_color_entry.insert(0, d_ore_color)
ore_color_entry.place(relx=0.37, rely=0.22, anchor="center")

ore_color_default = tk.Button(settings,                                 #button for setting ore color to default
    text="default",
    command=lambda: default("ore_color"))
ore_color_default.place(relx=0.8, rely=0.22, anchor="center")

bgColor = tk.Label(settings,                                            #label for bgcolor
    text="Enter RGB color for stone",
    font=("", 10))
bgColor.place(relx=0.5, rely=0.28, anchor="center")

bg_color_entry = tk.Entry(settings,                                     #entry for bgcolor
    justify="center")
bg_color_entry.insert(0, d_bgcolor)
bg_color_entry.place(relx=0.37, rely=0.33, anchor="center")

bg_color_default = tk.Button(settings,                                  #button for setting bg color to default
    text="default",
    command=lambda: default("bgcolor"))
bg_color_default.place(relx=0.8, rely=0.33, anchor="center")

oreLen = tk.Label(settings,                                             #label for ore_len
    text="Enter square number for the side",
    font=("", 10))
oreLen.place(relx=0.5, rely=0.39, anchor="center")

ore_len_entry = tk.Entry(settings,                                      #entry for ore_len
    justify="center")
ore_len_entry.insert(0, d_ore_len)
ore_len_entry.place(relx=0.37, rely=0.44, anchor="center")

ore_len_default = tk.Button(settings,                                   #button for setting ore len to default
    text="default",
    command=lambda: default("ore_len"))
ore_len_default.place(relx=0.8, rely=0.44, anchor="center")

Rare = tk.Label(settings,                                               #label for rare
    text="Enter rareness of ore appearance",
    font=("", 10))
Rare.place(relx=0.5, rely=0.5, anchor="center")

rare_entry = tk.Entry(settings,                                         #entry for rare
    justify="center")
rare_entry.insert(0, d_rare)
rare_entry.place(relx=0.37, rely=0.55, anchor="center")

rare_default = tk.Button(settings,                                      #button for setting rare to default
    text="default",
    command=lambda: default("rare"))
rare_default.place(relx=0.8, rely=0.55, anchor="center")

squareLen = tk.Label(settings,                                          #label for square_len
    text="Enter pixel number for the pixel side",
    font=("", 10))
squareLen.place(relx=0.5, rely=0.61, anchor="center")

square_len_entry = tk.Entry(settings,                                   #entry for square_len
    justify="center")
square_len_entry.insert(0, d_square_len)
square_len_entry.place(relx=0.37, rely=0.66, anchor="center")

square_len_default = tk.Button(settings,                                #button for setting square len to default
    text="default",
    command=lambda: default("square_len"))
square_len_default.place(relx=0.8, rely=0.66, anchor="center")

gen_button = tk.Button(settings,                                        #button for ore generation
    text="Generate!",
    font=("Helvetica", 16, "italic"),
    command=generate)
gen_button.place(relx=0.5, rely=0.92, anchor="center")

clear_button = tk.Button(settings,                                      #button for canvas and entries clearness
    text="Clear",
    font=("Helvetica", 10, "italic"),
    command=clear)
clear_button.place(relx=0.5, rely=0.83, anchor="center")

adv_settings_button = tk.Button(settings,                               #button for adv_settings
    text="Advanced settings",
    font=("Helvetica", 10),
    command=advanced)
adv_settings_button.place(relx=0.5, rely=0.73, anchor="center")

root.mainloop()

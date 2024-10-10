import tkinter as tk
import random as rd

class Ore:
    def __init__(self, ore_color="66ffff", bgcolor="606060", square_len=16, ore_len=25, rare=4):
        self.bgcolor = bgcolor
        self.d_bgcolor = bgcolor
        self.ore_color = ore_color
        self.d_ore_color = ore_color
        self.square_len = square_len
        self.d_square_len = square_len
        self.ore_len = ore_len
        self.d_ore_len = ore_len
        self.rare = rare
        self.d_rare = rare
        self.wn = 0

    def setting_up(self):
        self.root = tk.Tk()
        self.root.title("Ore Generator")
        self.root.geometry(f"{self.ore_len * self.square_len + 250}x{self.ore_len * self.square_len}")

        self.picture = tk.Frame(self.root,                                      #frame for canvas
            width=self.ore_len * self.square_len,
            height=self.ore_len * self.square_len)
        self.picture.pack(side="left", fill="both", expand=True)

        self.settings = tk.Frame(self.root,                                     #frame for settings
            width=250,
            height=self.ore_len * self.square_len,)
        self.settings.pack(side="left", fill="both")

        self.canvas = tk.Canvas(self.picture,                                   #canvas
            width=self.ore_len * self.square_len,
            height=self.ore_len * self.square_len,
            bg='white')
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")

        self.adv_settings = tk.Frame(self.root,                                     #frame for advanced settings
            width=250,
            height=self.ore_len * self.square_len,)

        self.label = tk.Label(self.settings,                                    #label for the title
            text="Ore Generator 3.0",
            font=("Helvetica", 16, "bold"))
        self.label.place(relx=0.5, rely=0.1, anchor="center")

        self.oreColor = tk.Label(self.settings,                                 #label for ore color
            text="Enter RGB color for ore",
            font=("", 10))
        self.oreColor.place(relx=0.5, rely=0.17, anchor="center")

        self.ore_color_entry = tk.Entry(self.settings,                          #entry for ore color
            justify="center")
        self.ore_color_entry.insert(0, self.d_ore_color)
        self.ore_color_entry.place(relx=0.37, rely=0.22, anchor="center")

        self.ore_color_default = tk.Button(self.settings,                       #button for setting ore color to default
            text="default",
            command=lambda: self.default("ore_color"))
        self.ore_color_default.place(relx=0.8, rely=0.22, anchor="center")

        self.bgColor = tk.Label(self.settings,                                  #label for bgcolor
            text="Enter RGB color for stone",
            font=("", 10))
        self.bgColor.place(relx=0.5, rely=0.28, anchor="center")

        self.bg_color_entry = tk.Entry(self.settings,                           #entry for bgcolor
            justify="center")
        self.bg_color_entry.insert(0, self.d_bgcolor)
        self.bg_color_entry.place(relx=0.37, rely=0.33, anchor="center")

        self.bg_color_default = tk.Button(self.settings,                        #button for setting bg color to default
            text="default",
            command=lambda: self.default("bgcolor"))
        self.bg_color_default.place(relx=0.8, rely=0.33, anchor="center")

        self.oreLen = tk.Label(self.settings,                                   #label for ore_len
            text="Enter square number for the side",
            font=("", 10))
        self.oreLen.place(relx=0.5, rely=0.39, anchor="center")

        self.ore_len_entry = tk.Entry(self.settings,                            #entry for ore_len
            justify="center")
        self.ore_len_entry.insert(0, self.d_ore_len)
        self.ore_len_entry.place(relx=0.37, rely=0.44, anchor="center")

        self.ore_len_default = tk.Button(self.settings,                         #button for setting ore len to default
            text="default",
            command=lambda: self.default("ore_len"))
        self.ore_len_default.place(relx=0.8, rely=0.44, anchor="center")

        self.Rare = tk.Label(self.settings,                                     #label for rare
            text="Enter rareness of ore appearance",
            font=("", 10))
        self.Rare.place(relx=0.5, rely=0.5, anchor="center")

        self.rare_entry = tk.Entry(self.settings,                               #entry for rare
            justify="center")
        self.rare_entry.insert(0, self.d_rare)
        self.rare_entry.place(relx=0.37, rely=0.55, anchor="center")

        self.rare_default = tk.Button(self.settings,                            #button for setting rare to default
            text="default",
            command=lambda: self.default("rare"))
        self.rare_default.place(relx=0.8, rely=0.55, anchor="center")

        self.squareLen = tk.Label(self.settings,                                #label for square_len
            text="Enter pixel number for the pixel side",
            font=("", 10))
        self.squareLen.place(relx=0.5, rely=0.61, anchor="center")

        self.square_len_entry = tk.Entry(self.settings,                         #entry for square_len
            justify="center")
        self.square_len_entry.insert(0, self.d_square_len)
        self.square_len_entry.place(relx=0.37, rely=0.66, anchor="center")

        self.square_len_default = tk.Button(self.settings,                      #button for setting square len to default
            text="default",
            command=lambda: self.default("square_len"))
        self.square_len_default.place(relx=0.8, rely=0.66, anchor="center")

        self.gen_button = tk.Button(self.settings,                              #button for ore generation
            text="Generate!",
            font=("Helvetica", 16, "italic"),
            command=self.generate)
        self.gen_button.place(relx=0.5, rely=0.92, anchor="center")

        self.clear_button = tk.Button(self.settings,                            #button for canvas and entries clearness
            text="Clear",
            font=("Helvetica", 10, "italic"),
            command=self.clear)
        self.clear_button.place(relx=0.5, rely=0.83, anchor="center")

        self.adv_settings_button = tk.Button(self.settings,
            text="Advanced settings",
            font=("Helvetica", 10),
            command=self.advanced)
        self.adv_settings_button.place(relx=0.5, rely=0.73, anchor="center")
        
        self.root.mainloop()
    
    def generate(self):
        try:
            entry = self.ore_color_entry.get()
            a = int(entry, 16)
            if a <= 16777215 and a >= 0 and len(entry) == 6:                    # check this
                ore_color = True
        except:
            self.oreColor.config(text="Enter valid HEX color for ore", fg="red")# print return to end the func
        else:
            self.oreColor.config(text="Enter RGB color for ore", fg="black")

        try:
            entry = self.bg_color_entry.get()
            a = int(entry, 16)
            if a <= 16777215 and a >= 0 and len(entry) == 6:                    # check this
                bgcolor = True
        except:
            self.bgColor.config(text="Enter valid HEX color for ore", fg="red") # print return to end the func
        else:
            self.bgColor.config(text="Enter RGB color for stone", fg="black")
        self.ore_color = self.ore_color_entry.get()
        self.bgcolor = self.bg_color_entry.get()
        self.ore_len = int(self.ore_len_entry.get())
        self.rare = int(self.rare_entry.get())
        self.square_len = int(self.square_len_entry.get())

        self.canvas.config(width=self.ore_len * self.square_len,
                           height=self.ore_len * self.square_len)
        if ore_color and bgcolor:
            self.ore_gen()
    
    def clear(self):
        self.canvas.delete("all")
        self.ore_color_entry.delete(0, tk.END)
        self.bg_color_entry.delete(0, tk.END)
        self.ore_len_entry.delete(0, tk.END)
        self.rare_entry.delete(0, tk.END)
        self.square_len_entry.delete(0, tk.END)
    
    def default(self, entry):
        if entry == "ore_color":
            self.ore_color_entry.delete(0, tk.END)
            self.ore_color_entry.insert(0, self.d_ore_color)
        elif entry == "bgcolor":
            self.bg_color_entry.delete(0, tk.END)
            self.bg_color_entry.insert(0, self.d_bgcolor)
        elif entry == "ore_len":
            self.ore_len_entry.delete(0, tk.END)
            self.ore_len_entry.insert(0, self.d_ore_len)
        elif entry == "rare":
            self.rare_entry.delete(0, tk.END)
            self.rare_entry.insert(0, self.d_rare)
        elif entry == "square_len":
            self.square_len_entry.delete(0, tk.END)
            self.square_len_entry.insert(0, self.d_square_len)

    def advanced(self):
        if self.wn == 1:
            self.wn -= 1
            self.root.geometry(f"{self.root.winfo_width() - 250}x{self.root.winfo_height()}")
            self.adv_settings.pack_forget()
        else:
            self.wn += 1
            self.root.geometry(f"{self.root.winfo_width() + 250}x{self.root.winfo_height()}")
            self.adv_settings.pack(side="left", fill="both")

    def ore_or_not(self, border=True):
        if border:
            border = self.ore_len // 9
        # add else statenebt, changing border to int
        self.squares = {}
        a = int("1"+"0"*(self.ore_len-1))
        b = int("9"*self.ore_len)
        for y in range(self.ore_len):
            seed = rd.randint(a, b)
            for x in range(self.ore_len):
                


        # for y in range(self.ore_len):
        #     self.rare += rare_increase
        #     for x in range(self.ore_len):
        #         if x in range(self.ore_len // border)\
        #             or x in range(self.ore_len - self.ore_len // border, self.ore_len)\
        #             or y in range(self.ore_len // border)\
        #             or y in range(self.ore_len - self.ore_len // border, self.ore_len):
        #             rare = self.rare * extra_rare
        #         else:
        #             rare = self.rare
        #         is_ore = rd.randint(1, rare) == 1
        #         color = self.ore_color if is_ore else self.bgcolor
        #         self.squares[(x, y)] = color
                
    def processing1(self):
        for (x, y), color in self.squares.items():
            if color == self.ore_color:
                r = rd.randint(1, 3) == 1

    def draw_square(self, x, y, color):
        x0 = x * self.square_len
        y0 = y * self.square_len
        x1 = x0 + self.square_len
        y1 = y0 + self.square_len
        self.canvas.create_rectangle(x0, y0, x1, y1,
                                     fill=f"#{color}", outline="")

    def ore_gen(self):
        self.ore_or_not()
        for (x, y), color in self.squares.items():
            self.draw_square(x, y, color)

ore = Ore()
ore.setting_up()

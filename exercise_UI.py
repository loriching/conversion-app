from tkinter import *
import tkinter as tk
from tkinter import ttk
from collections import defaultdict

class Imperial:
    conversion_dict = defaultdict(lambda: "Invalid unit")
    conversion_dict["grams"] = 28.3495231
    conversion_dict["kilograms"] = 0.0283494899964

    conversion_dict["centimeters"] = 2.54
    conversion_dict["meters"] = 0.0254
    conversion_dict["kilometers"] = 0.0000254

    conversion_dict["milliliters"] = 29.573529
    conversion_dict["liters"] = 0.029574

    weightlist = ["grams", "kilograms"]
    lengthlist = ["centimeters", "meters", "kilometers"]
    
    def __init__(self, ounces=0, pounds=0, inches=0, feet=0, miles=0, floz=0, gallons=0):
        self.weight = ounces + 16*pounds
        self.length = inches + 12*feet + 12*5280*miles
        self.volume = floz + 128*gallons

    def set_weight(self,oz,lb):
        self.weight = oz + 16*lb
    def set_length(self,inches,feet,miles):
        self.length = inches + 12*feet + 12*5280*miles
    def set_volume(self,floz,gal):
        self.volume = floz + 128*gal
    
    def convert(self, convert_to):
        if convert_to in Imperial.weightlist:
            self.weight *= Imperial.conversion_dict[convert_to]
            return self.weight
        elif convert_to in Imperial.lengthlist:
            self.length *= Imperial.conversion_dict[convert_to]
            return self.length
        else:
            self.volume *= Imperial.conversion_dict[convert_to]
            return self.volume

    def reset(self):
        self.weight = 0
        self.length = 0
        self.volume = 0

    def __del__(self):
        del self.weight
        del self.length
        del self.volume

class Metric:
    conversion_dict = defaultdict(lambda: "Invalid unit")
    conversion_dict["ounces"] = 0.03527396
    conversion_dict["pounds"] = 0.00220462

    conversion_dict["inches"] = 0.39370079 
    conversion_dict["feet"] = 0.0328084
    conversion_dict["miles"] = 0.00000621

    conversion_dict["fluid ounces"] = 0.03381402
    conversion_dict["gallons"] = 0.00026417

    weightlist = ["ounces", "pounds"]
    lengthlist = ["inches", "feet", "miles"]

    def __init__(self, grams=0, cm=0, mil=0):
        self.weight = grams
        self.length = cm
        self.volume = mil
    
    def set_weight(self,grams,kg):
        self.weight = grams + kg*1000
    def set_length(self,cm,m,km):
        self.length = cm + 100*m + 100*1000*km
    def set_volume(self,mil,L):
        self.volume = mil + 1000*L

    def convert(self, convert_to):
        if convert_to in Metric.weightlist:
            self.weight *= Metric.conversion_dict[convert_to]
            return self.weight
        elif convert_to in Metric.lengthlist:
            self.length *= Metric.conversion_dict[convert_to]
            return self.length
        else:
            self.volume *= Metric.conversion_dict[convert_to]
            return self.volume
    
    def reset(self):
        self.weight = 0
        self.length = 0
        self.volume = 0

    def __del__(self):
        del self.weight
        del self.length
        del self.volume

# Radio Button Set1:  Allow user to select Imperial or Metric Unit.
def unit_type():
    for widget in (rb_frame1.winfo_children() or rb_frame2.winfo_children()):
        widget.destroy()
    
    global selected_type 
    selected_type = tk.StringVar()
    options = ("Imperial to Metric", "Metric to Imperial")

    label = tk.Label(rb_frame1, text="Select input type:", font=("Calibri",16), bd=4)
    label.pack()

    for option in options:
        r = ttk.Radiobutton(rb_frame1, text=option, value=option, variable=selected_type, command=unit_category)
        r.pack()
    
    style.configure("TRadiobutton", font=("Calibri",12))
    
    rb_frame1.pack()

# Radio Button Set2:  Allow user to select the Measurement Types.
def unit_category():
    global selected_category
    selected_category = tk.StringVar()

    for widget in rb_frame2.winfo_children():
        widget.destroy()

    options = ("Weight", "Length", "Volume")

    label = tk.Label(rb_frame2, text="Select conversion: ", font=("Calibri",16), bd=4)
    label.pack()

    for option in options:
        r = ttk.Radiobutton(rb_frame2, text=option, value=option, variable=selected_category, command=listbox)
        r.pack()
    
    rb_frame2.pack()

# ListBox: Displays the Unit types for the selected Measurement Type.
def listbox():
    for widget in lb_frame.winfo_children():
        widget.destroy()

    imperial_units = [["pounds (lb) to kilograms (kg)", "ounces (oz) to grams (g)"], ["miles (mi) to kilometers (km)", "feet (ft) to meters (m)", "inches (in) to centimeters (cm)"], ["gallons (gal) to liters (L)", "fluid ounces (floz) to milliliters (mL)"]]
    metric_units = [["kilograms (kg) to pounds (lb)", "grams (g) to ounces (oz)"], ["kilometers (km) to miles (mi)", "meters (m) to feet (ft)", "centimeters (cm) to inches (in)"], ["liters (L) to gallons (gal)", "milliliters (mL) to fluid ounces (floz)"]]

    if selected_type.get()=="Imperial to Metric":
        if selected_category.get()=="Weight":
            unit_list = imperial_units[0]
        elif selected_category.get()=="Length":
            unit_list = imperial_units[1]
        else:
            unit_list = imperial_units[2]
    else:
        if selected_category.get()=="Weight":
            unit_list = metric_units[0]
        elif selected_category.get()=="Length":
            unit_list = metric_units[1]
        else:
            unit_list = metric_units[2]

    listbox = Listbox(lb_frame, bg="white", font=("Calibri",11), fg="black", width=40)
    label = Label(lb_frame, text="{} {} Units".format(selected_type.get().split()[0], selected_category.get()), font=("Calibri",12))

    for i in range(len(unit_list)):
        listbox.insert(i, unit_list[i])
    
    def go(event):
        cs = listbox.curselection()
        unit = listbox.get(cs)
        user_textbox(unit)
    
    listbox.bind("<Double-1>",go)
    #style.configure()
    
    label.pack()
    listbox.pack()
    lb_frame.pack(side=tk.LEFT, padx=80)

# Textbox1: Allows user to input a value to convert.
def user_textbox(user_unit):
    def config_textboxes(tb, new_value):
        tb.config(state="normal")
        tb.delete(1.0, "end")
        tb.insert("end",new_value)
        tb.config(state="disabled")

    def convert():
        inp = (user_textbox.get(1.0, "end-1c"))

        if not inp:
            result_textbox.config(state="normal")
            result_textbox.delete(1.0, "end")
            result_textbox.config(state="disabled")
            return
                
        if selected_type.get()=="Imperial to Metric":
            im = Imperial()
            if selected_category.get()=="Weight":
                if user_unit=="pounds (lb) to kilograms (kg)":
                    im.set_weight(0,float(inp))
                    config_textboxes(result_textbox, im.convert("kilograms"))
                else:
                    im.set_weight(float(inp),0)
                    config_textboxes(result_textbox, im.convert("grams"))
            elif selected_category.get()=="Length":
                if user_unit=="miles (mi) to kilometers (km)":
                    im.set_length(0,0,float(inp))
                    config_textboxes(result_textbox, im.convert("kilometers"))
                elif user_unit=="feet (ft) to meters (m)":
                    im.set_length(0,float(inp),0)
                    config_textboxes(result_textbox, im.convert("meters"))
                else:
                    im.set_length(float(inp),0,0)
                    config_textboxes(result_textbox, im.convert("centimeters"))
            else:
                if user_unit=="gallons (gal) to liters (L)":
                    im.set_volume(0,float(inp))
                    config_textboxes(result_textbox, im.convert("liters"))
                else:
                    im.set_volume(float(inp),0)
                    config_textboxes(result_textbox, im.convert("milliliters"))
        else:
            met = Metric()
            if selected_category.get()=="Weight":
                if user_unit=="kilograms (kg) to pounds (lb)":
                    met.set_weight(0,float(inp))
                    config_textboxes(result_textbox, met.convert("pounds"))
                else:
                    met.set_weight(float(inp),0)
                    config_textboxes(result_textbox, met.convert("ounces"))
            elif selected_category.get()=="Length":
                if user_unit=="kilometers (km) to miles (mi)":
                    met.set_length(0,0,float(inp))
                    config_textboxes(result_textbox, met.convert("miles"))
                elif user_unit=="meters (m) to feet (ft)":
                    met.set_length(0,float(inp),0)
                    config_textboxes(result_textbox, met.convert("feet"))
                else:
                    met.set_length(float(inp),0,0)
                    config_textboxes(result_textbox, met.convert("inches"))
            else:
                if user_unit=="liters (L) to gallons (gal)":
                    met.set_volume(0,float(inp))
                    config_textboxes(result_textbox, met.convert("gallons"))
                else:
                    met.set_volume(float(inp),0)
                    config_textboxes(result_textbox, met.convert("fluid ounces"))

    def generate_conversion_label():
        imperial = ["Pounds","Ounces","Miles","Feet","Inches","Gallons","Fluid Ounces"]
        metric = ["Kilograms","Grams","Kilometers","Meters","Centimeters","Liters","Milliliters"]

        imperial_dict = dict(zip(imperial, metric))
        metric_dict = dict(zip(metric, imperial))

        if selected_type.get()=="Imperial to Metric":
            return imperial_dict[text]
        else:
            return metric_dict[text]

        
    for widget in tb_frame.winfo_children():
        widget.destroy()

    user_textbox = Text(tb_frame, width=30, height=12)
    user_textbox.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

    result_textbox = Text(tb_frame, width=30, height=12)
    result_textbox.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
    result_textbox.config(state="disabled")

    if user_unit.startswith("fluid"):
        text = "Fluid Ounces"
    else:
        text = user_unit.split()[0]
        text = text.capitalize()

    starting_unit = Label(tb_frame, text=text, font=("Calibri",12))
    starting_unit.grid(row=0, column=0)
    converted_unit = Label(tb_frame, text=generate_conversion_label(), font=("Calibri",12))
    converted_unit.grid(row=0, column=1)

    label = Label(tb_frame, text="Enter value")
    label.grid(row=2, column=0, pady=5)
    label2 = Label(tb_frame, text="Result")
    label2.grid(row=2, column=1, pady=5)

    convertButton = tk.Button(tb_frame, text="Convert", command=convert)
    convertButton.grid(row=3, column=0, columnspan=2, pady=5)

    tb_frame.grid_columnconfigure(0, weight=1)
    tb_frame.grid_columnconfigure(1, weight=1)
    tb_frame.grid_rowconfigure(0, weight=1)

    tb_frame.pack(side=tk.LEFT, padx=20, pady=10, expand=TRUE)

if __name__ == "__main__":
    interface = Tk()
    interface.geometry("800x600")
    interface.title("Unit Conversion")
    style = ttk.Style()

    rb_frame1 = Frame(interface, pady=30)
    rb_frame2= Frame(interface)
    lb_frame = Frame(interface)
    tb_frame = Frame(interface)

    unit_type()

    interface.mainloop()
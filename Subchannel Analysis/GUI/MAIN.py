from tkinter import messagebox
from analysis import subchannel_analysis
import os, warnings
import customtkinter as ctk
import tkinter as tk
from CTkTable import CTkTable
from PIL import Image
import pandas as pd
import sys

warnings.simplefilter(action='ignore', category=FutureWarning)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main():
    # Define the DIRECtory
    DIREC = os.path.dirname(os.path.abspath(__file__))
    filepath = ['']

    def on_close():
        if messagebox.askyesno("Confirmation", "Are you sure you want to close the application?", parent=root):
            root.quit()
            root.destroy()

    # Creating the main tkinter window
    root = tk.Tk()
    root.iconbitmap(resource_path(DIREC + r"\images\favicon.ico"))
    root.title("Single Phase Subchannel Analysis")
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.geometry("+0+0")
    root.resizable(0, 0)
    
    # DATA
    scaling = 0.8
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    screen_width = int(w*scaling)
    screen_height = int(h*scaling)
    
    light_col = "#2c2c2c"
    dark_col = "#202020"
    button_fg = "#005c4b"
    button_hover = "#1daa61"
    font_type = "Inter"
    width_size = screen_width
    height_size = (screen_height/14)
    padding = 10
    root.configure(bg=light_col)

    # Function to upload Excel file
    def upload_excel():
        filepath[0] = tk.filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        ########## DEBUG
        #filepath[0] = r"E:\COde work\Things\Subchannel-Analysis\Codes\Subchannel Analysis\GUI\gooddata.xlsx"
        
        if filepath[0]:
            status.configure(text=f"  Status: Uploaded File -> {os.path.basename(filepath[0])}")
            data = pd.read_excel(filepath[0])
            data.fillna("", inplace=True)
            data = [list(headings.keys())] + data.values.tolist()
            nonlocal table
            table.destroy()
            table = CTkTable(table_frame, values=data, width=(width_size-5*padding)/9, wraplength=(width_size-9*padding)/9, font=("Arial Bold", table_body_font), justify="left", anchor="w", colors=["#454545", "#515151"], header_color=dark_col, hover_color=light_col)
            table.grid(row=0, column=0, padx=padding, pady=padding)
            table.edit_column(0, font=("Arial Bold", table_body_font), anchor="w")
            table.edit_row(0, font=(font_type, table_head_font, "bold"), anchor="c")

    # Function to check the validity of the uploaded data
    def data_checker():
        data = pd.read_excel(filepath[0])
        data.fillna("", inplace=True)
        titles = list(headings.keys())[1:]
        try:
            values = [float(i) for i in data[titles[0]].tolist()[:18]]
        except:
            status.configure(text=f"  Status: Constant Values entered are not numbers!")
            return 0
        nchanl = int(values[7])
        values[7] = nchanl
        nk = int(values[8])
        values[8] = nk
        nnode = int(values[9])
        values[9] = nnode
        hf = [values[-2] for _ in range(nchanl)]
        h0 = [values[-1] for _ in range(nchanl)]
        try:
            gap = [float(i) for i in data[titles[1]].tolist()[:nk]]
        except:
            status.configure(text=f"  Status: Gap Values entered are not numbers/insufficient!")
            return 0
        try:
            hdia = [float(i) for i in data[titles[2]].tolist()[:nchanl]]
        except:
            status.configure(text=f"  Status: Hydraulic Diameter Values entered are not numbers/insufficient!")
            return 0
        try:
            hperi = [float(i) for i in data[titles[3]].tolist()[:nchanl]]
        except:
            status.configure(text=f"  Status: Heated Perimeter Values entered are not numbers/insufficient!")
            return 0
        try:
            ic = [int(i) for i in data[titles[4]].tolist()[:nk]]
        except:
            status.configure(text=f"  Status: Interconnection (IC) Values entered are not numbers/insufficient!")
            return 0
        try:
            jc = [int(i) for i in data[titles[5]].tolist()[:nk]]
        except:
            status.configure(text=f"  Status: Interconnecton (JC) Values entered are not numbers/insufficient!")
            return 0
        try:
            a = [float(i) for i in data[titles[6]].tolist()[:nchanl]]
        except:
            status.configure(text=f"  Status: Area Values entered are not numbers/insufficient!")
            return 0
        try:
            f0 = [float(i) for i in data[titles[7]].tolist()[:nchanl]]
        except:
            status.configure(text=f"  Status: Inlet MassFlow Rate Values entered are not numbers/insufficient!")
            return 0        
        return [values[:16], gap, hdia, hperi, ic, jc, a, f0, hf, h0]

    # Function to process data
    def process_data():
        if filepath == ['']:
            status.configure(text=f"  Status: No File Uploaded!")
        else:
            valid = data_checker()
            if valid != 0:
                status.configure(text=f"  Status: Processing... Please Wait...")
                
                # Analysis function call (MAIN CALL)
                subchannel_analysis(valid, root, status)

            else:
                pass

    # Function to download template Excel file
    def download_template():
        lenizer = max(len(i) for i in headings.values())
        template_data = {}
        for i in headings:
            if i == "Constants:":
                template_data[i] = constants + [" "] * (lenizer - len(constants))
            else:
                template_data[i] = [" "] * lenizer
        template_df = pd.DataFrame(template_data)
        template_path = os.path.join(DIREC, 'template.xlsx')
        template_df.to_excel(template_path, index=False)
        status.configure(text=f"  Status: Template saved as 'template.xlsx'.")


    # Creating the main frame
    top_frame = ctk.CTkFrame(root, fg_color=dark_col, bg_color=dark_col, corner_radius=0)
    top_frame.grid(row=0, column=0)
    bottom_frame = ctk.CTkFrame(root, fg_color=light_col, bg_color=light_col, corner_radius=0)
    bottom_frame.grid(row=1, column=0)

    # HEADING label
    heading_image = Image.open(resource_path(DIREC + "\\Images\\college.png"))
    tup_siz = ((109/90)*height_size*2-padding*2, height_size*2-padding*2)
    heading_image = ctk.CTkImage(heading_image, size=tup_siz)
    heading_image = ctk.CTkLabel(top_frame, width=(1/10)*width_size - 2*padding, height=height_size*2, image=heading_image, text="", bg_color=dark_col, fg_color=dark_col)
    heading_image.grid(row=0, column=0, padx=padding, pady=padding)
    heading_label = ctk.CTkLabel(top_frame, width=(9/10)*width_size - 2*padding, height=height_size*2, text="Single Phase Subchannel Analysis", font=(font_type, height_size, "bold"), bg_color=dark_col, fg_color=dark_col, anchor="w")
    heading_label.grid(row=0, column=1, padx=padding, pady=padding)
    

    button_font_size = height_size/2
    # BUTTONS
    upload_image = Image.open(resource_path(DIREC + "\\Images\\upload.png"))
    upload_image = ctk.CTkImage(upload_image, size=(button_font_size,button_font_size))
    upload_button = ctk.CTkButton(bottom_frame, width=width_size/3 - 2*padding, height=height_size, image=upload_image, text="Upload Excel File", command=upload_excel, font=(font_type, button_font_size, "bold"), hover_color=button_hover, bg_color=light_col, fg_color=button_fg, anchor="w")
    upload_button.grid(row=0, column=0, padx=padding, pady=padding)

    process_image = Image.open(resource_path(DIREC + "\\Images\\process.png"))
    process_image = ctk.CTkImage(process_image, size=(button_font_size,button_font_size))
    process_button = ctk.CTkButton(bottom_frame, width=width_size/3 - 2*padding, height=height_size, image=process_image, text="Process Data", command=process_data, font=(font_type, button_font_size, "bold"), hover_color=button_hover, bg_color=light_col, fg_color=button_fg, anchor="w")
    process_button.grid(row=0, column=1, padx=padding, pady=padding)

    download_image = Image.open(resource_path(DIREC + "\\Images\\download.png"))
    download_image = ctk.CTkImage(download_image, size=(button_font_size,button_font_size))
    download_button = ctk.CTkButton(bottom_frame, width=width_size/3 - 2*padding, height=height_size, image=download_image, text="Download Template Excel", command=download_template, font=(font_type, button_font_size, "bold"), hover_color=button_hover, bg_color=light_col, fg_color=button_fg, anchor="w")
    download_button.grid(row=0, column=2, padx=padding, pady=padding)

    constants = [
            "Angle (at which rods are inclined)",
            "Axial Length (of Fuel Rod)        ",
            "Correction Factor                 ",
            "Momentum Correction Factor        ",
            "Turbulent Factor                  ",
            "Correction Factor (gamma)         ",
            "Acceleration due to Gravity (g)   ",
            "No. of Subchannels                ",
            "No. of Connections                ",
            "No. of Nodes                      ",
            "Diameter of Fuel Rod              ",
            "Density (at given system pressure)",
            "Slip                              ",
            "Implicit Factor                   ",
            "Viscosity                         ", 
            "Pressure Input                    ",
            "Heat Flux                         ",
            "Inlet Enthalpy (KJ/Kg)            ",
            " "                                                             
    ]

    values, gap, hdia, hperi, ic, jc, a, f0 = [], [], [], [], [], [], [], []

    headings = {"Constants:": constants, "Values:": values, "Gap between\nAdjacent\nSubchannels:": gap, "Hydraulic\nDiameter:": hdia, 
                "Heated\nPerimeter:": hperi, "Intercon.\n(IC):": ic, "Intercon.\n(JC):": jc, "Areas:": a, "Initial\nMassflow\nRate:": f0}

    table_data = [list(headings.keys())]

    for i in constants:
        table_data.append([i])

    table_head_font = height_size/2.7
    table_body_font = height_size/3.2
    # TABLE For Excel
    table_frame = ctk.CTkScrollableFrame(root, width=width_size - 1.6*padding, height=height_size*10, fg_color=light_col, bg_color=light_col, corner_radius=0)
    table_frame.grid(row=2, column=0)
    table = CTkTable(table_frame, values=table_data, width=(width_size-5*padding)/9, wraplength=(width_size-9*padding)/9, font=("Arial Bold", table_body_font), justify="left", anchor="w", colors=["#454545", "#515151"], header_color=dark_col, hover_color=light_col)
    table.grid(row=0, column=0, padx=padding, pady=padding)
    table.edit_column(0, font=("Arial Bold", table_body_font), anchor="w")
    table.edit_row(0, font=(font_type, table_head_font, "bold"), anchor="c")

    # STATUS Label
    status = ctk.CTkLabel(root, width=width_size, height=height_size - 2*padding, text="  Status:", font=(font_type, (height_size - 2*padding)/1.5, "bold"), bg_color=light_col, anchor="w")
    status.grid(row=3, column=0, sticky="w")

    root.mainloop()

main()
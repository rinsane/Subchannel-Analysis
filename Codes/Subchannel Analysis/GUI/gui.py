import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from PIL import Image
import os
import pandas as pd
from CTkTable import CTkTable

def main():
    # Define the directory
    direc = os.path.dirname(os.path.abspath(__file__))
    filepath = ['']

    # Creating the main tkinter window
    root = tk.Tk()
    root.title("Single Phase Subchannel Analysis")
    width = 1080
    height = 720
    root.geometry(f"{width}x{height}+0+0")
    #root.resizable(0, 0)

    # Function to upload Excel file
    def upload_excel():
        filepath[0] = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        if filepath[0]:
            status.configure(text=f"  Status: Uploaded File -> {os.path.basename(filepath[0])}")
            data = pd.read_excel(filepath[0])
            data = [list(headings.keys())] + data.values.tolist()
            nonlocal table
            table = CTkTable(table_frame, values=data, wraplength=890/6, font=(font_type, 15), justify="left", colors=["#454545", "#515151"], header_color=dark_col, hover_color=light_col, width=890/6)
            table.grid(row=0, column=0, padx=10)
            table.edit_row(0, font=(font_type, 14, "bold"))
            table.edit_column(5, width=(900/6)//2)
            table.edit_column(6, width=(900/6)//2)

    # Function to process data
    def process_data():
        if filepath == ['']:
            status.configure(text=f"  Status: No File Uploaded!")
        else:
            status.configure(text=f"  Status: Processing... Please Wait...")
            data = pd.read_excel(filepath[0])
            data = [list(headings.keys())] + data.values.tolist()

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
        template_path = os.path.join(direc, 'template.xlsx')
        template_df.to_excel(template_path, index=False)
        status.configure(text=f"  Status: Template saved as 'template.xlsx'.")

    # DATA
    light_col = "#2c2c2c"
    dark_col = "#202020"
    button_fg = "#005c4b"
    button_hover = "#1daa61"
    font_size = 23
    font_type = "Inter"
    width_size = 1020/3
    height_size = 40

    # Creating the main frame
    top_frame = ctk.CTkFrame(root, width=1080, fg_color=dark_col, corner_radius=0)
    top_frame.grid(row=0, column=0)
    bottom_frame = ctk.CTkFrame(root, width=1080, fg_color=light_col, corner_radius=0)
    bottom_frame.grid(row=1, column=0)

    # HEADING label
    heading_image = Image.open(direc + "/Images/college.png")
    heading_image = ctk.CTkImage(heading_image, size=(109,90))
    heading_image = ctk.CTkLabel(top_frame, image=heading_image, text="")
    heading_image.grid(row=0, column=0, padx=30, pady=25)
    heading_label = ctk.CTkLabel(top_frame, text="Single Phase Subchannel Analysis", font=(font_type, 53, "bold"), bg_color=dark_col, width=1080-(109+60), anchor="w")
    heading_label.grid(row=0, column=1, pady=25)
    
    # BUTTONS
    upload_image = Image.open(direc + "/Images/upload.png")
    upload_image = ctk.CTkImage(upload_image, size=(font_size,font_size))
    upload_button = ctk.CTkButton(bottom_frame, image=upload_image, text="Upload Excel File", command=upload_excel, font=(font_type, font_size, "bold"), hover_color=button_hover, bg_color=light_col, fg_color=button_fg, width=width_size, height=height_size, anchor="w")
    upload_button.grid(row=0, column=0, padx=10, pady=10)

    process_image = Image.open(direc + "/Images/process.png")
    process_image = ctk.CTkImage(process_image, size=(font_size,font_size))
    process_button = ctk.CTkButton(bottom_frame, image=process_image, text="Process Data", command=process_data, font=(font_type, font_size, "bold"), hover_color=button_hover, bg_color=light_col, fg_color=button_fg, width=width_size, height=height_size, anchor="w")
    process_button.grid(row=0, column=1, padx=10, pady=10)

    download_image = Image.open(direc + "/Images/download.png")
    download_image = ctk.CTkImage(download_image, size=(font_size,font_size))
    download_button = ctk.CTkButton(bottom_frame, image=download_image, text="Download Template Excel", command=download_template, font=(font_type, font_size, "bold"), hover_color=button_hover, bg_color=light_col, fg_color=button_fg, width=width_size, height=height_size, anchor="w")
    download_button.grid(row=0, column=2, padx=10, pady=10)

    constants = [
        "ALPHA ",  
        "AXLN  ",  
        "DELTA ",  
        "FACK  ",  
        "FT    ",  
        "GAMA  ",  
        "GC    ",  
        "NCHANL",  
        "NK    ",  
        "NNODE ",  
        "RDIA  ",  
        "RHO   ",  
        "SLP   ",  
        "THETA ",  
        "VISC  ",  
        "DELX  ",
        "PIN   " 
    ]

    values, gap, hdia, hperi, ic, jc, areas = [], [], [], [], [], [], []

    headings = {"Constants:": constants, "Values:": values, "GAP:": gap, "Hydraulic Diameter:": hdia, "Heated Perimeter:": hperi, "IC:": ic, "JC:": jc, "Areas:": areas}

    table_data = [list(headings.keys())]

    for i in constants:
        table_data.append([i])

    
    # TABLE For Excel
    table_frame = ctk.CTkScrollableFrame(root, width=1064, height=479.5, fg_color=light_col, corner_radius=0)
    table_frame.grid(row=2, column=0)
    table = CTkTable(table_frame, values=table_data, wraplength=890/6, font=(font_type, 15), justify="left", colors=["#454545", "#515151"], header_color=dark_col, hover_color=light_col, width=890/6)
    table.grid(row=0, column=0, padx=10)
    table.edit_row(0, font=(font_type, 14, "bold"))
    table.edit_column(5, width=(900/6)//2)
    table.edit_column(6, width=(900/6)//2)

    # STATUS Label
    status = ctk.CTkLabel(root, text="  Status:", font=(font_type, font_size, "bold"), bg_color=light_col, anchor="w", height=45, width=1080)
    status.grid(row=3, column=0, sticky="w")

    root.mainloop()

if __name__ == "__main__":
    main()

import os
import csv
import sys
import tkinter as tk
from tkinter import messagebox
from analysis import calculate
from functions import sub_routines
import matplotlib.pyplot as plt
from curves import worker

def main():

    # DRIVER CODE FOR GUI
    NODE = [sub_routines()]

    # Labels and Entry widgets for each parameter
    parameters = {
        "ALPHA" : NODE[0].ALPHA,    # 0
        "AXLN"  : NODE[0].AXLN, 
        "DELTA" : NODE[0].DELTA, 
        "FACK"  : NODE[0].FACK, 
        "FT"    : NODE[0].FT, 
        "GAMA"  : NODE[0].GAMA, 
        "GC"    : NODE[0].GC, 
        "NCHANL": NODE[0].NCHANL, 
        "NK"    : NODE[0].NK, 
        "NNODE" : NODE[0].NNODE,
        "RDIA"  : NODE[0].RDIA, 
        "RHO"   : NODE[0].RHO, 
        "SLP"   : NODE[0].SLP, 
        "THETA" : NODE[0].THETA, 
        "VISC"  : NODE[0].VISC, 
        "PIN"   : NODE[0].PIN,      # 15

        "GAP"   : NODE[0].GAP,      # 16
        "HDIA"  : NODE[0].HDIA, 
        "HF"    : NODE[0].HF, 
        "HPERI" : NODE[0].HPERI, 
        "IC"    : NODE[0].IC, 
        "JC"    : NODE[0].JC, 
        "A"     : NODE[0].A         # 22
    }

    def data_storer(NODE):

        err_label.config(text="Computing...", fg="black")

        ret_val = calculate(NODE)
        NODE, Axial_length, Enthalpy, MassFlowRate, Pressure, Crossflow = ret_val  
        if ret_val[1:] == (0, 0, 0, 0, 0):
            err_label.config(text=NODE, fg="red")

        else:
            err_label.config(text="Computation Finished Successfully!", fg="green")
            # DATA TABULATION
            Headings = ["Sub-Channel", "Inlet Mass Flow Rate [F0]", "Inlet Enthalpy [H0]",
                "Outlet Mass Flow Rate [F1 at last Node]",
                "Outlet Enthalpy [H1 at last Node]",
                "Heat Generated [C1 at last Node]", "H0 + C1"]
            SCs = [i + 1 for i in range(NODE[0].NCHANL)]
            F0 = NODE[0].F0
            H0 = NODE[0].H0
            F1 = NODE[NODE[0].NCHANL - 1].F1
            H1 = NODE[NODE[0].NCHANL - 1].H1
            C1 = NODE[NODE[0].NCHANL - 1].C1
            H0_C1 = [H0[i] + C1[i] for i in range(NODE[0].NCHANL)]
            LAST_ROW = ["", sum(F0), "", sum(F1), sum(H1), sum(C1), sum(H0_C1)]

            datas = zip(SCs, F0, H0, F1, H1, C1, H0_C1)
            direc = os.path.dirname(os.path.abspath(__file__))
            
            with open(direc+r"\results.csv", "w", newline='') as datasheet:
                writer = csv.writer(datasheet)
                writer.writerow(Headings)
                writer.writerows(datas)

                writer.writerow(LAST_ROW)

            # PLOT CREATION
            worker(NODE, Axial_length, Enthalpy, MassFlowRate, Pressure, Crossflow)
            return

    def get_values():

        nodes = int(data_values["NNODE"].get())
        NODE = [sub_routines() for _ in range(nodes)]

        for indx in range(nodes):
            NODE[indx].ALPHA    = float(data_values["ALPHA"].get())
            NODE[indx].AXLN     = float(data_values["AXLN"].get())
            NODE[indx].DELTA    = float(data_values["DELTA"].get())
            NODE[indx].FACK     = float(data_values["FACK"].get())
            NODE[indx].FT       = float(data_values["FT"].get())
            NODE[indx].GAMA     = float(data_values["GAMA"].get())
            NODE[indx].GC       = float(data_values["GC"].get())
            NODE[indx].NCHANL   = int(data_values["NCHANL"].get())
            NODE[indx].NK       = int(data_values["NK"].get())
            NODE[indx].NNODE    = int(data_values["NNODE"].get())
            NODE[indx].RDIA     = float(data_values["RDIA"].get())
            NODE[indx].RHO      = float(data_values["RHO"].get())
            NODE[indx].SLP      = float(data_values["SLP"].get())
            NODE[indx].THETA    = float(data_values["THETA"].get())
            NODE[indx].VISC     = float(data_values["VISC"].get())
            NODE[indx].PIN      = int(data_values["PIN"].get())

            NODE[indx].DELX     = NODE[indx].AXLN/(NODE[indx].NNODE-1)
            
            NODE[indx].GAP      = [float(item) for item in data_values["GAP"].get("1.0", tk.END).strip().split("\n") if item]
            NODE[indx].HDIA     = [float(item) for item in data_values["HDIA"].get("1.0", tk.END).strip().split("\n") if item]
            NODE[indx].HF       = [float(item) for item in data_values["HF"].get("1.0", tk.END).strip().split("\n") if item]
            NODE[indx].HPERI    = [float(item) for item in data_values["HPERI"].get("1.0", tk.END).strip().split("\n") if item]
            NODE[indx].IC       = [int(item) for item in data_values["IC"].get("1.0", tk.END).strip().split("\n") if item]
            NODE[indx].JC       = [int(item) for item in data_values["JC"].get("1.0", tk.END).strip().split("\n") if item]
            NODE[indx].A        = [float(item) for item in data_values["A"].get("1.0", tk.END).strip().split("\n") if item]

            NODE[indx].initializer()
        
        data_storer(NODE)

    def on_close():
        if messagebox.askyesno("Confirmation", "Are you sure you want to close the application?", parent=root):
            root.quit()
            root.destroy()
    # Create the main window
    root = tk.Tk()
    root.title("Input Values")
    root.resizable(False, False)
    root.geometry(f"+0+0")
    root.protocol("WM_DELETE_WINDOW", on_close)
    bgcolor1 = 'skyblue'
    bgcolor2 = 'light yellow'
    root.configure(bg=bgcolor1)

    heading = tk.Label(root, text="SUBCHANNEL ANALYSIS", font=("Courier New", 30, "bold"), bg=bgcolor1)
    heading.grid(column=0, row=0, columnspan=9)

    data_values = {}

    # Creation of all the NON-LIST parameters
    idx = 1
    for param1 in list(parameters.keys())[:16]:
        label = tk.Label(root, text=param1.ljust(7) + ':', anchor='w', width=8, font=("Courier New", 15, "bold"), bg=bgcolor1)
        label.grid(column=0, row=idx)
        entry = tk.Entry(root, width=10, font=("Courier New", 15), bg=bgcolor2)
        entry.insert(0, parameters[param1])
        entry.grid(column=1, row=idx, padx=2, pady=2)
        data_values[param1] = entry
        idx += 1

    # Creation of all LIST parameters
    idx = 2
    for param2 in list(parameters.keys())[16:]:
        label = tk.Label(root, text=param2.ljust(9) + ':', anchor='w', width=10, font=("Courier New", 15, "bold"), bg=bgcolor1)
        label.grid(column=idx, row=1)
        textbox = tk.Text(root, width=12, font=("Courier New", 15), bg=bgcolor2)
        textbox.grid(column=idx, row=2, padx=2, pady=2, rowspan=15)
        data_values[param2] = textbox
        textbox.insert(tk.END, "\n".join(map(str, parameters[param2])))
        idx += 1

    # Button to get the values
    submit_button = tk.Button(root, text="Submit", command=get_values, width=50, font=("Courier New", 20, "bold"), bg='light green')
    submit_button.grid(column=0, row=17, padx=5, pady=5, columnspan=6)

    err_label = tk.Label(root, text="STATUS", font=("Arial", 15, "bold"), bg=bgcolor1)
    err_label.grid(column=6, row=17, columnspan=3)

    # Run the main event loop
    root.mainloop()
    sys.exit("BYE! BYE!")

if __name__ == "__main__":
    main()
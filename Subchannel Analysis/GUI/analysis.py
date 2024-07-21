from routines import sub_routines
from plotting_gui import plotting
import csv, os, copy
import customtkinter as ctk
import tkinter as tk
from tabulate import tabulate
import pandas as pd
import shutil
import sys

DIREC = os.path.dirname(os.path.abspath(__file__))

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def subchannel_analysis(values, root, status):

    # DATA
    scaling = 0.8
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    screen_width = int(w*scaling)
    screen_height = int(h*scaling)
    
    light_col = "#2c2c2c"
    button_hover = "#1daa61"
    font_type = "Inter"
    width_size = screen_width
    height_size = (screen_height/14)

    # Function for Progress Bar
    nnode = values[0][9]
    processing = tk.Toplevel(root)
    # processing.iconbitmap(resource_path(DIREC + "/images/favicon.ico"))
    processing.focus_set()
    processing.title("Computing...")
    processing.geometry(f"+{screen_width//3}+{screen_height//4}")
    processing.configure(bg=light_col)

    progressBar = ctk.CTkProgressBar(processing, border_color="white", border_width=1, progress_color=button_hover, width=width_size/3, height=height_size/2, orientation="horizontal", determinate_speed=50/(nnode+1))
    progressBar.grid(row=0, column=0, pady=height_size/2, padx=width_size/40)
    progressBar.set(0)
    progressLabel = ctk.CTkLabel(processing, width=width_size/3, height=height_size/4, text="", font=(font_type, height_size/3.5, "bold"), anchor="w")
    progressLabel.grid(row=1, column=0, padx=width_size/40, sticky="w")
    buffer = ctk.CTkLabel(processing, height=height_size/2, text="")
    buffer.grid(row=2, column=0)

    NODE = [sub_routines() for _ in range(2)]

    NODE[0].ALPHA, NODE[0].AXLN, NODE[0].DELTA, NODE[0].FACK, NODE[0].FT, NODE[0].GAMA, NODE[0].GC, NODE[0].NCHANL, NODE[0].NK, NODE[0].NNODE, NODE[0].RDIA, NODE[0].RHO, NODE[0].SLP, NODE[0].THETA, NODE[0].VISC, NODE[0].PIN = values[0]
    NODE[0].GAP, NODE[0].HDIA, NODE[0].HPERI, NODE[0].IC, NODE[0].JC, NODE[0].A, NODE[0].F0, NODE[0].HF, NODE[0].H0 = values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8], values[9]
    NODE[0].init()

    NODE_initial = NODE[0]

    NODE[1] = copy.deepcopy(NODE[0])

    Axial_length = [NODE[0].DELX*i for i in range(NODE[0].NNODE)]
    Enthalpy = [[] for _ in range(NODE[0].NCHANL)]      # H1
    MassFlowRate = [[] for _ in range(NODE[0].NCHANL)]  # F1
    Pressure = [[] for _ in range(NODE[0].NCHANL)]      # P1
    Crossflow = [[] for _ in range(NODE[0].NK)]
    
    direc2 = DIREC + f"/Computation Results/RESULTS_{NODE[0].NCHANL}_Channels_{NODE[0].NNODE}_Nodes/Subchannel Data"
    if os.path.exists(DIREC + f"/Computation Results/RESULTS_{NODE[0].NCHANL}_Channels_{NODE[0].NNODE}_Nodes"):
        progressLabel.configure(text=f"Deleting old data for same config.")
        shutil.rmtree(DIREC + f"/Computation Results/RESULTS_{NODE[0].NCHANL}_Channels_{NODE[0].NNODE}_Nodes")
    if not os.path.exists(direc2):
        os.makedirs(direc2)
    
    def update_progress(progressbar, i):
        if i < NODE[0].NNODE:
            progressBar.step()

            # Start

            # For setting the boundary condition -- no error
            if i == 0:
                for I in range(NODE[1].NCHANL):
                    NODE[1].F1[I] = NODE[1].F0[I]
                    NODE[1].P0[I] = NODE[1].PIN
                #print("FOR NODE ZERO (init)\n")

                for K in range(NODE[1].NK):
                    NODE[1].WIJ0[K] = NODE[1].WIJIN
                    NODE[1].WIJ1[K] = NODE[1].WIJIN
            else:
                #print(f"FOR NODE {i}\n")
                NODE[1].P0 = NODE[0].P1.copy()

                NODE[1].F0 = NODE[0].F1.copy()
                NODE[1].F1 = NODE[1].F0.copy()

                NODE[1].WIJ0 = NODE[0].WIJ1.copy()
                NODE[1].WIJ1 = NODE[1].WIJ0.copy()

                NODE[1].H0 = NODE[0].H1.copy()

            '''/////////////////////////////////////////////////'''
            # CALLING SUBROUTINES 
            progressLabel.configure(text=f"Node: {i + 1} -> executing subroutine SKI") 
            NODE[1].SKI()
            progressLabel.configure(text=f"Node: {i + 1} -> executing subroutine XD") 
            NODE[1].XD()
            progressLabel.configure(text=f"Node: {i + 1} -> executing subroutine XB") 
            NODE[1].XB()
            progressLabel.configure(text=f"Node: {i + 1} -> executing subroutine GAUSS") 
            NODE[1].gauss()
            progressLabel.configure(text=f"Node: {i + 1} -> executing subroutine DCROSS") 
            NODE[1].DCROSS()

            # Reversing the flow
            for K in range(NODE[1].NK):
                NODE[1].WIJ1[K] = - NODE[1].WIJ1[K]
            
            NODE[1].MASFLO()
            
            # copying the F1 in F11
            for I in range(NODE[1].NCHANL):
                NODE[1].F11[I] = NODE[1].F1[I]
            
            '''
            P1, WIJ1, F1, -- calculated from above functions respectively
            now introducing checks if P1, F1, is positive or not
            '''
            progressLabel.configure(text=f"Node: {i + 1} -> doing checks...") 
            # Check for P1
            for I in range(NODE[1].NCHANL):
                if(NODE[1].P1[I] < 0 ):
                    progressLabel.configure(text=f"Negative pressure in P1 at node {i+1}, check error.txt!")
                    a = tabulate([[NODE[1].P1[I], NODE[1].F1[I]] for I in range(14)], headers=['P1', 'F1'], tablefmt = 'grid')
                    b = tabulate([[NODE[1].WIJ1[I]] for I in range(19)], headers=['WIJ1'], tablefmt = 'grid')
                    with open(DIREC+"/error_log.txt", "w") as f:
                        f.write(f"Negative pressure in P1 at node {i+1}\n\n")
                        f.write(a)
                        f.write("/n/n")
                        f.write(b)
                    return
            # Check for F1
            for I in range(NODE[1].NCHANL):
                if(NODE[1].F1[I] < 0 ):
                    progressLabel.configure(text=f"Negative massflow rate in F1 at node {i+1}, check error.txt!")
                    a = (tabulate([[NODE[1].P1[I], NODE[1].F1[I]] for I in range(14)], headers=['P1', 'F1'], tablefmt = 'grid'))
                    b = (tabulate([[NODE[1].WIJ1[I]] for I in range(19)], headers=['WIJ1'], tablefmt = 'grid'))
                    with open(DIREC+"/error_log.txt", "w") as f:
                        f.write(f"Negative massflow rate in F1 at node {i+1}\n\n")
                        f.write(a)
                        f.write("\n\n")
                        f.write(b)
                    return
            progressLabel.configure(text=f"Node: {i + 1} -> all checks passed!") 
            
            for I in range(NODE[1].NCHANL):
                NODE[1].ERROR[I] = abs((NODE[1].F11[I] - NODE[1].F1[I]) / NODE[1].F1[I])
            
            EMAX = max(NODE[1].ERROR)

            progressLabel.configure(text=f"Node: {i + 1} -> checking for errors") 
            while EMAX > 10E-8:
                NODE[1].AXIMOM()
                for I in range(NODE[1].NCHANL):
                    NODE.P1[I] = (NODE[1].DELTA *NODE[1].P1[I]) + ((1 - NODE[1].DELTA) * NODE[1].P0[I])
                NODE[1].DCROSS()
                for I in range(NODE[1].NCHANL):
                    NODE.WIJ1[I] = (NODE[1].GAMA *NODE[1].WIJ1[I]) + ((1 - NODE[1].GAMA) * NODE[1].WIJ0[I])
                for I in range(NODE[1].NCHANL):
                    NODE[1].F11[I] = NODE[1].F1[I]
                
                NODE[1].MASFLO()

                for I in range(NODE[1].NCHANL):
                    NODE[1].ERROR[I] = abs((NODE[1].F11[I] - NODE[1].F1[I]) / NODE[1].F1[I])
                
                EMAX = max(NODE[1].ERROR)

            progressLabel.configure(text=f"Node: {i + 1} -> executing subroutine HM") 
            NODE[1].HM()

            # DEBUG
            if 0:#i%1 == 0:
                print(f"FOR NODE {i}:\n")
                print(f"Pressure {i}: {NODE[1].P1}\n")
                print(f"Enthalpy {i}: {NODE[1].H1}\n")
                print(f"WIJ{i}      : {NODE[1].WIJ1}\n")
                print(f"MassFlow {i}: {NODE[1].F1}")
                print()
                print()

            for chan in range(NODE[0].NCHANL):
                Enthalpy[chan].append(NODE[1].H1[chan])
                MassFlowRate[chan].append(NODE[1].F1[chan])
                Pressure[chan].append(NODE[1].P1[chan])

            for chan in range(NODE[0].NK):
                Crossflow[chan].append(NODE[1].WIJ1[chan])

            # DATA STORING
            progressLabel.configure(text=f"Node: {i + 1} -> Computing...") 
            if i == 0:
                for channel in range(NODE[1].NCHANL):
                    with open(direc2+f"/Channel {channel + 1}.csv", 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(["Node", "Pressure", "Enthalpy", "Mass Flow Rate", "CrossFlow"])
                        writer.writerow([int(i+1), NODE[1].P1[channel], NODE[1].H1[channel], NODE[1].F1[channel], NODE[1].WIJ1[channel]])

            else:
                for channel in range(NODE[1].NCHANL):
                    with open(direc2+f"/Channel {channel + 1}.csv", 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([int(i+1), NODE[1].P1[channel], NODE[1].H1[channel], NODE[1].F1[channel], NODE[1].WIJ1[channel]])


            ################################## THIS IS WHERE THE COPYING HAPPENS
            NODE[0] = copy.deepcopy(NODE[1])

            if i == NODE[0].NNODE - 1:
                progressLabel.configure(text=f"Computation finished! Please wait...")
            root.after(1, update_progress, progressbar, i + 1)  # Schedule next update after 1ms

        else:
            tabulation()
            processing.destroy()
            status.configure(text=f"  Status: Computation Finished!")
            plotting(f"/Computation Results/RESULTS_{NODE[0].NCHANL}_Channels_{NODE[0].NNODE}_Nodes", Axial_length, Crossflow)
            return

    update_progress(progressBar, 0)

    def tabulation():
        # DATA TABULATION
        Headings = ["Sub-Channel", "Inlet Mass Flow Rate [F0]", "Inlet Enthalpy [H0]",
            "Outlet Mass Flow Rate [F1 at last Node]",
            "Outlet Enthalpy [H1 at last Node]",
            "Heat Generated [C1 at last Node]", "H0 + C1"]
        SCs = [i + 1 for i in range(NODE_initial.NCHANL)]
        F0 = NODE_initial.F0
        H0 = NODE_initial.H0
        F1 = NODE[1].F1
        H1 = NODE[1].H1
        C1 = NODE[1].C1
        H0_C1 = [H0[i] + C1[i] for i in range(NODE_initial.NCHANL)]
        LAST_ROW = ["", sum(F0), "", sum(F1), sum(H1), sum(C1), sum(H0_C1)]

        datas = zip(SCs, F0, H0, F1, H1, C1, H0_C1)
        direc = DIREC + f"/Computation Results/RESULTS_{NODE[0].NCHANL}_Channels_{NODE[0].NNODE}_Nodes"
        if not os.path.exists(direc):
            os.makedirs(direc)
        with open(direc+"/final_results.csv", "w", newline='') as datasheet:
            writer = csv.writer(datasheet)
            writer.writerow(Headings)
            writer.writerows(datas)
            writer.writerow(LAST_ROW)
        
        df = pd.read_csv(direc+"/final_results.csv")
        df.to_excel(direc+"/final_results.xlsx", index=False)
        os.remove(direc+"/final_results.csv")

        return
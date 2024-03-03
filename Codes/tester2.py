import os
import csv
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

def worker(NODE, Axial_length, Enthalpy, MassFlowRate, Pressure, Crossflow):

    # MAIN PLOT PENDING CREATION !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
    def create_plot(option, plot_option):
        fig, ax = plt.subplots()
        fig.set_size_inches(8, 5.5)
        schanl = 0 if option == "" else (int(option.split(' ')[1]) - 1)

        if plot_option == "Pressure":
            # Plot Pressure
            ax.plot(Axial_length, Pressure[schanl], label="Pressure")
            ax.legend()

        elif plot_option == "Enthalpy":
            # Plot Enthalpy
            ax.plot(Axial_length, Enthalpy[schanl], label="Enthalpy")
            ax.legend()

        elif plot_option == "Massflow Rate":
            # Plot MassFlowRate
            ax.plot(Axial_length, MassFlowRate[schanl], label="Massflow Rate")
            ax.legend()

        ax.set_title(option + ' ' + plot_option)
        ax.set_xlabel('Axial Length')
        ax.set_ylabel(plot_option)
        
        # Clear previous plot
        for widget in frame.winfo_children():
            widget.destroy()
        
        # Plot Embedding
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0)

        frame4 = tk.Frame(root)
        frame4.grid(row=1, column=1, sticky='w', padx=7)    
        toolbar1 = NavigationToolbar2Tk(canvas, frame4)
        toolbar1.update()
        toolbar1.grid(row=0, column=0)

    def on_close():
        if messagebox.askyesno("Confirmation", "Are you sure you want to close the Plots?", parent=root):
            root.quit()
            root.destroy()

    root = tk.Tk()
    root.title("Subchannel Analysis Plots")
    root.resizable(False, False)
    root.geometry(f"+0+0")
    root.protocol("WM_DELETE_WINDOW", on_close)
    bgcolor1 = 'skyblue'
    bgcolor2 = 'light yellow'
    root.configure(bg=bgcolor1)

    heading = tk.Label(root, text="PLOTS OBTAINED", font=("Courier New", 20, "bold"), bg=bgcolor1)
    heading.grid(column=0, row=0, columnspan=6)

    # Plot Frame
    frame = tk.Frame(root)
    frame.grid(row=1, column=1, rowspan=14)

    options = [f"SubChannel {i + 1}" for i in range(NODE[0].NCHANL)]

    option_buttons = []
    selected_option = tk.StringVar()
    selected_plot_option = tk.StringVar()

    def show_plot_options(option):
        # Clear previous plot option buttons
        for widget in plot_option_frame.winfo_children():
            widget.destroy()

        # Create new plot option buttons
        if option:
            plot_options = ["Pressure", "Enthalpy", "Massflow Rate"]
            for idx, plot_option in enumerate(plot_options):
                button = tk.Radiobutton(plot_option_frame, text=plot_option, variable=selected_plot_option, value=plot_option, command=lambda opt=option, plt_opt=plot_option: create_plot(opt, plt_opt), bg=bgcolor1)
                button.grid(row=idx + 1, column=0, sticky="w")

    # Plot Options frames
    plot_option_frame = tk.Frame(root)
    plot_option_frame.grid(row=1, column=2, rowspan=14)

    # init
    create_plot("", "")

    # Option radio buttons
    for idx, option in enumerate(options):
        button = tk.Radiobutton(root, text=option, variable=selected_option, value=option, command=lambda option=option: show_plot_options(option), bg=bgcolor1)
        button.grid(row=idx + 1, column=0, sticky="w")
        option_buttons.append(button)

    show_plot_options(options[0])

    pwd = os.getcwd()
    file_path = pwd + r".\results.csv"
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)

    for row1 in range(len(data[0])):
        data[0][row1] = data[0][row1].split('[')[0]

    # EXCEL DATA ###########################################################    
    tree = ttk.Treeview(root)
    tree["columns"] = data[0][1:]
    tree.heading("#0", text=data[0][0])

    for col in data[0][1:]:
        tree.heading(col, text=col)
    tree.grid(row=NODE[0].NCHANL + 1, column=0, columnspan=3, padx=10, pady=20)
    tree.tag_configure("bg", background=bgcolor2)

    for item in data[1:]:
        tree.insert("", "end", text=item[0], values=item[1:])

    tree.column("#0", width=100)
    tree.column(data[0][1], width=120+20)
    tree.column(data[0][2], width=100+20)
    tree.column(data[0][3], width=150+20)
    tree.column(data[0][4], width=120+20)
    tree.column(data[0][5], width=120+20)
    tree.column(data[0][6], width=120+20)

    # Add scrollbar
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    scrollbar.grid(row=NODE[0].NCHANL + 1, column=4, rowspan=NODE[0].NCHANL + 1, sticky='ns')
    tree.config(yscrollcommand=scrollbar.set)

    # Plot Frame for crossflow
    frame2 = tk.Frame(root)
    frame2.grid(row=1, column=5, rowspan=NODE[0].NCHANL*2 + 1)

    fig2, ax2 = plt.subplots()
    fig2.set_size_inches(8, 8.3)

    ax2.set_title(f"Crossflow")
    ax2.set_xlabel("Axial Length")
    ax2.set_ylabel("Crossflow Rate")
    for i in range(NODE[0].NK):
        ax2.plot(Axial_length, Crossflow[i], label=f"Cf {i+1}")
    ax2.legend()

    canvas2 = FigureCanvasTkAgg(fig2, master=frame2)
    canvas2.draw()
    canvas2.get_tk_widget().grid(row=0, column=0, rowspan=14)

    frame3 = tk.Frame(root)
    frame3.grid(row=1, column=5, sticky='w', padx=7)    
    toolbar = NavigationToolbar2Tk(canvas2, frame3)
    toolbar.update()
    toolbar.grid(row=0, column=0)

    root.mainloop()
    return
# Subchannel Analysis

A GUI application for the Subchannel Analysis of annular fuel assembly using the preconditioned Jacobian-free Newton Krylov methods.

## Table of Contents
- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Description
We have developed a GUI using the CustomTkinter Python library to facilitate ease in nuclear fuel rod subchannel analysis.

**Steady and Transient State for Nuclear Rods:** Under the guidance of our senior professor, Prof. Kannan Iyer, we developed codes to analyze the temperature profile of nuclear fuel rods in both steady and transient conditions. We utilized libraries such as Pandas, NumPy, and Matplotlib to enhance the efficiency of computation, storage, and visualization of results.

**Subchannel Analysis:** Subsequently, we created a state-of-the-art Graphical User Interface (GUI) for the subchannel analysis of an annular fuel assembly using CustomTkinter. We designed a user-friendly frontend that seamlessly integrates with the computation algorithm, which was also developed in Python.

## Installation
1. **Clone the repository:**
    ```sh
    git clone https://github.com/rinsane/Subchannel-Analysis.git
    ```
2.    **Setup the Python virtual environment:** To use the Application, run the `init.sh` script on your machine to create a Python Virtual Environment with all the required libraries.

4. **Activate the virtual environment:**
    ```sh
    source venv/bin/activate
    ```

## Usage
To use the GUI:
```sh
cd "Subchannel Analysis/GUI"
Python3 MAIN.py
```
Refer the `USAGE.pdf`.

(For Advanced users: To use the rod analysis (CLI driven), provide it with the data in the inputs file)

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

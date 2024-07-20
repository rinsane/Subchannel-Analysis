# Subchannel Analysis

A GUI application for the Subchannel Analysis of annular fuel assembly using the preconditioned Jacobian-free Newton Krylov methods.

## Table of Contents
- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Description
We have developed a GUI using the CustomTkinter Python library in order to facilitate ease in nuclear fuel rod subchannel analysis.
1. **Steady and Transient State for Nuclear Rod:**
    We developed codes, under the guidance of our senior professor Prof. Kannan Iyer, for analysing the temperature profile of Nuclear Fuel rods for both Stedy and Trasnsient conditions. We used libraries like Pandas, NumPy, Matplotlib, etc. for efficiency in computation, storage and visualisation of results.

2. **Subchannel Analysis:**
    We then proceeded to make a state-of-the-art Graphical User Interface for the Subchannel Analysis of annular fuel assembly using CustomTkinter. We created a user friendly frontend that was seamless integrated with computation algorithm, which was also written in Python.

## Installation
To use the Application, run the `.sh` script on your machine to create a Python Virtual Environment with all the required libraries.

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yaegeristhitesh/RLox
    ```
2. **Navigate to the project directory:**
    ```sh
    cd rlox-basic/
    ```
3. **Build the project:**
    ```sh
    cargo build --release
    ```

## Usage
After building the project, you can run the interpreter with the following command:

```sh
./target/release/rlox_basic yourscript.lox
```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

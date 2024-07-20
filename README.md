# Subchannel Analysis

A GUI application for the Subchannel Analysis of annular fuel assembly using the preconditioned Jacobian-free Newton Krylov methods.

## Table of Contents
- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Language Grammar](#language-grammar)
  - [Syntax](#syntax)
  - [High-Level Characteristics](#high-level-characteristics)
    - [Dynamic Typing](#dynamic-typing)
    - [Automatic Memory Management](#automatic-memory-management)
  - [Data Types](#data-types)
    - [Booleans](#booleans)
    - [Numbers](#numbers)
    - [Strings](#strings)
    - [Nil](#nil)
  - [Expressions](#expressions)
    - [Arithmetic](#arithmetic)
    - [Comparison and Equality](#comparison-and-equality)
    - [Logical Operators](#logical-operators)
    - [Precedence and Grouping](#precedence-and-grouping)
  - [Statements](#statements)
    - [Expression Statements](#expression-statements)
    - [Blocks](#blocks)
  - [Variables](#variables)
    - [Declaration and Assignment](#declaration-and-assignment)
  - [Control Flow](#control-flow)
    - [If Statements](#if-statements)
    - [While Loops](#while-loops)
    - [For Loops](#for-loops)
  - [Functions](#functions)
    - [Function Calls](#function-calls)
    - [Function Definitions](#function-definitions)
    - [Closures](#closures)
  - [Classes](#classes)
    - [Class Declaration](#class-declaration)
    - [Instantiation](#instantiation)
    - [Initialization](#initialization)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

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

## Features
- **Basic arithmetic operations**: Support for addition, subtraction, multiplication, and division.
- **Variable declarations**: Ability to declare and use variables in scripts.
- **Control structures**: Includes if-else statements and while loops for flow control.
- **Functions**: Define and call functions with parameters and return values.
- **Standard library**: A small standard library with useful functions for common tasks.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

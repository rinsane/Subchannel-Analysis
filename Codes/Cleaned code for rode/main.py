import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
from helper import one_for_all

def main():
    obj = one_for_all()
    obj.run()
    obj.prnt()

if __name__ == '__main__':
    main()
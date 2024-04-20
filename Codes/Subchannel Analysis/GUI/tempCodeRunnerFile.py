import os
direc2 = os.path.dirname(os.path.abspath(__file__)) + rf"\RESULTS\SUBCHANNELS"
if not os.path.exists(direc2):
    os.makedirs(direc2)
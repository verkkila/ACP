import os
import sys

def make_training_data():
    lines = []
    outfile = open("training_data.txt", "w")
    if not outfile:
        return False
    for f in os.listdir("logs"):
        if f.startswith("log_"):
            logfile = open("logs/" + f, "r")
        else:
            continue
        for line in logfile:
            #take relevant info
            line_no_header = line.split(" ")[1:5]
            try:
                #check line for every irrelevant line (e.g. errors)
                useless = [float(word) for word in line_no_header]
                for val in useless:
                    if val == 0.0:
                        raise ValueError("Zero value in log")
            except ValueError:
                pass
            else:
                outfile.write(" ".join(line_no_header) + "\n")
        logfile.close()
    outfile.close()
    return True

make_training_data()

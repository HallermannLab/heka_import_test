import heka_reader
import os
import matplotlib.pyplot as plt
import numpy as np


def main():
    IMPORT_FOLDER = "/Users/stefanhallermann/Library/CloudStorage/Dropbox/tmp/Sophie/old/in"
    filename = "Sophie_2025-04-17_002.dat"
    heka_path = os.path.join(IMPORT_FOLDER, filename)
    print("Reading from " + heka_path)
    bundle = heka_reader.Bundle(heka_path)
    trace = bundle.data[0, 4, 0, 1]
    node = bundle.pul[0][4][0][1]
    time = np.linspace(node.XStart, node.XStart + node.XInterval * (len(trace) - 1), len(trace))
    plt.plot(time * 1000, trace)  # time in ms
    plt.xlabel("Time (ms)")
    plt.ylabel(f"{node.Label} ({node.YUnit})")
    plt.show()


if __name__ == '__main__':
    main()

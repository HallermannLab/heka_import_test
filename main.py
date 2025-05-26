import heka_reader
import os
import matplotlib.pyplot as plt


def main():
    IMPORT_FOLDER = "/Users/stefanhallermann/Library/CloudStorage/Dropbox/tmp/Sophie/in"
    filename = "Sophie_2025-04-17_002.dat"
    heka_path = os.path.join(IMPORT_FOLDER, filename)
    print("Reading from " + heka_path)
    bundle = heka_reader.Bundle(heka_path)
    trace = bundle.data[0, 4, 0, 2]
    print(trace)
    plt.plot(trace)
    plt.show()


if __name__ == '__main__':
    main()

import pandas as pd
import matplotlib.pyplot as plt

def import_file(filepath):
    dataframe = pd.read_csv(filepath)
    return dataframe

def draw_plot(dataframe):
    Xs = dataframe[dataframe.columns[0]]
    ys = dataframe["stopped_cars"] / dataframe["cars_number"] * 100
    plt.scatter(Xs, ys, s=1)
    plt.title("Stopped cars percent")
    plt.xlabel("Time [s]")
    plt.ylabel("Stopped cars / active cars [%]")
    plt.show()


if __name__ == "__main__":
    draw_plot(import_file("./records/CROSSING_NO_RIGHT_OF_WAY_SIM-2023_04_06-17_13_25"))
    draw_plot(import_file("./records/CROSSING_NO_RIGHT_OF_WAY_SIM-2023_04_06-17_14_38"))
    draw_plot(import_file("./records/CROSSING_NO_RIGHT_OF_WAY_SIM-2023_04_06-18_08_43"))
    draw_plot(import_file("./records/CROSSING_NO_RIGHT_OF_WAY_SIM-2023_04_06-18_09_35"))
    draw_plot(import_file("./records/CROSSING_NO_RIGHT_OF_WAY_SIM-2023_04_08-22_16_25"))
    draw_plot(import_file("./records/CROSSING_NO_RIGHT_OF_WAY_SIM-2023_04_08-22_23_21"))
import numpy as np
import pandas as pd


def create_data(dataset):
    dataset["GG Temp Avg"] = dataset.loc[:, ["GG Temp 1",
                                             "GG Temp 2",
                                             "GG Temp 3",
                                             "GG Temp 4",
                                             "GG Temp 5",
                                             "GG Temp 6",
                                             "GG Temp 7",
                                             "GG Temp 8"]].mean(axis=1)

    for i in range(1, 9):
        name_1 = "T" + str(i) + " Avg"
        name_2 = "GG Temp " + str(i)

        dataset[name_1] = dataset[name_2] - dataset["GG Temp Avg"]

    return dataset

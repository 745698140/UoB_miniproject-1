import pandas as pd


if __name__ == "main":
    path = "./data/TstB02_2022-01-04tapes.csv"
    tapes = pd.read_csv(path, header=None)
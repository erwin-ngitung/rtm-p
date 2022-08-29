from adtk.data import validate_series
from adtk.detector import ThresholdAD
import pandas as pd
import numpy as np


def anomaly_detection(data):
    data = data.set_index("TimeStamp")
    data.index = pd.to_datetime(data.index)
    data = validate_series(data)
    threshold_ad = ThresholdAD(high=1200, low=500)
    anomalies = threshold_ad.detect(data).values
    index = []

    for i in range(len(anomalies)):
        if bool(anomalies[i]):
            index.append(i)

    return index

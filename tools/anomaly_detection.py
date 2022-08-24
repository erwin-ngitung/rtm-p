from adtk.data import validate_series
from adtk.detector import ThresholdAD
import pandas as pd


def anomaly_detection(data):
    data = validate_series(data)
    threshold_ad = ThresholdAD(high=1200, low=700)
    anomalies = threshold_ad.detect(data)
    value = anomalies.values[-1][0]

    return value

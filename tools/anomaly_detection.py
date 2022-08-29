from adtk.data import validate_series
from adtk.detector import ThresholdAD
from adtk.visualization import plot
import pandas as pd


def anomaly_detection(data):
    data = data.set_index("TimeStamp")
    data.index = pd.to_datetime(data.index)
    data = validate_series(data)
    threshold_ad = ThresholdAD(high=1200, low=500)
    anomalies = threshold_ad.detect(data)

    graph = plot(data, anomaly=anomalies, ts_linewidth=1, ts_markersize=3, anomaly_markersize=5, anomaly_color='red',
                 anomaly_tag="marker")

    return graph


def anomaly_detection_manual(data, column, high, low):
    data_true = data.loc[(data[column] > high) | (data[column] < low)]
    index = data_true.index.values

    return index

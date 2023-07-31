import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder

def cyclical_feature_encoder(time_period):
    period_max = np.max(time_period)
    time_sin = np.sin(2 * np.pi * time_period / period_max)
    time_cos = np.cos(2 * np.pi * time_period / period_max)
    return time_sin, time_cos

def transform_cyclical_features(data: pd.DataFrame, features_names: list):
    new_features = pd.DataFrame(index=data.index)
    for column in features_names:
        feature_sin, feature_cos = cyclical_feature_encoder(data[column])
        new_features[column + '_sin'] = feature_sin
        new_features[column + '_cos'] = feature_cos
    return new_features

def tranform_label_features(data: pd.DataFrame, features_names: list):
    new_features = pd.DataFrame(index=data.index)
    encoder = LabelEncoder()
    for column in features_names:
        new_features[column] = encoder.fit_transform(data[column])
    return new_features
"""
Resistance-Support Indicator
"""
import numpy as np
import pandas as pd

from trade_assistant.signal_processing.base import Indicator
from sklearn.cluster import AgglomerativeClustering


class SupportResistanceIndicator(Indicator):
    rolling_wave_length: int = None
    num_clusters: int = None

    def __init__(self, rolling_wave_length: int, num_clusters: int):
        super().__init__(rolling_wave_length=rolling_wave_length, num_clusters=num_clusters)
        self.list_supports = []
        self.list_resistances = []

    def process(self, input_df: pd.DataFrame):
        """
        Using the close price instead of high and low for max and min waves.
        :param input_df:
        :return:
        """
        # Create min and max waves
        max_waves_temp = input_df.close.rolling(self.rolling_wave_length).max().rename('waves')
        min_waves_temp = input_df.close.rolling(self.rolling_wave_length).min().rename('waves')
        max_waves = pd.concat([max_waves_temp, pd.Series(np.zeros(len(max_waves_temp)) + 1)], axis=1)
        min_waves = pd.concat([min_waves_temp, pd.Series(np.zeros(len(min_waves_temp)) + -1)], axis=1)
        # Remove duplicates
        max_waves.drop_duplicates('waves', inplace=True)
        min_waves.drop_duplicates('waves', inplace=True)
        # Merge max and min waves
        waves = max_waves.append(min_waves).sort_index()
        waves = waves[waves[0] != waves[0].shift()].dropna()
        # Find Support/Resistance with clustering using the rolling stats
        # Create [x,y] array where y is always 1
        x = np.concatenate((waves.waves.values.reshape(-1, 1), (np.zeros(len(waves)) + 1).reshape(-1, 1)), axis=1)
        # Initialize Agglomerative clustering
        cluster = AgglomerativeClustering(n_clusters=self.num_clusters, affinity='manhattan', linkage='complete')
        cluster.fit_predict(x)

        waves['clusters'] = cluster.labels_
        # Get index of the max wave for each cluster
        waves2 = waves.loc[waves.groupby('clusters')['waves'].idxmax()]
        waves2.waves.drop_duplicates(keep='first', inplace=True)

        # From the current close, identify the resistance/ support
        list_waves = waves2.reset_index().waves.values.tolist()
        current_close = input_df.close.iloc[-1]
        highs = sorted([i for i in list_waves if i > current_close])[:3]
        lows = sorted([i for i in list_waves if i < current_close], reverse=True)[:3]

        self.list_resistances.append(highs)
        self.list_supports.append(lows)




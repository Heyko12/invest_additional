from freqtrade.strategy import IStrategy
import pandas as pd
import talib.abstract as ta

class RSI(IStrategy):
    minimal_roi = {"0": 0.02}
    stoploss = -0.02
    trailing_stop = False

    def populate_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)
        return dataframe

    def populate_entry_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        dataframe.loc[(dataframe["rsi"] < 30), "enter_long"] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        dataframe.loc[(dataframe["rsi"] > 50), "exit_long"] = 1
        return dataframe

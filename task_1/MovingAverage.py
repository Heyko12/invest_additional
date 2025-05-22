from freqtrade.strategy import IStrategy
import pandas as pd

class MovingAverage(IStrategy):
    minimal_roi = {"0": 0.05}
    stoploss = -0.1
    trailing_stop = True

    def populate_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        dataframe["sma_fast"] = dataframe["close"].rolling(window=10).mean()
        dataframe["sma_slow"] = dataframe["close"].rolling(window=30).mean()
        return dataframe

    def populate_entry_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        long_cond = (
            (dataframe["sma_fast"] > dataframe["sma_slow"]) &
            (dataframe["sma_fast"].shift(1) <= dataframe["sma_slow"].shift(1))
        )
        dataframe.loc[long_cond, "enter_long"] = 1

        short_cond = (
            (dataframe["sma_fast"] < dataframe["sma_slow"]) &
            (dataframe["sma_fast"].shift(1) >= dataframe["sma_slow"].shift(1))
        )
        dataframe.loc[short_cond, "enter_short"] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        dataframe.loc[dataframe["sma_fast"] < dataframe["sma_slow"], "exit_long"] = 1
        dataframe.loc[dataframe["sma_fast"] > dataframe["sma_slow"], "exit_short"] = 1

        return dataframe
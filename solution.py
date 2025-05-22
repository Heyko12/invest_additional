from freqtrade.strategy import IStrategy
import pandas as pd

class ThreeGreenCandles(IStrategy):
    timeframe = "1h"
    minimal_roi = {"0": 0.1}
    stoploss = -0.10
    trailing_stop = False

    def populate_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        # Заполняем колонку со свечами (НЕ ЗАГЛЯДЫВАЯ В БУДУЩЕЕ!)
        dataframe["green"] = dataframe["close"] > dataframe["open"]
        dataframe["three_green"] = (
            dataframe["green"] &
            dataframe["green"].shift(1) &
            dataframe["green"].shift(2)
        )

        return dataframe

    def populate_entry_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        # Играем на повышение если прошли через три свечи и стоим на третьей
        dataframe.loc[dataframe["three_green"] == 1, "enter_long"] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        # Выходного правила из позиции нет - только stoploss нас остановит
        return dataframe
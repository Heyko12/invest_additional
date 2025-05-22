## Теоретическое обоснование лучшей производительности при большем `timeframe` и код:

### В этой стратегии мы используем MovingAverage из файла MovingAverage.py, строющую усредняющие значения, которые выступают в роли трендовых индикаторов - `sma_fast` - это текущий тренд, посчитанный с окном `window=10`, а `sma_slow` - запаздывающий, посчитанный с окном `window=30`. Когда текущий тренд пробивает запаздывающий, это служит сигналом на вход в long позицию, при противоположном пробитии мы входим в short. Такая стратегия как раз призвана сгладить насколько возможно ценовые флуктуации, отфильтровывая краткосрочный шум, и наиболее эффективна там, где существуют средне- и долгосрочные тренды:

```
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
```

## Запуск стратегии на разных таймфреймах:

### Из корня репозитория переходим в папку task_1:

```
cd task_1
```

### Билдим образ:

```
docker build -t antipova-movingaverage .
```

### Бэктестим стратегию MovingAverage при `timeframe=5m`:

```
$ docker run --rm antipova-movingaverage backtesting --strategy MovingAverage --timeframe 5m --timerange 20220101-20250101
                                                            STRATEGY SUMMARY                                                             
┏━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
┃      Strategy ┃ Trades ┃ Avg Profit % ┃ Tot Profit USDT ┃ Tot Profit % ┃ Avg Duration ┃  Win  Draw  Loss  Win% ┃             Drawdown ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
│ MovingAverage │   6544 │        -0.02 │        -328.911 │       -32.89 │      2:01:00 │ 2084     0  4460  31.8 │ 387.448 USDT  38.74% │
```

### Бэктестим стратегию MovingAverage при `timeframe=4h`:

```
$ docker run --rm antipova-movingaverage backtesting --strategy MovingAverage --timeframe 4h --timerange 20220101-20250101
                                                              STRATEGY SUMMARY                                                              
┏━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃      Strategy ┃ Trades ┃ Avg Profit % ┃ Tot Profit USDT ┃ Tot Profit % ┃     Avg Duration ┃  Win  Draw  Loss  Win% ┃            Drawdown ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ MovingAverage │    129 │         0.40 │         173.468 │        17.35 │ 2 days, 10:12:00 │   58     0    71  45.0 │ 100.067 USDT  9.71% │
└───────────────┴────────┴──────────────┴─────────────────┴──────────────┴──────────────────┴────────────────────────┴─────────────────────┘
```

## Мы видим ожидаемое: MovingAverage более эффективна на бОльших `timeframe`, т.к. при увеличении `timeframe`, можно сказать, происходит дополнительное сглаживание, и входить в лонг и шорт стратегия может с большей уверенностью.
## **Задание 1**

Запустить стратегию можно, вызвав следующую команду:

```sh
docker build -t antipova_strat1 . && docker run --rm antipova_strat1
```

### Примерный вывод:

```
│          Strategy │ Trades │ Avg Profit % │ Tot Profit USDT │ Tot Profit % │     Avg Duration │  Win  Draw  Loss  Win% │             Drawdown │
|-------------------|--------|--------------|-----------------|--------------|------------------|------------------------|----------------------|
│ ThreeGreenCandles │     80 │         1.52 │         429.093 │        42.91 │ 13 days, 5:09:00 │   46     0    34  57.5 │ 254.481 USDT  24.85% │
```
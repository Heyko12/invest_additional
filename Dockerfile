FROM freqtradeorg/freqtrade:stable
VOLUME [ "/freqtrade/user_data" ]

COPY config.json /freqtrade
RUN freqtrade download-data -p BTC/USDT -t 1h --timerange=20220101-20250101
COPY solution.py /freqtrade/user_data/strategies

WORKDIR /freqtrade

ENTRYPOINT [ "freqtrade" ]
CMD [ "backtesting", "--strategy", "ThreeGreenCandles", "--timeframe", "1h", "--timerange", "20220101-20250101" ]
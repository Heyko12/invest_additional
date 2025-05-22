FROM freqtradeorg/freqtrade:stable
RUN freqtrade download-data -p BTC/USDT --exchange bybit -t 4h 5m --timerange=20220101-20250101
COPY config.json /freqtrade/config.json
COPY RSI.py /freqtrade/user_data/strategies
WORKDIR /freqtrade
ENTRYPOINT ["freqtrade"]
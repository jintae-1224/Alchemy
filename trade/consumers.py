import json
from time import sleep
from trade.models import BinanceTradeConditions

from tradingview_ta import TA_Handler, Interval, Exchange
import ccxt
import time
import requests

from channels.generic.websocket import WebsocketConsumer


class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        trade_data = BinanceTradeConditions.objects.all()
        trade_datalist = trade_data.values_list()
        trade_tuple = trade_datalist[0]
        api_key = trade_tuple[1]
        secret_key = trade_tuple[2]
        ticker = trade_tuple[3]
        order_type = trade_tuple[4]
        candle_time = trade_tuple[5]
        used_amount = trade_tuple[6]
        # condition_sentence = +trade_tuple[8] + trade_tuple[9]

        binance = ccxt.binance(
            {
                "options": {"defaultType": "future"},
                "timeout": 30000,
                "apiKey": api_key,
                "secret": secret_key,
                "enableRateLimit": True,
            }
        )

        position = 0

        while True:
            use_ticker = TA_Handler(symbol="BTCPERP", screener="crypto", exchange="BINANCE", interval=candle_time)

            use_ticker_data = use_ticker.get_analysis()
            condition1 = use_ticker_data.indicators[trade_tuple[7]]
            condition3 = use_ticker_data.indicators["close"]
            condition2 = use_ticker_data.indicators[trade_tuple[9]]

            print(condition1)
            print(condition3)

            if trade_tuple[8] == ">":
                trade_condition = str(condition1 > condition2)
            elif trade_tuple[8] == "<":
                trade_condition = str(condition1 > condition2)
            elif trade_tuple[8] == ">=":
                trade_condition = str(condition1 >= condition2)
            elif trade_tuple[8] == "<=":
                trade_condition = str(condition1 <= condition2)
            elif trade_tuple[8] == "=":
                trade_condition = str(condition1 == condition2)
            elif trade_tuple[8] == "!=":
                trade_condition = str(condition1 != condition2)

            if position == 0 and trade_condition:
                order = binance.create_market_buy_order(symbol=ticker, amount=used_amount)
                buy_price = order["price"]
                position = 1

                def post_message(token, channel, text):
                    response = requests.post(
                        "https://slack.com/api/chat.postMessage",
                        headers={"Authorization": "Bearer " + token},
                        data={"channel": channel, "text": text},
                    )
                    print(response)

                myToken = "xoxb-1845751276917-1861484716081-k2ZQ2ZnEwJOYB0H3IR3ga1Cs"

                post_message(myToken, "#chimpanzee", "Position : 매수 , 체결가 :" + str(buy_price))

            buy_ticker = binance.fetch_ticker(ticker)
            buy_ticker_now = buy_ticker["last"]
            Initial_Margin = float(used_amount) * buy_price * 0.04
            PNL = (buy_ticker_now - buy_price) * float(used_amount)
            ROE = str(round((PNL / Initial_Margin) * 100, 2)) + "%"

            count = json.dumps(
                {
                    "ticker": ticker,
                    "position": order_type,
                    "now_price": buy_ticker_now,
                    "buy_price": buy_price,
                    "roe": ROE,
                }
            )
            print(count)
            self.send(count)
            sleep(0.5)

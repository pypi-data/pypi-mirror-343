from stock_prediction.core import StockPredictor
from stock_prediction.utils import optimize_lookback

import schedule
import time
import pandas as pd
from datetime import date, timedelta, datetime
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.linear_model import LinearRegression

import alpaca_trade_api as tradeapi
import yfinance as yf
from pandas_market_calendars import get_calendar

nyse = get_calendar("NYSE")

# api = tradeapi.REST(
#     key_id='PKR0BKC0QMVXGC6WUYZB',
#     secret_key='nIonxysbSHIIC77ojMjiQPgCrug78echi1IcZMe8',
#     base_url='https://paper-api.alpaca.markets/'  # Paper trading endpoint
# )

# API imports
api_key = "PKR0BKC0QMVXGC6WUYZB"
secret_key = "nIonxysbSHIIC77ojMjiQPgCrug78echi1IcZMe8"
paper = True
# DO not change this
trade_api_url = None
trade_api_wss = None
data_api_url = None
stream_data_wss = None

import requests
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import (
    MarketOrderRequest,
    LimitOrderRequest,
    StopLossRequest,
    TakeProfitRequest,
    GetOrdersRequest,
    QueryOrderStatus,
)
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType, OrderClass

trading_client = TradingClient(
    api_key=api_key, secret_key=secret_key, paper=True, url_override=trade_api_url
)


energy_sector = yf.Sector("energy").top_companies.index
technology_sector = yf.Sector("technology").top_companies.index

# Define the trading strategy
generate_trading_signal = StockPredictor.generate_trading_signal
generate_hft_signals = StockPredictor.generate_hft_signals


def market_hours_check(current_date=date.today()):
    """
    Returns the next valid trading day using NYSE calendar.
    """
    # Get NYSE calendar
    nyse = get_calendar("NYSE")

    # Convert input to pandas Timestamp if it isn't already
    current_date = pd.Timestamp(current_date)

    # Get valid trading days for a range (using 10 days to be safe)
    schedule = nyse.schedule(
        start_date=current_date, end_date=current_date + pd.Timedelta(days=10)
    )

    # Check if the current date is in the schedule
    return current_date in schedule.index


################################# Trading Job


def trading_job():
    if not market_hours_check():
        print("Market is closed. Exiting...")
        return
    for symbol in energy_sector[:10]:
        predictor = StockPredictor(
            symbol, start_date="2023-01-01", end_date=date.today()
        )

        try:
            signal = generate_trading_signal(predictor, symbol)
            StockPredictor.execute_trade(symbol, signal, trading_client)
            print(f"Executed {signal} for {symbol}")
        except Exception as e:
            print(f"Trade failed: {str(e)}")


def energy_sector_trading():
    if not market_hours_check():
        print("Market is closed. Exiting...")
        return

    volatile_symbols = [
        "CERO",
        "BOWN",
        "CNEY",
        "JZXN",
        "AREB",
        "AGMH",
        "PET",
        "XELB",
        "OMEX",
        "AREN",
        "JYD",
        "CMLS",
        "SWKH",
        "TMC",
        "AGRI",
        "CTHR",
        "INBK",
        "WLGS",
        "AMBP",
        "FFAI",
        "RLMD",
        "TNMG",
        "UOKA",
        "BUJA",
        "CYH",
        "CDIO",
        "VSME",
        "SGMA",
        "FAMI",
        "ABP",
        "GSHD",
        "BSLK",
        "ASGN",
        "SHYF",
        "LIXT",
        "TLSA",
        "PHIO",
        "SHFS",
        "ENSC",
        "MXL",
        "TOI",
        "RZLV",
        "ABTS",
        "FI",
        "ALBT",
        "ABLV",
        "PRPO",
        "APCX",
        "HOLO",
        "AMTB",
        "SISI",
        "CNSP",
        "SBEV",
        "CHDN",
        "VS",
        "SLXN",
        "XTNT",
        "VCIG",
        "DUO",
        "BLZE",
        "INTS",
        "SXTC",
        "PI",
        "BTOG",
        "GNS",
        "XFOR",
        "SRM",
        "OBLG",
        "ANGH",
        "FARO",
        "BW",
        "EPOW",
        "USAR",
        "BCAB",
        "NTRP",
        "CLGN",
        "PLUR",
        "SMX",
        "MODV",
    ]
    energy_symbols = [
        "COP",
        "TPL",
        "APA",
        "AR",
        "EOG",
        "LLY",
        "CHX",
        "BKR",
        "NOV",
    ]  # Example energy stocks
    technology_symbols = list(technology_sector)[:10]  # list(technology_sector)[10:15] #["GOOGL", 'AXP', "MSFT", "AMZN", "NVDA", 'AXP']#[sym for sym in list(technology_sector)[10:15] if sym not in ["GOOGL", 'AXP', "MSFT", "AMZN", "NVDA", 'AXP'] ]
    # #AAPL", # Example technology stocks

    predictors = []
    open_orders = list(
        set(
            [
                stock.symbol
                for stock in trading_client.get_orders(
                    filter=GetOrdersRequest(status=QueryOrderStatus.OPEN)
                )
            ]
        )
    )

    # Initialize predictors
    for symbol in technology_symbols:
        predictor = StockPredictor(symbol=symbol, start_date="2023-06-01")
        predictor.load_data()
        predictors.append(predictor)

    # Generate signals with correlation check
    signals = []
    hft_signals = []
    for predictor, symbol in zip(predictors, technology_symbols):
        # Check if the symbol is already in open orders
        if symbol in open_orders:
            print(f"Skipping {symbol} as it is already in open orders.")
            continue
        if datetime.now().hour < 16 and datetime.now().hour > 9:
            current_price = (
                yf.download(symbol, start=date.today(), interval="1m")["Close"]
                .iloc[-1]
                .values[0]
            )
        else:
            current_price = (
                yf.download(symbol, start=date.today(), interval="1d")["Close"]
                .iloc[-1]
                .values[0]
            )

        try:
            signal = predictor.generate_trading_signal(
                predictor=predictor, symbol=symbol
            )
        except Exception as e:
            print(f"Signal generation failed for {symbol}: {str(e)}")
            continue
        try:
            hft_signal = predictor.generate_hft_signals(
                symbol=symbol, profit_target=0.0001
            )
        except Exception as e:
            print(f"HFT signal generation failed for {symbol}: {str(e)}")
            continue
        signals.append((predictor.symbol, signal))
        hft_signals.append((predictor.symbol, hft_signal))
    # Execute trades with risk checks
    # for symbol, signal in signals:
    #     predictor = next(p for p in predictors if p.symbol == symbol)
    #     try:
    #         predictor.execute_trade(signal)
    #         print(f"Executed {signal} for {symbol}")

    #     except Exception as e:
    #         print(f"Trade failed for {symbol}: {str(e)}")
    # Execute HFT trades
    for symbol in technology_symbols:
        predictor = next(p for p in predictors if p.symbol == symbol)
        try:

            predictor.execute_hft(symbol=symbol, manual=True)
            print(f"Executed HFT for {symbol}")
        except Exception as e:
            print(f"HFT trade failed for {symbol}: {str(e)}")
    


# Run hourly during market hours
schedule.every(5).minutes.do(energy_sector_trading)
energy_sector_trading()  # Run immediately on script start

# # Run daily at market close
# schedule.every().day.at("16:00").do(trading_job)

while True:
    schedule.run_pending()
    time.sleep(60)

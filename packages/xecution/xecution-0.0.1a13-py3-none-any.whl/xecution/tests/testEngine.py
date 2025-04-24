import asyncio
import sys
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
else:
    sys.path.append("/Users/kaihock/Desktop/All In/Xecution")


import numpy as np
import logging
from datetime import datetime, timezone
from xecution.core.engine import BaseEngine
from xecution.common.enums import Exchange, KlineType, Mode, OrderSide, OrderType, Symbol, TimeInForce
from xecution.models.config import OrderConfig, RuntimeConfig
from xecution.models.topic import KlineTopic
from xecution.utils.logger import Logger

KLINE_FUTURES = KlineTopic(klineType=KlineType.Binance_Futures, symbol=Symbol.BTCUSDT, timeframe="1m")
KLINE_SPOT = KlineTopic(klineType=KlineType.Binance_Spot, symbol=Symbol.BTCUSDT, timeframe="1m")

# Enable logging to see real-time data
class Engine(BaseEngine):
    """Base engine that initializes BinanceService and processes on_candle_closed and on_datasource_update."""
    def __init__(self, config):
        Logger(log_file="abc.log", log_level=logging.INFO)
        super().__init__(config)

    async def on_candle_closed(self, kline_topic: KlineTopic):
        """Handles closed candle data using `self.data_map[kline_topic]`."""
        # await self.get_order_book(Symbol.ETHUSDT)
        # await self.get_position_info(Symbol.BTCUSDT)
        # await self.get_wallet_balance()
        # await self.set_hedge_mode(False)
        abc = await self.place_order(order_config=OrderConfig(
            market_type=KlineType.Binance_Futures,
            symbol=Symbol.BTCUSDT,
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=0.02,
            price = 80000,
            time_in_force=TimeInForce.GTC
        ))
        logging.info(f"{abc}")
        # await self.set_leverage(Symbol.BTCUSDT,100)
        # await self.get_current_price(Symbol.BTCUSDT)
        candles = self.data_map[kline_topic]
        logging.info(f"Candle Incoming: {kline_topic}")
        starttime = np.array(list(map(lambda c: float(c["start_time"]), candles)))       
        candle = np.array(list(map(lambda c: float(c["close"]), candles)))           
        logging.info(f"Last Kline Closed | {kline_topic.symbol}-{kline_topic.timeframe} | Close: {candle[-1]} | Time: {datetime.fromtimestamp(starttime[-1] / 1000)}")

    async def on_order_update(self, order):
        logging.info(f"{order}")

engine = Engine(
    RuntimeConfig(
        mode= Mode.Testnet,
        kline_topic=[
            KLINE_SPOT,
            KLINE_FUTURES
        ],
        datasource_topic=None,
        start_time=datetime(2025,1,1,0,0,0,tzinfo=timezone.utc),
        data_count=1000,
        exchange=Exchange.Binance,
        API_Key="0023f3dd37d75912abffc7a7bb95def2f7a1e924dc99b2a71814ada35b59dd15" ,  # Replace with your API Key if needed
        API_Secret="5022988215bffb0a626844e7b73125533d1776b723a2abe2a8d2f8440da378d9", # Replace with your API Secret if needed
    )
)

asyncio.run(engine.start())

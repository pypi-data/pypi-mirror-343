import asyncio
import logging
from xecution.common.enums import Exchange, KlineType, Mode, Symbol
from xecution.models.active_order import ActiveOrder
from xecution.models.config import OrderConfig, RuntimeConfig
from xecution.models.topic import KlineTopic
from xecution.services.exchange.binance_service import BinanceService
from xecution.services.exchange.bybit_service import BybitService
from xecution.services.exchange.okx_service import OkxService

class BaseEngine:
    """Base engine that initializes BinanceService and processes on_candle_closed and on_datasource_update."""

    def __init__(self, config: RuntimeConfig):
        self.config = config
        self.data_map = {}  # Local data storage for kline data
        self.binance_service = BinanceService(config, self.data_map)  # Pass data_map to BinanceService
        self.bybit_service = BybitService(config, self.data_map)  # Pass data_map to BybitService
        self.okx_service = OkxService(config, self.data_map)  # Pass data_map to OkxService

    async def on_candle_closed(self, kline_topic: KlineTopic):
        """Handles closed candle data"""

    async def on_order_update(self, order):
        """Handles order status"""

    async def on_datasource_update(self, datasource_topic):
        """Handles updates from external data sources."""
    
    async def on_active_order_interval(self,activeOrders: list[ActiveOrder]):
        """Handles open orders data."""

    async def start(self):
        """Starts BinanceService and behaves differently based on the runtime mode."""
        try:
            await self.binance_service.get_klines(self.on_candle_closed)

            if self.config.mode == Mode.Live or self.config.mode == Mode.Testnet:
                await self.binance_service.check_connection()
                await self.listen_order_status()
                asyncio.create_task(self.listen_open_orders_periodically())
                while True:
                    await asyncio.sleep(1)  # Keep the loop alive
            else:
                logging.info("Backtest mode completed. Exiting.")
        except ConnectionError as e:
                logging.error(f"Connection check failed: {e}")
        
    async def place_order(self, order_config: OrderConfig):
        return await self.binance_service.place_order(order_config)
        
    async def get_account_info(self):
        return await self.binance_service.get_account_info()

    async def set_hedge_mode(self, is_hedge_mode: bool):
        return await self.binance_service.set_hedge_mode( is_hedge_mode)

    async def set_leverage(self, symbol: Symbol, leverage: int):
        return await self.binance_service.set_leverage(symbol, leverage)
    
    async def get_position_info(self, symbol: Symbol):
        return await self.binance_service.get_position_info(symbol)
    
    async def get_wallet_balance(self):
        return await self.binance_service.get_wallet_balance()

    async def get_current_price(self,symbol: Symbol):
        if self.config.exchange == Exchange.Binance:
            return await self.binance_service.get_current_price(symbol)
        elif self.config.exchange == Exchange.Bybit:
            return await self.bybit_service.get_current_price(symbol)
        elif self.config.exchange == Exchange.Okx:
            return await self.okx_service.get_current_price(symbol)
        else:
            logging.error("Unknown exchange")
            return None
        
    async def get_order_book(self,symbol:Symbol):
        if self.config.exchange == Exchange.Binance:
            return await self.binance_service.get_order_book(symbol)
        else:
            logging.error("Unknown exchange")
            return None

    async def listen_order_status(self):
        if self.config.exchange == Exchange.Binance:
            return await self.binance_service.listen_order_status(self.on_order_update)
        else:
            logging.error("Unknown exchange")
            return None
        
    async def get_open_orders(self):
        if self.config.exchange == Exchange.Binance:
            # 呼叫 BinanceService 並傳入 on_active_order_interval callback
            return await self.binance_service.get_open_orders(self.on_active_order_interval)
        else:
            logging.error("Unknown exchange")
            
    async def cancel_order(self, symbol:Symbol, client_order_id: str):
        if self.config.exchange == Exchange.Binance:
            return await self.binance_service.cancel_order(symbol, client_order_id)
        else:
            logging.error("Unknown exchange")

    async def listen_open_orders_periodically(self):
        """
        每 60 秒呼叫一次 Binance 的 get_open_orders API，
        將回傳的 open orders 轉換成 ActiveOrder 後，
        傳給 on_active_order_interval 處理。
        """
        while True:
            try:
                # 由 get_open_orders 內部已使用 on_active_order_interval 處理資料，
                # 這裡只需等待該方法完成即可。
                await self.get_open_orders()
            except Exception as e:
                logging.error("取得 open orders 時發生錯誤: %s", e)
            await asyncio.sleep(60)         

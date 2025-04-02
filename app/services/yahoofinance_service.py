from app.config.settings import settings 
from app.utils.logger import logger


import json
import yfinance as yf

class YahooFinanceService:

    def __init__(self):
        logger.info('Started YahooFinanceService')
        
    def get_stock_price(self, stock_symbol: str):
        logger.info(f'# Getting stock price for {stock_symbol}')
        return 10.0
    
    def get_historical_stock_quote(self, stock_symbol: str, period: str):
        logger.info(f'# Getting historical stock quote for {stock_symbol} with period {period}')
        
        try:
            ticker_obj = yf.Ticker(f'{stock_symbol}.SA')
            if not ticker_obj:
                raise Exception('Ticker object not found')


            hist = ticker_obj.history(period=period, auto_adjust=False)
            if hist.empty:
                raise Exception('# Empty DataFrame - might be caused by an invalid symbol')

            if len(hist) > 30:
                slice_size = int(len(hist) / 30)
                hist = hist.iloc[::slice_size][::-1]

            hist.index = hist.index.strftime('%m-%d-%Y')
            return hist.to_json()
        
        except Exception as e:
            logger.error(f'# Error getting historical stock quote for {stock_symbol} with period {period}')
            logger.error(e)
        

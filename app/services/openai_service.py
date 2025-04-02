import json
from app.config.settings import settings 
from app.utils.logger import logger
from app.utils.error_handler import custom_error_handler
from app.services.yahoofinance_service import YahooFinanceService

import openai

class OpenAIService:

    def __init__(self):
        self.client = openai.Client()
        logger.info('Started OpenAIService')
        self.model = 'gpt-3.5-turbo-0125'
        self.tools = [
            {
            'type': 'function',
            'function': {
                'name': 'get_historical_stock_quote',
                'description': 'Returns the daily historical stock quote for a Bovespa stock',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'ticker': {
                        'type': 'string',
                        'description': 'The stock ticker. Example: "ABEV3" for Ambev, "PETR4" for Petrobras, etc.'
                        },
                        'period': {
                        'type': 'string',
                        'description': 'The period for which historical data will be returned, \
                                where "1mo" corresponds to one month of data, "1d" to \
                                one day, and "1y" to one year',
                        'enum': ["1d","5d","1mo","6mo","1y","5y","10y","ytd","max"]
                        }
                    }
                }
            }
            }
        ]
        self.available_functions = {'get_historical_stock_quote': get_historical_stock_quote}

    
    def generate_response(self, messages):
        response = self.client.chat.completions.create(
        messages=messages,
        model=self.model,
        tools=self.tools,
        )
        tool_calls = response.choices[0].message.tool_calls

        if tool_calls:
            messages.append(response.choices[0].message)
            for tool_call in tool_calls:
                func_name = tool_call.function.name
                function_to_call = self.available_functions[func_name]
                func_args = json.loads(tool_call.function.arguments)
                func_return = function_to_call(**func_args)
                messages.append({
                'tool_call_id': tool_call.id,
                'role': 'tool',
                'name': func_name,
                'content': func_return
                })
        second_response = self.client.chat.completions.create(
            messages=messages,
            model=self.model,
        )
        messages.append(second_response.choices[0].message)
        
        print(f'Assistant: {messages[-1].content}')

        return messages

    def start_chat(self):

        """"
        Starts the chat with the user.
        """
        while True:
            user_input = input('User: ')
            messages = [{'role': 'user', 'content': user_input}]
            messages = self.generate_response(messages)

def get_historical_stock_quote(ticker, period):
    """
    Returns the daily historical stock quote for a Bovespa stock.
    :param ticker: The stock ticker. Example: "ABEV3" for Ambev, "PETR4" for Petrobras, etc.
    :param period: The period for which historical data will be returned, where "1mo" corresponds to one month of data,
                    "1d" to one day, and "1y" to one year.
    :return: A dictionary containing the historical stock quote.
    """
    yfinance = YahooFinanceService()
    ticker_hist = yfinance.get_historical_stock_quote(
        ticker, period
    )
    
    return ticker_hist

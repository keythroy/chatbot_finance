import json
import yfinance as yf

import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

client = openai.Client()


def get_historical_stock_quote(
    ticker,
    period='1mo'
):
    print('get_historical_stock_quote',ticker)
    ticker = ticker.replace('.SA', '')
    ticker_obj = yf.Ticker(f'{ticker}.SA')
    hist = ticker_obj.history(period=period)['Close']
    # hist.index = hist.index.astype(str)
    
    #hist.index = hist.index.strftime('%Y-%m-%d').tolist()
    hist = round(hist, 2)
    if len(hist) > 30:
        slice_size = int(len(hist) / 30)
        hist = hist.iloc[::-slice_size][::-1]
        return hist.to_json()

# qual é a cotação da vale agora?

tools = [
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

available_functions = {'get_historical_stock_quote': get_historical_stock_quote}


def generate_response(messages):
    response = client.chat.completions.create(
    messages=messages,
    model='gpt-3.5-turbo-0125',
    tools=tools,
    tool_choice='auto'
    )


    tool_calls = response.choices[0].message.tool_calls

    if tool_calls:
        messages.append(response.choices[0].message)
        for tool_call in tool_calls:
            func_name = tool_call.function.name
            function_to_call = available_functions[func_name]
            func_args = json.loads(tool_call.function.arguments)
            func_return = function_to_call(**func_args)
            messages.append({
            'tool_call_id': tool_call.id,
            'role': 'tool',
            'name': func_name,
            'content': func_return
            })
    second_response = client.chat.completions.create(
        messages=messages,
        model='gpt-3.5-turbo-0125',
    )
    messages.append(second_response.choices[0].message)
    
    print(f'Assistant: {messages[-1].content}')

    return messages

def start_chat():
    print('Welcome to Your Financial ChatBot.')

    while True:
        user_input = input('User: ')
        messages = [{'role': 'user', 'content': user_input}]
        messages = generate_response(messages)



if __name__ == '__main__':
    start_chat()
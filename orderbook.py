from functions import *
import re, time
import asyncio, aiohttp
from project_exceptions import InvalidTokenError

class Books:
    """A class to fetch and process order book data for a cryptocurrency pair from multiple exchanges."""
    
    def __init__(self, pair='BTC_USDT', limit=100):
        """Initialize the Books object with a pair and limit.
        
        Args:
            pair (str): A string representing the cryptocurrency pair, e.g., 'BTC_USDT'.
            limit (int): The maximum number of bids and asks to fetch from each exchange.
        """
        if re.search(r"^(\w+)_(\w+)$", pair):
            self.pair = pair
        else:
            raise InvalidTokenError("Invalid pair parameter: pair must be separated by an underscore, i.e., 'BTC_USDT'")
        self.limit = limit
        self.urls = self.generate_urls()

    def generate_urls(self):
        """Generate the URLs for each exchange based on the provided pair and limit.
        
        Returns:
            dict: A dictionary containing the URLs for each exchange.
        """
        pair_formatted = {
            'binance': self.pair.replace('_', '').upper(),
            'bitfinex': self.pair.replace('_', '')[:-1].upper(),
            'kucoin': self.pair.replace('_', '-').upper(),
            'okx': self.pair.replace('_', '-').upper(),
            'gate': self.pair.upper(),
            'huobi': self.pair.replace('_', '').lower(),
            'mexc': self.pair.upper().replace('_', '')
        }
        return {
            'binance': f"https://api.binance.com/api/v3/depth?symbol={pair_formatted['binance']}&limit={self.limit}",
            'bitfinex': f"https://api-pub.bitfinex.com/v2/book/t{pair_formatted['bitfinex']}/P0?len=100",
            'kucoin': f"https://api.kucoin.com/api/v1/market/orderbook/level2_100?symbol={pair_formatted['kucoin']}",
            'okx': f"https://www.okx.com/api/v5/market/books?instId={pair_formatted['okx']}&sz=400",
            'gate': f"https://api.gateio.ws/api/v4/spot/order_book?currency_pair={pair_formatted['gate']}&limit=1000",
            'huobi': f"https://api.huobi.pro/market/depth?symbol={pair_formatted['huobi']}&type=step0",
            'mexc': f"https://api.mexc.com/api/v3/depth?symbol={pair_formatted['mexc']}"
        }

    async def make_request(self, name, url):
        """Make an asynchronous request to fetch data from an exchange.
        
        Args:
            name (str): The name of the exchange.
            url (str): The URL to fetch data from the exchange.
            
        Returns:
            dict: A dictionary containing the exchange name and the fetched JSON data.
        """
        async with aiohttp.ClientSession() as session:
            try:
                response = await session.get(url)
                return {name: await response.json()}
            except aiohttp.ClientConnectorError:
                pass

    async def process_requests(self):
        """Process the asynchronous requests to fetch data from all exchanges.
        
        Returns:
            list: A list of dictionaries containing the exchange names and their fetched JSON data.
        """
        tasks = [asyncio.ensure_future(self.make_request(name, url)) for name, url in self.urls.items()]
        responses = await asyncio.gather(*tasks)
        return responses

   
    def process(self):
        """Fetch and process order book data for the cryptocurrency pair from multiple exchanges.
        
        Returns:
            dict: A dictionary containing the cryptocurrency pair and formatted data for each exchange.
        """
        raw_data = asyncio.run(self.process_requests())
        formatted_data = {}

        for exchange_data in raw_data:
            if exchange_data:
                for exchange, data in exchange_data.items():
                    if exchange == 'binance':
                        if "bids" in data:
                            formatted_data[exchange] = {"bids": data["bids"][:self.limit], "asks": data["asks"][:self.limit]}

                    elif exchange == 'bitfinex':
                        if "error" not in data:
                            bids = [[price, size] for price, count, size in data if size > 0]     #count is the Number of orders at that price level, only applicable to bitfinexapi
                            asks = [[price, abs(size)] for price, count, size in data if size < 0]
                            formatted_data[exchange] = {"bids": bids, "asks": asks}

                    elif exchange == 'okx':
                        if data['code'] == "0":
                            bids = [[price, size] for price, size, _, _ in data["data"][0]["bids"]] 
                            asks = [[price, size] for price, size, _, _ in data["data"][0]["asks"]]
                            formatted_data[exchange] = {"bids": bids, "asks": asks}

                    elif exchange == 'gate':
                        if "asks" in data:
                            formatted_data[exchange] = {"bids": data["bids"], "asks": data['asks']}

                    elif exchange == 'huobi':
                        if "tick" in data:
                            formatted_data[exchange] = data["tick"]

                    elif exchange == 'mexc':
                        if "bids" in data:
                            formatted_data[exchange] = {"bids": data["bids"], "asks": data['asks']}

                    elif exchange == 'kucoin':
                        if data["code"] != "429000" and data["data"]["bids"]:
                            formatted_data[exchange] = {"bids": data["data"]["bids"], "asks": data["data"]["asks"]}

        return {'pair': self.pair, 'data': formatted_data}

 
 
if __name__ == "__main__":  
    st = time.time()
    book = Books('INT_USDT')
    responses = book.process()
    print(responses)
    print(time.time() - st)
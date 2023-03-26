from orderbook import Books
import urllib.request
from urllib.error import URLError
from project_exceptions import InvalidTokenError


class ArbitrageDetector:
    """
    This class analyzes arbitrage opportunities among different exchanges.
    """
    
    def __init__(self, token):
        """
        Initializes the ArbitrageAnalyzer with a given token.
        
        :param token: A string representing the token symbol (e.g., 'BTC').
        """
        self.token = token.upper()

    def get_order_book_data(self):
        """
        Fetches the order book data for the specified token from the Books class.
        
        :return: A dictionary containing the order book data for the given token.
        """
        try:
            order_book = Books(self.token)
            return order_book.process()['data']
        except InvalidTokenError as e:
            raise ValueError("Invalid Token Input")

    def get_buy_quantity(self, data, buy_amount):
        """
        Calculate the maximum buy quantity for each exchange given a specific buy amount.
        
        :param data: A dictionary containing the order book data for the token.
        :param buy_amount: A float representing the buy amount in USDT.
        :return: A dictionary containing the exchange names and their corresponding maximum buy quantity.
        """
        exchange_quantities = {}
        for exchange, order_data in data.items():
            asks = order_data['asks']
            total_value = 0
            total_amount = 0
            for price, amount in asks:
                total_value += float(amount) * float(price)
                total_amount += float(amount)
                if total_value > buy_amount:
                    quantity = buy_amount / (total_value / total_amount)
                    exchange_quantities[exchange] = quantity
                    break
        max_quantity = max(exchange_quantities.values())
        return {exchange: max_quantity for exchange, quantity in exchange_quantities.items() if quantity == max_quantity}

    def get_sell_amount(self, data, sell_quantity):
        """
        Calculate the maximum sell amount for each exchange given a specific sell quantity.
        
        :param data: A dictionary containing the order book data for the token.
        :param sell_quantity: A float representing the sell quantity of the token.
        :return: A dictionary containing the exchange names and their corresponding maximum sell amount.
        """
        exchange_amounts = {}
        for exchange, order_data in data.items():
            bids = order_data['bids']
            total_value = 0
            total_amount = 0
            for price, amount in bids:
                total_value += float(amount) * float(price)
                total_amount += float(amount)
                if total_amount > sell_quantity:
                    sell_amount = (total_value / total_amount) * sell_quantity
                    exchange_amounts[exchange] = sell_amount
                    break
        max_amount = max(exchange_amounts.values())
        return {exchange: max_amount for exchange, amount in exchange_amounts.items() if amount == max_amount}

    def check_internet_connection(self):
        """Check if there is an active internet connection."""
        try:
            urllib.request.urlopen('https://google.com')  # Python 3.x
            return True
        except URLError:
            return False

    def run(self, start: int = 100, add: int = 100):
        """
        Analyzes arbitrage opportunities and prints the results.

        :param start: An integer representing the starting buy amount in USDT (default: 100).
        :param add: An integer representing the increment for each iteration (default: 100).
        :return: 0 if there's an arbitrage opportunity, 1 otherwise.
        """
        token = self.token.upper()
        order_book_data = self.get_order_book_data()
        turns = 100
        list_of_amounts = list(range(start, (add * turns) + start, add))

        if order_book_data:
            buy_data = [self.get_buy_quantity(order_book_data, amount) for amount in list_of_amounts]
            buy_dict = {value: key for each in buy_data for key, value in each.items()}
            buy_list = sorted(buy_dict)

            sell_data = [self.get_sell_amount(order_book_data, amount) for amount in buy_list]
            sell_dict = {value: key for each in sell_data for key, value in each.items()}
            sell_list = sorted(sell_dict)

            final_buy_dict = {amount: buy_dict[amount] for amount in buy_list}
            final_sell_dict = {amount: sell_dict[amount] for amount in sell_list}
            final_sell_dict = {list_of_amounts[index]: item for index, item in enumerate(final_sell_dict.items())}

            diff_list = []
            for num, item in enumerate(final_sell_dict.items()):
                key, value = item
                diff = value[0] - key
                diff_list.append(diff)
                if max(diff_list) > diff:
                    if (diff_list[num-1] / list(final_sell_dict.items())[num-1][0]) > 0.0:
                        print("\n")
                        return(f"Using ${list(final_sell_dict.items())[num-1][0]} or less, buy {token} from {list(final_buy_dict.items())[num-1][1]} to {list(final_sell_dict.items())[num-1][1][1]} for ${diff_list[num-1]} profit.")
                        return 0
                    else:
                        return 1
            else:
                start = list(final_sell_dict.items())[num-1][0]
                self.run()
                if (diff_list[num-1] / list(final_sell_dict.items())[num-1][0]) > 0.0:
                    return(f"Using ${list(final_sell_dict.items())[num-1][0]} or less, buy {token} from {list(final_buy_dict.items())[num-1][1]} to {list(final_sell_dict.items())[num-1][1][1]} for ${diff_list[num-1]} profit.")
                    return 0
        else:
            print("TOKEN NOT FOUND ON ALL EXCHANGES")


if __name__ == "__main__":
   
    token = input("Enter the token symbol: ")
    arbitrage_detector = ArbitrageDetector(token)
    if arbitrage_detector.check_internet_connection():
        arbitrage_detector.run()
    else:
        print("No internet connection. Please check your connection and try again.")
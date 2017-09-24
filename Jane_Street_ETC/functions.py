import json
from portfolio import portfolio

class Functions():

    def __init__(self):
        self.order_id = 0
        self.portfolio = portfolio()
    	
    def strategy(self, message_dict):
        self.update_portfolio(message_dict)
        print(message_dict)
        if message_dict["type"] ==  & message_dict["symbol"] == "BOND":
            trade_bonds()
        else:
            return (0,0)

    def update_portfolio(self, message_dict):
        if message_dict["type"] == "trade":
            portfolio.set_last_sold(self.message_dict["symbol"], self.message_dict["price"])
        if message_dict["type"] == "book":
            highest_bid = self.message_dict["buy"][0][0]
            lowest_offer = self.message_dict["sell"][0][0]
            fair_price = (highest_bid + fair_price)/2
            portfolio.set_fair_price(self.message_dict["symbol"], fair_price)

    def trade_bonds(self):
        if self.message_dict["type"] == "book":
            if self.message_dict["buy"][0][0] > 1000:
                sell_bonds(self.message_dict["buy"][0][0], 1)
            elif self.message_dict["sell"][0][0] < 1000:
                buy_bonds(self.message_dict["sell"][0][0], 1)

    def sell_bonds(self, price ,quantity):
        #{"type": "add", "order_id": 5, "symbol": "BOND", "dir": "BUY", "price": 1002, "size": 50}
        order = {"type": "add", "order_id": self.order_id, "symbol": "BOND", "dir": "SELL", "price": price, "size": quantity}
        self.order_id += 1
        return (json.dumps(order),1)

    def buy_bonds(self, price, quantity):
        order = {"type": "add", "order_id": self.order_id, "symbol": "BOND", "dir": "BUY", "price": price, "size": quantity}
        self.order_id += 1
        return (json.dumps(order),1)


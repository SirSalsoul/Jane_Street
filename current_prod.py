from __future__ import print_function

import sys
import socket
import json

def connect():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("test-exch-disciplesofjy", 25000))
	return s.makefile('rw', 1)

def write(exchange, obj):
	json.dump(obj, exchange)
	exchange.write("\n")

def read(exchange):
	return json.loads(exchange.readline())

def main():
	exchange = connect()
	write(exchange, {"type": "hello", "team": "DISCIPLESOFJY"})
	hello_from_exchange = read(exchange)
	print("The exchange replied:", hello_from_exchange, file=sys.stderr)
	i = 0
	while True:
		message = read(exchange)
		if message["type"] == "fill":
			print(message)
		if (message["type"] == "book"):
			#print(message)
			if message["symbol"] != "BOND":
				if (len(message["buy"]) > 0) & (len(message["sell"]) > 0):
					buy_price = message["buy"][0][0]
					sell_price = message["sell"][0][0]
					gap = sell_price - buy_price
					#print(gap)
					if gap > 7:
						write(exchange,{"type": "add", "order_id": i, "symbol": message["symbol"], "dir": "BUY", "price": buy_price+1, "size": 1})
						i += 1
						write(exchange,{"type": "add", "order_id": i, "symbol": message["symbol"], "dir": "SELL", "price": sell_price-1, "size": 1})
						i += 1

if __name__ == "__main__":
	main()

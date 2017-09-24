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
	fmvs = {}
	while True:
		message = read(exchange)
		if message["type"] == "fill":
			print(message)
		if (message["type"] == "book"):
			#print(message)
			
			if (len(message["buy"]) > 0) & (len(message["sell"]) > 0):
				highest_bid = message["buy"][0][0]
				lowest_offer = message["sell"][0][0]
				gap = lowest_offer - highest_bid
				symbol = message["symbol"]
				fmvs[symbol] = (gap/2) + highest_bid
				xlf_fmv = 0
				
				if ("GS" in fmvs) and ("MS" in fmvs) and ("WFC" in fmvs) and ("BOND" in fmvs):
                                	xlf_fmv = ((2*fmvs["GS"]) + (3*fmvs["MS"]) + (2*fmvs["WFC"]) + (3*fmvs["BOND"]))/10
                                	buy_midpoint = (buy_price + xlf_fmv)/2
                                	sell_midpoint = (sell_price + xlf_fmv)/2	
				#print(gap)
				if gap > 7:
					sell_price = lowest_offer - 1
					buy_price = highest_bid + 1
					if symbol == "XLF":
						if xlf_fmv != 0:
							print(xlf_fmv)
							if buy_price < buy_midpoint:
								write(exchange,{"type": "add", "order_id": i, "symbol": message["symbol"], "dir": "BUY", "price": buy_price, "size": 1})
								i += 1
							if sell_price > xlf_fmv:
								write(exchange,{"type": "add", "order_id": i, "symbol": message["symbol"], "dir": "SELL", "price": sell_price, "size": 1})
								i += 1
							else:
								write(exchange,{"type": "add", "order_id": i, "symbol": message["symbol"], "dir": "SELL", "price": sell_midpoint, "size": 1})
						else:
							write(exchange,{"type": "add", "order_id": i, "symbol": message["symbol"], "dir": "BUY", "price": buy_price, "size": 1})
							i += 1
							write(exchange,{"type": "add", "order_id": i, "symbol": message["symbol"], "dir": "SELL", "price": sell_price, "size": 1})
							i += 1
				
if __name__ == "__main__":
	main()

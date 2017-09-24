from __future__ import print_function

import sys
import socket
import json
import time
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
	high_bids = {}
	low_sells = {}
	xtf_bonds = 0
	xtf_gs = 0
	xtf_ms = 0
	xtf_wfc = 0

	bonds = 0
	gs = 0
	ms = 0
	wfc = 0

	while True:
		time.sleep(.01)
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
				high_bids[symbol] = highest_bid
				low_sells[symbol] = lowest_offer
				if "XLF" in high_bids and "BOND" in low_sells and "GS" in low_sells and "MS" in low_sells and "WFC" in low_sells:
					if high_bids["XLF"] > (10 + 3*low_sells["BOND"] + 2*low_sells["GS"] + 3*low_sells["MS"] + 2*low_sells["WFC"]):
						if xtf_bonds < 3:
							write(exchange,{"type": "add", "order_id": i, "symbol": "BOND", "dir": "BUY", "price": buy_price, "size": 1})
							i += 1
							xtf_bonds += 1
						if xtf_gs < 2:
                                                        write(exchange,{"type": "add", "order_id": i, "symbol": "GS", "dir": "BUY", "price": buy_price, "size": 1})
                                                        i += 1
                                                        xtf_gs += 1
						if xtf_ms < 3:
                                                        write(exchange,{"type": "add", "order_id": i, "symbol": "symbol", "dir": "BUY", "price": buy_price, "size": 1})
                                                        i += 1
                                                        xtf_ms += 1
						if xtf_wfc < 2:
							write(exchange,{"type": "add", "order_id": i, "symbol": "WFC", "dir": "BUY", "price": buy_price, "size": 1})
							i += 1
							xtf_wfc += 1
						if xtf_bonds >=3 and xtf_gs >=2 and xtf_ms >= 3 and xtf_wfc >= 2:
							write(exchange,{"type": "convert", "order_id": i, "symbol": "XTF", "dir": "BUY", "size": 1})
							i+=1
				if "XLF" in low_sells and "BOND" in high_bids and "GS" in high_bids and "MS" in high_bids and "WFC" in high_bids:	
					if low_sells["XLF"] < (10 + 3*high_bids["BOND"] + 2*high_bids["GS"] + 3*high_bids["MS"] + 2*high_bids["WFC"]):
							if bonds < 3:
                                                        	bonds += 1
							if gs < 2:
                                                        	gs += 1
							if ms < 3:
                                                        	ms += 1
							if wfc < 2:
                                                        	wfc += 1
							if bonds >=3 and gs >=2 and ms >= 3 and wfc >= 2:
                                                        	write(exchange,{"type": "convert", "order_id": i, "symbol": "XLF", "dir": "SELL", "size": 1})
                                                        	i+=1
				if gap > 7:
					sell_price = lowest_offer - 1
					buy_price = highest_bid + 1

					write(exchange,{"type": "add", "order_id": i, "symbol": message["symbol"], "dir": "BUY", "price": buy_price, "size": 1})
					i += 1
					write(exchange,{"type": "add", "order_id": i, "symbol": message["symbol"], "dir": "SELL", "price": sell_price, "size": 1})
					i += 1

if __name__ == "__main__":
	main()

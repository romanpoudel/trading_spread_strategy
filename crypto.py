import ccxt
import time

API_KEY='VucYuqs8WebqRZ3qiS'
API_SECRET='AyL7MKYmCMTFtHEYK85YBgNl2itjxSREHoeM'

bybit = ccxt.bybit({
    'enableRateLimit': True,
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'test': True    
})
bybit.set_sandbox_mode(True)
# print(bybit.fetch_balance())


symbol = 'BCH/USDT'
order_amount = 1
spread = 0.01
orderbook_depth = 5
interval = 15

# print(bybit.fetch_trades(symbol)[0]['price'])
def get_orderbook():
    orderbook = bybit.fetch_order_book(symbol,orderbook_depth)
    
    bids = orderbook["bids"]
    asks = orderbook["asks"]
    return bids,asks



def calculate(bids,asks):
    if len(bids)==0:
        highest_bid_from_orderbook=bybit.fetch_trades(symbol)[0]['price']
    else:
        highest_bid_from_orderbook=bids[0][0]
        
    
    if len(asks)==0:
        lowest_ask_from_orderbook=bybit.fetch_trades(symbol)[0]['price']
    else:
        lowest_ask_from_orderbook=asks[0][0]
    
    mid_price = (highest_bid_from_orderbook + lowest_ask_from_orderbook) / 2
    bid_price = mid_price - (mid_price * spread)
    ask_price = mid_price + (mid_price * spread)
    return bid_price,ask_price

def place_order(bid_price,ask_price):
    bid=bybit.create_limit_buy_order(symbol,order_amount,bid_price)
    ask=bybit.create_limit_sell_order(symbol,order_amount,ask_price)
    print('Order Placed')

def cancel_order():
    bybit.cancel_all_orders(symbol)
    

try:
    while True:
        bids,asks=get_orderbook()
        bid_price,ask_price=calculate(bids,asks)
        place_order(bid_price,ask_price)
        time.sleep(interval)
        if bybit.fetch_open_orders(symbol):
            cancel_order() 
except KeyboardInterrupt:
    print("Exiting..") 
    cancel_order()

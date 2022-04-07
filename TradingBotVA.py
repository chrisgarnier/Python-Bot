import websocket, json ,pprint, talib, numpy, config,csv
import pandas as pd
from binance.client import Client 
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
import datetime
import time
client = Client(config.API_KEY,config.API_SECRET, tld='us')
SOCKET ="wss://stream.binance.com:9443/ws/adausdt@kline_1m"
Sell_Triggers = 0
Buy_Triggers = 0
No_Triggers=0
closes = []
buy_price = 0
sell_price = 0
threshold = .00900
tolerance = .0025
headers = ['Date' + '\t','Open''\t','High'+'\t','Low'+'\t','Close'+'\t','Volume'+'\t']
trade_id = ''
TRADE_SYMBOL = 'ADAUSDT'
TRADE_QUANTITY = str(450)
in_position = True
buy_order_placed = False
sell_order_placed = False
#First create bot that does percent changes over longer period of time, than the rapid decay and rapid growth (model used for quikbots)
#start with object oriented programming
#create function for finding a "trading" period, how many ticks before the bots +
# + random fluctions repeat themselves, start and stop are not well defined until the period is determined
#create function for the time inbetween periods. When the random fluctions dominate trends
#create function that analyzes trading periods maybe use deep learning to guess a generic shape -
# -of the next probable periods
#create arapid buy/sell order function for after large random fluctations occur
# create an algo for general short cycle periodic trading have deep learning class- 
# -instantiate generalized parameters 
# think of some indicator that measures the momentum of charts similar to rsi except shorter term
# fix DifInCand function when you can think again
#remember, you are not a billion dollar hedgefund with infinite man power,-
# -resources, and experience

def order(sym,sides,typ,time,quant,price):
    global trade_id
    try:
        json.ord = client.create_test_order(
        symbol=sym,
        side=sides,
        type=typ,
        timeInForce=time,
        quantity=quant,
        price=price)
        trade_id = str(json.ord['orderId'])
        return  pprint.pprint(json.ord)
    except BinanceAPIException as e:
        print(e)
    except BinanceOrderException as e:  
        print(e)



def place_sell_order(someFloatArray,threshold,tolerance):
    #if the price increased 1 cent within 20 seconds (spiked) sell 
    global Sell_Triggers
    global sell_order_placed
    global sell_price
    difArray = []
    if len(someFloatArray) == 1 or len(someFloatArray) == 2:
            pass
    elif len(someFloatArray) ==3:
            pass
    elif len(someFloatArray) ==4:
            pass
    elif len(someFloatArray) ==5:
            pass
    elif len(someFloatArray) ==6:
            pass
    elif len(someFloatArray) ==7:
            pass
    elif len(someFloatArray) ==8:
            pass
    elif len(someFloatArray) ==9:
            pass
    elif len(someFloatArray) ==10:
        value = 0
        total = 0
        for i in range(len(someFloatArray)-1):
            value = someFloatArray[i+1] - someFloatArray[i]
            difArray.append(value)
            total += value
        print('Closing Prices SO:',['{:0.7f}'.format(x) for x in someFloatArray ])
        print('Difference Array:',[ '{:0.6f}'.format(x) for x in difArray ])
        print('Total Difference:', '{:0.6f}'.format(total))
        if total > threshold: 
            Sell_Triggers +=1
            print("Sell Triggers:",Sell_Triggers)
            sell_price = someFloatArray[-1] + tolerance
            print("Selling at ",'{:0.6f}'.format(sell_price))
            time_now = datetime.datetime.utcnow()
            print(time_now)
            someFloatArray.clear()
            sell_order_placed = True
            return order(sym=TRADE_SYMBOL,sides=Client.SIDE_SELL,
            typ=Client.ORDER_TYPE_LIMIT,time='GTC',
            quant= TRADE_QUANTITY,price=float(round(sell_price,8)))
        else:
            del someFloatArray[0]
    elif len(someFloatArray) == 11:
            del someFloatArray[0]
            


def place_buy_order(someFloatArray,threshold,tolerance):
    #if the price decreased 1 cent within 20 seconds (crashed) buys
    global Buy_Triggers
    global buy_order_placed
    global buy_price
    difArray = []
    if len(someFloatArray) == 1 or len(someFloatArray) == 2:
            pass
    elif len(someFloatArray) ==3:
            pass
    elif len(someFloatArray) ==4:
            pass
    elif len(someFloatArray) ==5:
            pass
    elif len(someFloatArray) ==6:
            pass
    elif len(someFloatArray) ==7:
            pass
    elif len(someFloatArray) ==8:
            pass
    elif len(someFloatArray) ==9:
            pass
    elif len(someFloatArray) ==10:
        value = 0
        total = 0
        for i in range(len(someFloatArray)-1):
            value = someFloatArray[i+1] - someFloatArray[i]
            difArray.append(value)
            total += value
        print('Closing Prices BO:',['{:0.7f}'.format(x) for x in someFloatArray ])
        print('Difference Array:',[ '{:0.6f}'.format(x) for x in difArray ])
        print('Total Difference:', '{:0.6f}'.format(total))
        if total < -threshold: 
            Buy_Triggers +=1
            print("Buy Triggers:",Buy_Triggers)
            buy_price = someFloatArray[-1] - tolerance
            print("Buying at ",'{:0.6f}'.format(buy_price))
            time_now = datetime.datetime.utcnow()
            print(time_now)
            someFloatArray.clear()
            buy_order_placed = True
            return order(sym=TRADE_SYMBOL,sides=Client.SIDE_BUY,
            typ=Client.ORDER_TYPE_LIMIT,time='GTC',
            quant= TRADE_QUANTITY,price=float(round(buy_price,8)))
        else:
            del someFloatArray[0]
    elif len(someFloatArray) == 11:
            del someFloatArray[0]
            
#need global variables
def makebuyFalse():
    global buy_order_placed
    buy_order_placed = False
def makesellFalse():
    global sell_order_placed
    sell_order_placed = False    
def makepositionFalse():
    global in_position
    in_position = False 
def makepositionTrue():
    global in_position
    in_position = True   
def get_order_status(symb,tradeID):
    json.order = client.get_order(
    symbol=symb,
    orderId=tradeID)
    status = str(json.order['status'])
    return status
    
       
        
def on_error(ws, error):
    print(error)
    
   

def on_open(ws):
    print('Opened connection to Christophers account:')
    json.info  =client.get_account()
    pprint.pprint(json.info)
    with open('data.txt', 'w') as f:
        f.writelines(headers)
        f.write('\n')
        f.close

def on_close(ws):
    print('closed connection')

def on_message(ws,message):
    #grabs the info from binance and sends to data file for real analysis.
    json.message =json.loads(message)
    candle = json.message['k']
    dataArray = []
    now = datetime.datetime.utcnow()
    closes.append(float(candle['c']))
    dataArray.append(str(now)+'\t')
    dataArray.append(str(candle['o'])+'\t')
    dataArray.append(str(candle['h'])+'\t')
    dataArray.append(str(candle['l'])+'\t')
    dataArray.append(str(candle['c'])+'\t')
    dataArray.append(str(candle['v'])+'\t')  
    with open('data.txt', 'a') as f:
        f.writelines(dataArray)
        f.write('\n')
        f.close  
    dataArray=[]
    if in_position == False and buy_order_placed == False:
        print('Not in position, attempting to place buy order')
        place_buy_order(closes,threshold,tolerance)
    elif in_position == False and buy_order_placed == True:
        while buy_order_placed:
            #print('Buy order placed attempting to Fill')
            time.sleep(2)
            get_order_status(TRADE_SYMBOL,trade_id)
            if get_order_status(TRADE_SYMBOL,trade_id) == 'FILLED':
                #print('Buy order FILLED')
                makepositionTrue()
                makebuyFalse()
                break
            if get_order_status(TRADE_SYMBOL,trade_id) == 'NEW':
                continue
        #print(in_position)
        #print(buy_order_placed)
        #print(sell_order_placed)
    elif in_position == True and sell_order_placed == False:
        #print('In position, attempting to place sell order')
        place_sell_order(closes,threshold,tolerance)
    elif in_position == True and sell_order_placed == True:
        while sell_order_placed:
            print('Sell order placed attempting to Fill')
            time.sleep(2)
            get_order_status(TRADE_SYMBOL,trade_id)
            if get_order_status(TRADE_SYMBOL,trade_id) == 'FILLED':
                #print('Sell order FILLED')
                makepositionFalse()
                makesellFalse()
                break
            if get_order_status(TRADE_SYMBOL,trade_id) == 'NEW':
               continue
        #print(in_position)
        #print(buy_order_placed)
        #print(sell_order_placed)

ws = websocket.WebSocketApp(SOCKET, on_open= on_open, on_close= on_close,on_message = on_message)
ws.run_forever()

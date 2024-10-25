import telepot
import requests
from datetime import datetime
from timeloop import Timeloop
from datetime import timedelta


def getStockData(ticker) :

    base_url =" https://financialmodelingprep.com/api/v3/quote/"
    key ="88bf8d3f535b2c1e1505ac38d74cf12b"
    full_url =base_url + ticker + "?apikey=" + key
    r = requests.get(full_url)    
    stock_data= r.json()
    return stock_data
real_time_data = getStockData( 'AMZN ' )
print(real_time_data)



def generateMessage(data) :
    symbol = data [0]['symbol']
    price = data [0] [ "price" ]
    changesPercent= data[0]["changesPercentage"]
    timestamp = data [0] [ 'timestamp' ]
    current =datetime.fromtimestamp(timestamp)
    
    message =str(current)
    message += "\n" + symbol
    message += "\n$" + str(price)
    if(changesPercent < -2):
        message += "\nWarning! price drop more than 2%! "
    return message
textMessage = generateMessage(real_time_data)
print (textMessage)





def sendMessage(text) :
    token ="6902842074:AAGTh1HnuNI3W8cCFF9yoytAWFhvHrV3fBQ"
    receiver_id = 5514934613
    bot = telepot. Bot (token)
    bot.sendMessage(receiver_id, text)
sendMessage(textMessage)




tl = Timeloop()
@tl.job(interval=timedelta(hours=.00278) )
def run_tasks():
    ticker = "AMZN"
    real_time_data =getStockData(ticker)
    textmessage = generateMessage(real_time_data)
    sendMessage(textMessage)
tl . start (block=True)

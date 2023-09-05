import constants
import os
import pandas as pd
import pandas_ta as ta
def getStockHistoryData(ticker):
    from datetime import datetime
    from datetime import date
    from dateutil.relativedelta import relativedelta

    three_months = date.today() + relativedelta(months=-3)

    endTime = datetime.strptime(date.today().strftime("%m/%d/%Y") + ', 23:59:00', "%m/%d/%Y, %H:%M:%S").timestamp()
    startTime = datetime.strptime(three_months.strftime("%m/%d/%Y") + ', 00:00:0', "%m/%d/%Y, %H:%M:%S").timestamp()
    import requests

    url = 'https://iboard.ssi.com.vn/dchart/api/history?resolution=D&symbol='+str(ticker)+'&from=0'+'&to='+str(endTime)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    x = requests.get(url, headers=headers)
    response = x.json()

    import numpy as np

    timestamp = np.array(response['t']).astype(int)
    close = np.array(response['c']).astype(float)
    open = np.array(response['o']).astype(float)
    high = np.array(response['h']).astype(float)
    low = np.array(response['l']).astype(float)
    volume = np.array(response['v']).astype(int)

    dataset = pd.DataFrame({'Time': timestamp, 'Open': list(open), 'High': list(high), 'Low': list(low), 'Close': list(close), 'Volume': list(volume)}, columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
    return dataset

ticker = "SAM"
htd = getStockHistoryData(ticker)
if 'Time' in htd.columns:
    from datetime import datetime
    htd['DateStr'] = htd.apply(
        lambda x: datetime.fromtimestamp(x['Time']).strftime("%Y-%m-%d"), axis=1)
macd = ta.macd(htd['Close'], 20, 5, 9)
htd['Date'] = pd.to_datetime(htd['DateStr'])
htd = htd.assign(MACD=macd['MACD_5_20_9'])
htd = htd.assign(MACDh=macd['MACDh_5_20_9'])
htd = htd.assign(MACDs=macd['MACDs_5_20_9'])
ticker_data = htd.set_index('Date').drop(columns=['Time', 'DateStr'])
saveFile = os.path.join(constants.ROOT_DIR, constants.PATH_STOCK_DATA, ticker+'.csv')
ticker_data.to_csv(saveFile, index=True)

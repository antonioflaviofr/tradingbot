from binance import Client
from sklearn import preprocessing
#from sklearn.preprocessing import StandardScaler, MinMaxScaler
from matplotlib import pyplot
import pandas as pd
import keys
import os

#Changes these values to obtain the desired csv
pair = os.getenv("PAIR", "ETHUSDT")
since = os.getenv("SINCE", "10 year ago UTC")

#Connect to the Binance client
client = Client(keys.apiKey, keys.secretKey)
# Get the data from Binance
df = client.get_historical_klines(pair, Client.KLINE_INTERVAL_1HOUR, since)

# Normalize the data
# normalizer = preprocessing.MinMaxScaler().fit(df)
# df = normalizer.transform(df)

# Transform the data to a pandas array
df = pd.DataFrame(df,
columns=[
"Open time", "Open", "High", "Low", "Close", "Volume",
"Close time", "Quote asset volume", "Number of trades",
"Taker buy base asset volume",
"Taker buy quote asset volume", "Ignore"
])

# #Plot the data
# #df.plot()

# # Add the real open and the real close to df
#df = pd.concat([df, real_df], axis=1)

df['Date'] = df['Close time']
# Drop useless columns
df.drop([
  "Open time", "Ignore", "Taker buy base asset volume",
  "Taker buy quote asset volume","Quote asset volume",
  "Number of trades", "Close time"], axis=1, inplace=True)

# # Remove the last timestep
df = df[:-1]

df['Date'] = pd.to_datetime(df['Date'], unit='ms', origin='unix')
df.set_index('Date', inplace=True)
df.sort_index(inplace=True)
df.to_csv(f"{pair}_.csv")


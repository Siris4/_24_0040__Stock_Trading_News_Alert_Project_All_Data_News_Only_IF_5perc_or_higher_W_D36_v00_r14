import requests, os, re
# import newsapi-python
from twilio.rest import Client
from datetime import datetime as dt
from datetime import timedelta


# TODO: Environment Variables to still apply:
# api_KEY  (for each API website):

STOCK_PRICE_API_KEY = os.environ.get('STOCK_PRICE_API_KEY')    #the API Key from the open weather website
print(f"The stock price api key is: {STOCK_PRICE_API_KEY}")

# news_api_key =
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')    #the API Key from the open weather website
print(f"The news price api key is: {NEWS_API_KEY}")
print()

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
print(f"The TWILIO_ACCOUNT_SID is: {TWILIO_ACCOUNT_SID}")
print(f"The TWILIO_AUTH_TOKEN is: {TWILIO_AUTH_TOKEN}")

print()

#Normal Variables:
STOCK1 = "AMZN"
COMPANY_NAME = "Amazon.com, Inc."

# account_SID (for each API):


# auth_TOKEN (for each API):



# TODO: STEP 1: Use https://www.alphavantage.co
# When STOCK1 price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# TODO: STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

# TODO: STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.


#------------------------- START OF STEP 1 -------------------------#
# Use https://www.alphavantage.co
# When STOCK1 price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# API_Weather_URL_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
full_stock_sample_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=full&apikey=demo"
Stock_Price_Alpha_Avan_URL_Endpoint = "https://www.alphavantage.co/query"

# Required Params:
'''
API Parameters
❚ Required: function

The time series of your choice. In this case, function=TIME_SERIES_INTRADAY

❚ Required: symbol

The name of the equity of your choice. For example: symbol=IBM

❚ Required: interval

Time interval between two consecutive json_data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min
'''

# https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&outputsize=full&apikey=demo
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
stock_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK1}&apikey={STOCK_PRICE_API_KEY}'
response = requests.get(stock_url)
response.raise_for_status()
json_data = response.json()

# Assuming json_data is your JSON response from the API
time_series_daily = json_data.get('Time Series (Daily)', {})
dates = list(time_series_daily.keys())
# data_list = [value for (key, value) in data.items()]

if dates:
    # First and second dates
    first_date = dates[0]  # Most recent trading day
    second_date = dates[1]  # Day before the most recent trading day

    # Fetch closing prices for these days
    stock_price_comparison1 = float(time_series_daily[first_date]['4. close']) if '4. close' in time_series_daily[
        first_date] else 0
    stock_price_comparison2 = float(time_series_daily[second_date]['4. close']) if '4. close' in time_series_daily[
        second_date] else 0

    print(f"The most recent trading day (first date) is: {first_date}")
    print(f"Closing price on the most recent trading day: ${stock_price_comparison1}\n")

    print(f"The day prior to the most recent trading day (second date) is: {second_date}")
    print(f"Closing price on the day prior to the most recent trading day: ${stock_price_comparison2}\n")

    # Calculate the percentage change between these two days
    if stock_price_comparison1 and stock_price_comparison2:
        percent_change = ((stock_price_comparison1 - stock_price_comparison2) / stock_price_comparison2) * 100
        print(f"Percentage change between {first_date} and {second_date}: {percent_change:.2f}%")
        if abs(percent_change) >= 5.00:
            news_url = f"https://newsapi.org/v2/everything?q={STOCK1}&apiKey={NEWS_API_KEY}"
            response2 = requests.get(news_url)
            response2.raise_for_status()
            news_json_data = response2.json()
            # print(news_json_data)

            print(f"Article #1 for {STOCK1}: {news_json_data['articles'][0]['content']}\n")
            print(f"Article #2 for {STOCK1}: {news_json_data['articles'][1]['content']}\n")
            print(f"Article #3 for {STOCK1}: {news_json_data['articles'][2]['content']}\n")

            text_bundled_up = (
                f"Article #1 for {STOCK1}: {news_json_data['articles'][0]['content']}\n\n"
                f"Article #2 for {STOCK1}: {news_json_data['articles'][1]['content']}\n\n"
                f"Article #3 for {STOCK1}: {news_json_data['articles'][2]['content']}"
            )

            account_sid = TWILIO_ACCOUNT_SID
            auth_token = TWILIO_AUTH_TOKEN

            client = Client(account_sid, auth_token)

            message = client.messages \
                .create(
                body=f"{text_bundled_up}",
                from_="+18888462616",
                # to='+16198800164',  #toggle this on and the one below this toggled off, to easily swap phone numbers
                to='+17654189611',  # toggle this on and the one above this toggled on, to easily swap phone numbers
                # to='+COUNTRYCODETHENFULLPHONENUMBER',
            )
            print(f"Message Status: {message.status}. Yes, the text got sent :)")
    else:
        print("Unable to calculate percentage change due to missing data.")


#------------------------- END OF STEP 1 -------------------------#

#------------------------- START OF STEP 2 -------------------------#
# Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

# news_url = f"https://newsapi.org/v2/everything?q={STOCK1}&apiKey={NEWS_API_KEY}"
# response2 = requests.get(news_url)
# response2.raise_for_status()
# news_json_data = response2.json()
# # print(news_json_data)
#
# print(f"Article #1 for {STOCK1}: {news_json_data['articles'][0]['content']}\n")
# print(f"Article #2 for {STOCK1}: {news_json_data['articles'][1]['content']}\n")
# print(f"Article #3 for {STOCK1}: {news_json_data['articles'][2]['content']}\n")
#
# text_bundled_up = (
#     f"Article #1 for {STOCK1}: {news_json_data['articles'][0]['content']}\n\n"
#     f"Article #2 for {STOCK1}: {news_json_data['articles'][1]['content']}\n\n"
#     f"Article #3 for {STOCK1}: {news_json_data['articles'][2]['content']}"
# )



#------------------------- END OF STEP 2 -------------------------#

#------------------------- START OF STEP 3 -------------------------#
# Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.

# account_sid = TWILIO_ACCOUNT_SID
# auth_token = TWILIO_AUTH_TOKEN
#
# client = Client(account_sid, auth_token)
#
# message = client.messages \
#     .create(
#     body=f"{text_bundled_up}",
#     from_="+18888462616",
#     # to='+16198800164',  #toggle this on and the one below this toggled off, to easily swap phone numbers
#     to='+17654189611',     #toggle this on and the one above this toggled on, to easily swap phone numbers
#     # to='+COUNTRYCODETHENFULLPHONENUMBER',
# )
# print(f"Message Status: {message.status}. Yes, the text got sent :)")


#------------------------- END OF STEP 3 -------------------------#

#------------------------- START OF OPTIONAL STEP 4 -------------------------#
# TODO: STEP 4: Optional: Format the SMS message like this:

"""
AMZN: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Amazon.com, Inc. (AMZN)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"AMZN: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Amazon.com, Inc. (AMZN)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

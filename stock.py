#Importing required libraries
import yfinance as yf
import datetime
import csv
import os
import pandas as pd

# taking input from user for start date and investment amount
chart_start_date = input("Enter the start date in format dd-mm-yyyy : ")
investment_amount = int(input("Enter the Investment amount : "))

# converted string to datetime
chart_start_date = datetime.datetime.strptime(chart_start_date,"%d-%m-%Y")

# calculating end date as yesterday's date
end_date = datetime.date.today()-datetime.timedelta(days=1)

#the directory path of the current Python file/CSV file
dir_path = os.path.dirname(__file__)

# open stock list csv which will be used to calculate no of shares
file = open(f'{dir_path}\Stocks.csv',encoding="utf-8")

# using dictreader for getting json values
data = csv.DictReader(file)

# iterating through the data dictionary and calculating the required values
result_dict = []
for row in data:
    company_data = {"Ticker":row["Ticker"],"Weightage":row["Weightage"]}
    try:
        # fetching stock data from yahoofinance
        stock_data = yf.download(row["Ticker"]+'.NS', ignore_tz=True,start=chart_start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"))
        
        # iterating over stock data for fetching data for all dates,
        # and then we'll calculate no of share that can be bought each day
        for i in range(len(stock_data)):
            stock_price = stock_data.iloc[i]["Close"]

            # weightage * investment amount
            w_cross_ia = float(row["Weightage"])*investment_amount

            # no of stocks can be bought for that particular date
            company_data[stock_data.index[i].strftime("%Y-%m-%d")] = w_cross_ia/stock_price
    except Exception as e:
        # logging the error
        print(str(e))
        continue
    
    # appending the final result to result list
    result_dict.append(company_data)

# creating a new csv file to store the result_dict list
filename = f"{dir_path}\ResultantData.csv"


# saving csv file in local repository
df = pd.DataFrame(result_dict)
df.to_csv(filename,index=False)
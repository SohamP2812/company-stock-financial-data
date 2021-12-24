import requests
import json
from datetime import datetime
import lxml
from lxml import html
import requests
import numpy as np
import pandas as pd

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

ticker = ""
while ticker != 'Q':
    ticker = input("Please enter a stock ticker (Press 'Q' to Quit): ")
    if(ticker == 'Q' or ticker == 'q'):
        exit()
    ticker = ticker.upper()
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    response = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/" + ticker + "?region=US&lang=en-US&includePrePost=false&interval=2m&useYfid=true&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance", headers=headers, timeout=5)

    data = response.json()
    #jprint(data)
    meta = data['chart']['result']
    if meta is None:
        print("No stock with ticker " + ticker + " found")
    else:
        for item in meta:
            try:
                print("")
                print("Currency: " + str(item['meta']['currency']))
                print("Ticker: " + str(item['meta']['symbol']))
                print("Regular Market Price: " + str(item['meta']['regularMarketPrice']))
                print("Previous Closing Price: " + str(item['meta']['previousClose']))

                print("")

                further = input("Would you like to see further financial information for " + ticker + "? (Y/N) ")
                if further == 'Y':
                    url = 'https://finance.yahoo.com/quote/' + ticker + '/balance-sheet?p=' + ticker 

                    headers = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Cache-Control': 'max-age=0',
                        'Connection': 'close',
                        'DNT': '1', # Do Not Track Request Header 
                        'Pragma': 'no-cache',
                        'Referrer': 'https://google.com',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
                    }

                    page = requests.get(url, headers=headers)

                    tree = html.fromstring(page.content)

                    tree.xpath("//h1/text()")

                    table_rows = tree.xpath("//div[contains(@class, 'D(tbr)')]")

                    assert len(table_rows) > 0

                    parsed_rows = []

                    index = 0
                    breakdown_index = 0
                    assets_index = 0
                    liabilities_index = 0

                    for table_row in table_rows:
                        parsed_row = []
                        el = table_row.xpath("./div")
                        
                        none_count = 0
                        
                        for rs in el:
                            try:
                                (text,) = rs.xpath('.//span/text()[1]')
                                parsed_row.append(text)
                            except ValueError:
                                parsed_row.append(np.NaN)
                                none_count += 1

                        if (none_count < 4):
                            parsed_rows.append(parsed_row)
                        if(parsed_row[0] == 'Breakdown'):
                            breakdown_index = index
                        if(parsed_row[0] == 'Total Assets'):
                            assets_index = index
                        if(parsed_row[0] == 'Total Liabilities Net Minority Interest'):
                            liabilities_index = index
                        index += 1

                    print("")

                    print("Breakdown for " + str(parsed_rows[breakdown_index][1]))
                    print("Total Assets: " + str(parsed_rows[assets_index][1]))
                    print("Total Liabilities Net Minority Interest: " + str(parsed_rows[liabilities_index][1]))
                    
                    
                    url = 'https://finance.yahoo.com/quote/' + ticker + '/financials?p=' + ticker 
                    page = requests.get(url, headers=headers)

                    tree = html.fromstring(page.content)

                    tree.xpath("//h1/text()")

                    table_rows = tree.xpath("//div[contains(@class, 'D(tbr)')]")

                    assert len(table_rows) > 0

                    parsed_rows = []

                    index = 0
                    revenue_index = 0
                    profit_index = 0
                    net_income_index = 0

                    for table_row in table_rows:
                        parsed_row = []
                        el = table_row.xpath("./div")
                        
                        none_count = 0
                        
                        for rs in el:
                            try:
                                (text,) = rs.xpath('.//span/text()[1]')
                                parsed_row.append(text)
                            except ValueError:
                                parsed_row.append(np.NaN)
                                none_count += 1

                        parsed_rows.append(parsed_row)
                        if(parsed_row[0] == 'Total Revenue'):
                            revenue_index = index
                        if(parsed_row[0] == 'Gross Profit'):
                            profit_index = index
                        if(parsed_row[0] == 'Net Income from Continuing & Discontinued Operation'):
                            net_income_index = index
                        index += 1

                    print("")
                    print("Total Revenue: " + str(parsed_rows[revenue_index][1]))
                    print("Gross Profit: " + str(parsed_rows[profit_index][1]))
                    print("Net Income: " + str(parsed_rows[net_income_index][1]))

            except:
                print("Error getting stock information")
    print("")
    
exit()
import datetime
import sys
import json
import requests
import csv
try:
    from urllib.request import urlopen
except ImportError:
    import urllib2

BASE_STOCK_URL = 'https://finance.yahoo.com/quote'
UNIVERSE_FILE = '/usr/src/hunter/src/data/universe.csv'
EARNINGS_FILE = '/usr/src/hunter/src/data/earnings_data.csv'
MARKET_CAP_FILE = '/usr/src/hunter/src/data/market_cap_data.csv'

class YahooFundamental(object):
    
    def _get_data_dict(self, url):
        page = requests.get(url)
        page_content = page.content
        page_data_string = [row for row in page_content.split(
            '\n') if row.startswith('root.App.main = ')][0][:-1]
        page_data_string = page_data_string.split('root.App.main = ', 1)[1]
        return json.loads(page_data_string)

    def get_next_earnings_date(self, symbol):
        url = '{0}/{1}'.format(BASE_STOCK_URL, symbol)
        try:
            page_data_dict = self._get_data_dict(url)
            print page_data_dict
            return page_data_dict['context']['dispatcher']['stores']['QuoteSummaryStore']['calendarEvents']['earnings']['earningsDate'][0]['raw']
        except:
            #raise Exception('Invalid Symbol or Unavailable Earnings Date')
            return 'DNE'
    
    def get_market_cap(self, symbol):
        url = '{0}/{1}'.format(BASE_STOCK_URL, symbol)
        try:
            page_data_dict = self._get_data_dict(url)
            return page_data_dict['context']['dispatcher']['stores']['QuoteSummaryStore']['price']['marketCap']['raw']
        except:
            raise Exception('Invalid Symbol or Unavailable Market Cap')

    def get_last_price(self, symbol):
        url = '{0}/{1}'.format(BASE_STOCK_URL, symbol)
        try:
            page_data_dict = self._get_data_dict(url)
            return page_data_dict['context']['dispatcher']['stores']['QuoteSummaryStore']['summaryDetail']['previousClose']['raw']
        except:
            raise Exception('Invalid Symbol or Unavailable Price Data')

if __name__ == '__main__':
    universefile = open(UNIVERSE_FILE)
    tickers = []

    for line in universefile:
        tickers.append(line.strip().split(','))
    
    yf = YahooFundamental()
    earnings_file = open (EARNINGS_FILE, 'w')
    marketcap_file = open (MARKET_CAP_FILE, 'w')

    for ticker in tickers:
        sys.stdout.write("Downloading: %s \r" % (ticker[1]))
        sys.stdout.flush()
        try:
            next_earning = yf.get_next_earnings_date(ticker[1])
            print next_earning
            earnings_file.write(ticker[1] + ',' + ticker[0] + ', '+ str(next_earning) + "\n")
        except:
            earnings_file.write(ticker[1] + ',' + ticker[0] + ', ' + "NA" + "\n")
        try: 
            market_cap = yf.get_market_cap(ticker[1])
            marketcap_file.write(ticker[1] + ', ' + ticker[0] + ', ' + str(market_cap) + "\n")
        except:
            marketcap_file.write(ticker[1] + ', ' + ticker[0] + ', ' + "NA"+ "\n")
    earnings_file.close()
    marketcap_file.close()






import telegram
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import numpy as np
import requests, json
from pandas.io.json import json_normalize
import json
from lxml import html
import schedule
import datetime
from time import sleep
from tabulate import tabulate
from array import *
bot_token = '1975107197:AAGKn3Ov_XpJugbNwozVhzZ2f6u6OMrQdTE'
group_id = '@chartlink_screenerbot'
bot = telegram.Bot(token=bot_token)
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(executable_path='C:/Users/itsmu/PycharmProjects/Telegraph/chromedriver', options=options)
urlB = 'https://chartink.com/screener/784512ubb'
urlS = 'https://chartink.com/screener/784512lbb'
urlBS = 'https://chartink.com/screener/784512bbutl'
urlSB = 'https://chartink.com/screener/784512bbltu'
driver.get(urlB)
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])
driver.get(urlS)
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[2])
driver.get(urlBS)
driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[3])
driver.get(urlSB)
def get_buy_stocks(urlB):
    driver.switch_to.window(driver.window_handles[0])
    driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/button[1]/i").click()
    form = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="DataTables_Table_0"]')))
    table = pd.read_html(driver.find_element_by_xpath('//*[@id="DataTables_Table_0"]').get_attribute('outerHTML'))
    return table[0]
def get_sell_stocks(urlS):
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/button[1]/i").click()
    form = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="DataTables_Table_0"]')))
    table = pd.read_html(driver.find_element_by_xpath('//*[@id="DataTables_Table_0"]').get_attribute('outerHTML'))
    return table[0]
def get_buy_to_sell_stocks(urlBS):
    driver.switch_to.window(driver.window_handles[2])
    driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/button[1]/i").click()
    form = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="DataTables_Table_0"]')))
    table = pd.read_html(driver.find_element_by_xpath('//*[@id="DataTables_Table_0"]').get_attribute('outerHTML'))
    return table[0]
def get_sell_to_buy_stocks(urlSB):
    driver.switch_to.window(driver.window_handles[3])
    driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[2]/div[1]/button[1]/i").click()
    form = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="DataTables_Table_0"]')))
    table = pd.read_html(driver.find_element_by_xpath('//*[@id="DataTables_Table_0"]').get_attribute('outerHTML'))
    return table[0]
def job():
    s = requests.session()
    data_bal = {
              "api_key":"57687cf0611148f865f6eb4ef804a142",
              "api_secret":"722540a2746ceb18f0f266bc7d4813c0"
            }
    url_bal = 'https://upapi.algomojo.com/1.0/Balance'
    url_hol = 'https://upapi.algomojo.com/1.0/Holdings'
    bal_check = s.post(url_bal, json=data_bal)
    bal = bal_check.json()
    bal_sheet =bal['data']
    bala_sheet=(bal_sheet['equity'])
    balance_sheet=bala_sheet['available_margin']
    buy_stocks=get_buy_stocks(urlB)
    sell_stocks=get_sell_stocks(urlS)
    buy_to_sell_stocks=get_buy_to_sell_stocks(urlBS)
    sell_to_buy_stocks=get_sell_to_buy_stocks(urlSB)
    buy_length=len(list(buy_stocks['Symbol']))
    sell_length=len(list(sell_stocks['Symbol']))
    b2s_length=len(list(buy_to_sell_stocks['Symbol']))
    s2b_length=len(list(sell_to_buy_stocks['Symbol']))
    half_length = (len(list(buy_stocks['Symbol'])) + (len(list(sell_stocks['Symbol']))))
    full_length=len(list(buy_stocks['Symbol']) + list(sell_stocks['Symbol']) + list(buy_to_sell_stocks['Symbol']) + list(sell_to_buy_stocks['Symbol']))
    global portfolio_size
    balance = balance_sheet
    lot_price = balance / half_length
    a, b, c, d, e, f = [], [], [], [], [], []
    for i in range(0, buy_length):
        a.append(str('B'))
    for i in range(0, sell_length):
        b.append(str('S'))
    for i in range(0, b2s_length):
        c.append(str('S'))
    for i in range(0, s2b_length):
        d.append(str('B'))
    for i in range(0, full_length):
        e.append("*")
    for i in range(0, half_length):
        f.append(lot_price)
    g = {
        'Symbol': list(buy_stocks['Symbol']) + list(sell_stocks['Symbol']) + list(buy_to_sell_stocks['Symbol']) + list(sell_to_buy_stocks['Symbol']),
        'Price': list(buy_stocks['Price']) + list(sell_stocks['Price']) + list(buy_to_sell_stocks['Price']) + list(sell_to_buy_stocks['Price']),
        'Shares': e,
        'Order': a + b + c + d,
        '% Chan': list(buy_stocks['% Chg']) + list(sell_stocks['% Chg']) + list(buy_to_sell_stocks['% Chg']) + list(sell_to_buy_stocks['% Chg']),
        'Volume': list(buy_stocks['Volume']) + list(sell_stocks['Volume']) + list(buy_to_sell_stocks['Volume']) + list(sell_to_buy_stocks['Volume']),
    }
    Stocks = pd.DataFrame(g)
    Stocks['Symbol'] = Stocks['Symbol'].replace({'No stocks filtered in the Scan':'N/A'})
    Stocks['Price'] = Stocks['Price'].replace({'No stocks filtered in the Scan':int(0)})
    Stocks['% Chan'] = Stocks['% Chan'].replace({'No stocks filtered in the Scan':'N/A'})
    Stocks['Volume'] = Stocks['Volume'].replace({'No stocks filtered in the Scan':'N/A'})
    h = np.array(list(Stocks['Price']))
    i = np.array(f)
    j = pd.Series(h)
    k = pd.Series(i)
    pd.options.mode.use_inf_as_na = True
    l = (k/j)
    for i in range(0, full_length):
        Stocks.loc[i,'Shares'] = (l[i])
    Stocks['Shares'] = Stocks['Shares'].fillna(0).astype(int)
    m='Symbol Price Shares Order %Chan'
    Stock_MSG = tabulate(Stocks.loc[:,'Symbol':'% Chan'], headers=[m], tablefmt='plain', numalign='right')
    bot.send_message(chat_id=group_id,text=f'{Stock_MSG} \n\nScreened @\n {datetime.datetime.now().strftime("%d/%b/%y || %I:%M:%S %p")}')
    print(Stocks)
    hol_check = s.post(url_hol, json=data_bal)
    holdingss = hol_check.json()
    dp=pd.json_normalize(holdingss)
    dp = dp.drop(dp.columns[[1,2,3,4,5,6,7,10]], axis=1)
    dp = dp[['symbol','avg_price','quantity']]
    dp.columns = ['Symbol','Price','Shares']
    print(dp)
    for x in list(buy_to_sell_stocks['Symbol']):
        for z in dp['Symbol']:
            if x == z:
                list(buy_to_sell_stocks['Shares']).loc[x,'Shares'] = (dp.loc[z,'Shares'])
    for x in list(sell_to_buy_stocks['Symbol']):
        for z in dp['Symbol']:
            if x == z:
                list(sell_to_buy_stocks['Shares']).loc[x,'Shares'] = (dp.loc[z,'Shares'])
    for i in range(0, half_length):
        data_placeorder = {
                                "api_key":"57687cf0611148f865f6eb4ef804a142",
                                "api_secret":"722540a2746ceb18f0f266bc7d4813c0",
                                "data":
                                  {
                                    "stgy_name":"Test Strategy",
                                    "symbol":str(Stocks.loc[i,'Symbol']),
                                    "exchange":"NSE_EQ",
                                    "transaction_type":str(Stocks.loc[i,'Order']),
                                    "duration":"DAY",
                                    "order_type":"MKT",
                                    "quantity":str(Stocks.loc[i,'Shares']),
                                    "disclosed_quantity":"0",
                                    "MktPro":"NA",
                                    "price":"0",
                                    "trigger_price":"0",
                                    "product":"MIS",
                                    "is_amo":"NO"
                                  }
                            }
        url_placeorder = 'https://upapi.algomojo.com/1.0/PlaceOrder'
        req_placeorder = s.post(url_placeorder, json=data_placeorder)
        place_order = req_placeorder.json()      
job()
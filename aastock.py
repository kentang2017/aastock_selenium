from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
broswer = webdriver.Chrome(chrome_options=chrome_options)
html = "http://www.aastocks.com/tc/stocks/quote/detail-quote.aspx?symbol=00001"
broswer.get(html)
stocklist_database = pd.read_excel("strongbuy_20190610.xlsx")
stocklist = list(stocklist_database["股票代號"])
timestr = time.strftime("%Y%m%d")


dataframelist = []
for i in stocklist: #or for i in range(1, 8700) if you don't have a complete stocklist.
    try:
        elem = broswer.find_element_by_xpath("html[1]/body[1]/form[1]/div[4]/div[1]/div[2]/div[2]/div[1]/table[1]/tbody[1]/tr[1]/td[3]/table[1]/tbody[1]/tr[1]/td[1]/input[1]")
        elem.send_keys(i)
        elem.send_keys(Keys.RETURN)
        stockcode = broswer.find_element_by_xpath("/html/body/form/div[4]/div[1]/div[2]/div[2]/div[2]/div[2]")
        name = broswer.find_element_by_xpath("html[1]/body[1]/form[1]/div[4]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/label[1]/span[1]")
        price = broswer.find_element_by_xpath("html[1]/body[1]/form[1]/div[4]/div[3]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/div[3]/div[1]/b[1]/span[1]")
        ten = broswer.find_element_by_xpath("html[1]/body[1]/form[1]/div[4]/div[3]/table[1]/tbody[1]/tr[1]/td[3]/div[1]/table[1]/tbody[1]/tr[1]/td[2]")
        fifty = broswer.find_element_by_xpath("html[1]/body[1]/form[1]/div[4]/div[3]/table[1]/tbody[1]/tr[1]/td[3]/div[1]/table[1]/tbody[1]/tr[2]/td[2]")
        hundred = broswer.find_element_by_xpath("html[1]/body[1]/form[1]/div[4]/div[3]/table[1]/tbody[1]/tr[1]/td[3]/div[1]/table[1]/tbody[1]/tr[3]/td[2]")
        twohundredfifty = broswer.find_element_by_xpath("html[1]/body[1]/form[1]/div[4]/div[3]/table[1]/tbody[1]/tr[1]/td[3]/div[1]/table[1]/tbody[1]/tr[4]/td[2]")
        turnover = broswer.find_element_by_xpath("html[1]/body[1]/form[1]/div[4]/div[3]/div[1]/table[1]/tbody[1]/tr[1]/td[3]/div[1]/div[3]")
        rsiten = broswer.find_element_by_xpath("/html/body/form/div[4]/div[4]/div[4]/table/tbody/tr[1]/td[2]")
        rsifourteen = broswer.find_element_by_xpath("/html/body/form/div[4]/div[4]/div[4]/table/tbody/tr[2]/td[2]")
        rsitwenty = broswer.find_element_by_xpath("/html/body/form/div[4]/div[4]/div[4]/table/tbody/tr[3]/td[2]")
        macd_eigth_seventeen = broswer.find_element_by_xpath("/html/body/form/div[4]/div[4]/div[4]/table/tbody/tr[4]/td[2]")
        macd_twelve_twentyfive = broswer.find_element_by_xpath("/html/body/form/div[4]/div[4]/div[4]/table/tbody/tr[5]/td[2]")
        row = [stockcode.get_attribute('textContent')[3:][:8], name.get_attribute('textContent'), price.get_attribute('textContent'),ten.get_attribute('textContent'), fifty.get_attribute('textContent'),  hundred.get_attribute('textContent'), twohundredfifty.get_attribute('textContent'),  rsiten.get_attribute('textContent'), rsifourteen.get_attribute('textContent'),  rsitwenty.get_attribute('textContent'), macd_eigth_seventeen.get_attribute('textContent'), macd_twelve_twentyfive.get_attribute('textContent'),  turnover.get_attribute('textContent')]
        print(row)
    except (NoSuchElementException, StaleElementReferenceException):
        pass
    eachrow = pd.DataFrame([row], columns = ['股票代號', '公司名稱', '股價', 'SMA 10', 'SMA 50', 'SMA 100', 'SMA 250', 'RSI 10', 'RSI 14', 'RSI 20', 'MACD 8/17', 'MACD 12/25', '成交量' ])
    dataframelist.append(eachrow)
    df = pd.concat(dataframelist)
broswer.quit()

output = df.to_csv("aastockta_"+timestr+".csv")
       

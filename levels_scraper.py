
import glob
from email.mime import base
from xml.etree.ElementInclude import include
from numpy import full
import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import random
import time

def make_web_browser(base_url,track_val,search_val,year_val):
    url = base_url.format(track_val,search_val,year_val,year_val)
    opts = Options()
    opts.add_argument("--headless")
    browser = Firefox(options=opts)
    browser.get(url)
    sleep_time = random.randint(1,4)
    time.sleep(sleep_time)
    print("URL: {}".format(url))

    return browser

def get_data_table(browser):
    sleep_time = random.randint(1,4)
    time.sleep(sleep_time)

    col_names = ['Company','Location | Date', 'Level Name', 'Tag', 'At Company / Total', 'Total Compensation', 'Base | Stock (/yr) | Bonus']

    table_rows_html = browser.find_elements(By.XPATH,'//*[@id="compTable"]/tbody/tr')
    table_rows = []
    for row in table_rows_html:
        try:
            # company = WebDriverWait(browser, 1).until(EC.visibility_of_element_located((By.XPATH,'./td[2]/span/a'))).get_attribute("innertext")
            company = row.find_element(By.XPATH,'./td[2]/span/a').text
        except:
            company = ''
        try:
            # loc_date = WebDriverWait(browser, 1).until(EC.visibility_of_element_located((By.XPATH,'./td[2]/p/span'))).get_attribute("innertext")
            loc_date = row.find_element(By.XPATH,'./td[2]/p/span').text
        except:
            loc_date = ''
        try:
            # level_name = WebDriverWait(browser, 1).until(EC.visibility_of_element_located((By.XPATH,'./td[3]/span'))).get_attribute("innertext")
            level_name = row.find_element(By.XPATH,'./td[3]/span').text
        except:
            level_name = ''
        try:
            # tag_name = WebDriverWait(browser, 1).until(EC.visibility_of_element_located((By.XPATH,'./td[3]/p/span'))).get_attribute("innertext")
            tag_name = row.find_element(By.XPATH,'./td[3]/p/span').text
        except:
            tag_name = ''
        try:
            # yoe_val = WebDriverWait(browser, 1).until(EC.visibility_of_element_located((By.XPATH,'./td[4]/span'))).get_attribute("innertext")
            yoe_val = row.find_element(By.XPATH,'./td[4]/span').text
        except:
            yoe_val = ''
        try:
            # tot_comp = WebDriverWait(browser, 1).until(EC.visibility_of_element_located((By.XPATH,'./td[5]/div/div/span'))).get_attribute("innertext")
            tot_comp = row.find_element(By.XPATH,'./td[5]/div/div/span').text
        except:
            tot_comp = ''
        try:
            # comp_breakdown = WebDriverWait(browser, 1).until(EC.visibility_of_element_located((By.XPATH,'./td[5]/div/div/p/span'))).get_attribute("innertext")
            comp_breakdown = row.find_element(By.XPATH,'./td[5]/div/div/p/span').text
        except:
            comp_breakdown = ''

        table_row = [company,loc_date,level_name,tag_name,yoe_val,tot_comp,comp_breakdown]
        table_rows.append(table_row)

        # print(table_row)

    df = pd.DataFrame(table_rows,columns=col_names)

    try:
        df[['Location', 'Date']] = df['Location | Date'].str.split('|', 1, expand=True)
        df.drop('Location | Date',inplace=True,axis=1)
    except:
        print('Location | Date')
        print(df['Location | Date'])
        print(table_rows)
        exit()

    try:
        df[['YOE At Company', 'YOE Total']] = df['At Company / Total'].str.split('/', 1, expand=True)
        df.drop('At Company / Total',inplace=True,axis=1)
    except:
        print('At Company / Total')
        print(df['At Company / Total'])
        print(table_rows)
        exit()

    try:
        if not df['Base | Stock (/yr) | Bonus'].empty:
            df['Base | Stock (/yr) | Bonus'] = df['Base | Stock (/yr) | Bonus'].str.replace('K','000')
            df[['Base Comp', 'Stock Comp', 'Bonus Comp']] = df['Base | Stock (/yr) | Bonus'].str.split('|', 2, expand=True)
        else:
            df['Base Comp'] = ''
            df['Stock Comp'] = ''
            df['Bonus Comp'] = ''
        df.drop('Base | Stock (/yr) | Bonus',inplace=True,axis=1)
    except:
        print('Base | Stock (/yr) | Bonus')
        print(df['Base | Stock (/yr) | Bonus'])
        print(table_rows)
        exit()

    df['Total Compensation'] = df['Total Compensation'].str.replace('$','',regex=False)
    df['Total Compensation'] = df['Total Compensation'].str.replace(',','',regex=False)

    df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)
    

    return df

def get_next_page(browser):
    next_button = browser.find_element(By.XPATH,'/html/body/div[2]/div/div[4]/div[4]/div/div[1]/div[1]/div[3]/div[2]/ul/li[last()]/a')
    browser_wait = WebDriverWait(browser, 3).until(EC.element_to_be_clickable(next_button))
    browser_wait.click()

def get_data_set(track_val,company_name,yoe):
    base_url = 'https://www.levels.fyi/comp.html?track={}&region=807,819,501,803,506,602,635,751&search={}&yoestart={}&yoeend={}'

    print('*******************')
    print('Company: {}'.format(company_name))
    print('Track: {}'.format(track_val))
    print('Experience: {}'.format(yoe))

    num_pages_xpath = '/html/body/div[2]/div/div[4]/div[4]/div/div[1]/div[1]/div[3]/div[2]/ul/li[last()-1]/a'

    browser = make_web_browser(base_url,track_val,search_val,year_val)
    num_pages = browser.find_element(By.XPATH,num_pages_xpath).text
    if not num_pages:
        print('{}'.format('No Data Present'))
        browser.quit()
        return pd.DataFrame()
    else:
        num_pages = int(browser.find_element(By.XPATH,num_pages_xpath).text)

        full_table = pd.DataFrame()

        

        for i in range(0,num_pages):
            
            print('Page: {}/{}'.format(i,num_pages))

            try:
                df = get_data_table(browser)
                full_table = pd.concat([full_table,df])
            except:
                continue

            get_next_page(browser)
        browser.quit()
        return full_table


track_val_list = ['Data%20Scientist','Software%20Engineer','Technical%20Program%20Manager','Product%20Manager','Sales','Recruiter','Software%20Engineering%20Manager']
search_val = ''
year_val_list = range(0,21)
num_files = len(glob.glob("./data/Track"))
while num_files < len(track_val_list) * len(year_val_list):
    try:
        num_files = len(glob.glob("./data/Track"))
        file_list = []
        for track_val in track_val_list:
            for year_val in year_val_list:

                file_list = glob.glob("./data/Track{}_YOE{}.csv".format(track_val,year_val))

                if len(file_list) == 0:
                    dataset = pd.DataFrame()
                    dataset = get_data_set(track_val,search_val,year_val)
                    dataset.to_csv("./data/Track{}_YOE{}.csv".format(track_val,year_val),index=False)
    except:
        continue




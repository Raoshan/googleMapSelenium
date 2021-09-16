import os
import xlrd
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
options = Options()
dataFloderPath = os.path.join('C:/Users/RDATS/Desktop/Projects/Data')
fulPath = os.path.join('C:/Users/RDATS/Desktop/Projects/Resturents')
siteKeyword = "restaurants in new york city"
workbook = xlrd.open_workbook("C:\\Users\\RDATS\\Desktop\\Projects\\keyWord\\key.xlsx", "rb")
sheet = workbook.sheet_by_name("UL")
sheet.cell_value(0, 0)
for col in range(sheet.ncols):
    keyword = sheet.cell_value(0, col)
    driver = webdriver.Chrome(executable_path=r"C:\\Users\\RDATS\\Desktop\\Projects\\driver\\chromedriver.exe")
    #driver.maximize_window()
    def GetDetailsOfItem(URL):
        driver.get(URL)
        time.sleep(5)
        try:
            time.sleep(3)
            RestaurantName = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/h1/span[1]').text
            print(RestaurantName)
        except:
            RestaurantName = ""
            print("RestaurantName")
        try:
           Address = driver.find_element_by_xpath("//*[@id='pane']/div/div[1]/div/div/div[9]/div[1]/button/div[1]/div[2]/div[1]").text
           print(Address)
        except:
           Address = ""
           print("Address")
        try:
            PhoneNumber = driver.find_element_by_class_name("QSFF4-text gm2-body-2").find_element_by_css_selector("div[jsan='7.QSFF4-text,7.gm2-body-2']").text
            print(PhoneNumber)

        except:
            PhoneNumber = " "
            print("PhoneNumber")
        try:
            Photos = driver.find_element_by_xpath("//*[@id='pane']/div/div[1]/div/div/div[1]/div[1]/button/img").get_attribute('src')
            print(Photos)
        except:
            Photos = ""
            print("Photos")

        try:
           star = driver.find_element_by_xpath("//*[@id='pane']/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span/span/span").text
           views = driver.find_element_by_xpath("//*[@id='pane']/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/span[1]/span/span[1]/span[2]/span[1]/button").text
           Reviews = star + " *, and " + views
           print(Reviews)
        except:
          Reviews = ""
          print("Reviews")
        try:
            site = driver.find_element_by_xpath("//*[@id='pane']/div/div[1]/div/div/div[9]/div[5]/button/div[1]/div[2]/div[1]").text
            Website = "www."+site
            print(Website)

        except:
            Website = ""
            print("Website")

        return pd.Series([RestaurantName, Address, PhoneNumber, Photos, Reviews, Website])
    driver.get("https://www.google.com/maps/")
    time.sleep(20)
    driver.find_element(By.ID, "searchboxinput").send_keys(siteKeyword, Keys.ENTER)
    time.sleep(20)
    # totalnoofitemsonsite = 22
    # if totalnoofitemsonsite == 0:
    #     loops = 0
    # else:
    #     loops = int(totalnoofitemsonsite / 22) + 1
    # print("loops=", loops)
    strss = driver.find_elements_by_css_selector("div[class='V0h1Ob-haAclf OPZbO-KE6vqe o0s21d-HiaYvf']")
    # print("lenght=", len(strss))
    loops = 1
    data = []
    for lo in range(loops):
        actions = ActionChains(driver)
        time.sleep(5)
        for prod in driver.find_elements_by_css_selector("div[class='V0h1Ob-haAclf OPZbO-KE6vqe o0s21d-HiaYvf']"):
            actions.move_to_element(prod).perform()
            try:
                URL = prod.find_element_by_css_selector("a[class='a4gq8e-aVTXAb-haAclf-jRmmHf-hSRGPd']").get_attribute('href')
                print(URL)
            except:
                URL = ""
                print(URL)

            data.append([URL])
        try:
            actions = ActionChains(driver)
            #actions.move_to_element(driver.find_element_by_xpath('//*[@id="ppdPk-Ej1Yeb-LgbsSe-tJiF1e"]/img', (str(lo+2))).perform()
            driver.find_element_by_xpath('//*[@id="ppdPk-Ej1Yeb-LgbsSe-tJiF1e"]/img').click()
        except:
            pass
    if loops == 0:
        driver.close()
        pass
    else:
        datadf = pd.DataFrame(data, columns=['URL'])
        datadf.to_csv(os.path.join(dataFloderPath, 'Map' + siteKeyword + '.csv'), index=False)
        if len(datadf) == 0:
            driver.close()
        else:
            datadf[['RestaurantName', 'Photos', 'Address', 'Reviews', 'PhoneNumber', 'Website']] = datadf[['URL']].apply(lambda x: GetDetailsOfItem(x[0]), axis=1)
            datadf = datadf[['RestaurantName', 'Photos', 'Address', 'Reviews', 'PhoneNumber', 'Website']]
            datadf.to_csv(os.path.join(fulPath, 'Details' + siteKeyword + '.csv'), index=False)
            driver.close()
            print("Completed...........")
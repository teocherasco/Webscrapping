import time
import numpy as np
from selenium import webdriver
import pandas as pd
import openpyxl
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

pinn_final_1 = []
pinn_final_X = []
pinn_final_2 = []
l1 = []
lX = []
l2 = []
loc_names = []
aw_names = []
times = []
date = []
null_col = []
loc_name = None
aw_name = None
time_m = None

driver = webdriver.Chrome("C:\\Users\\PC\\Downloads\\chromedriver_win32\\chromedriver.exe")

url = "https://www.oddsportal.com/football/england/premier-league/"

driver.get(url)
WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler"))).click()

# -----------------------------------------------------------------------------------------------------------

div_matches = driver.find_element("xpath", '//*[@id="app"]/div/div[1]/div/main/div[2]/div[5]')

elements = div_matches.find_elements(by=By.CSS_SELECTOR,
                                     value="div[class='flex items-center gap-1 my-1 align-center w-[100%]']")

for element in range(len(elements)):
    try:
        div_match = driver.find_element("xpath", '//*[@id="app"]/div/div[1]/div/main/div[2]/div[5]')

        loc_name = (div_match.find_elements(by=By.CSS_SELECTOR,
                                            value="div[class='relative block truncate whitespace-nowrap group-hover:underline next-m:!ml-auto text-[#000000]']")[element])

        aw_name = (div_match.find_elements(by=By.CSS_SELECTOR,
                                           value="div[class='relative block truncate whitespace-nowrap group-hover:underline text-[#000000]']")[element])

        time_m = (div_match.find_elements(by=By.CSS_SELECTOR, value="p[class='whitespace-nowrap']")[element])

        driver.execute_script("arguments[0].scrollIntoView();", loc_name)
        time.sleep(0.5)

        loc_name = loc_name.text
        aw_name = aw_name.text
        time_m = time_m.text
        loc_names.append(loc_name)
        aw_names.append(aw_name)
        times.append(time_m)

        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='flex flex-col px-3 text-sm max-mm:px-0']")))

        div_matches = driver.find_element(by=By.CSS_SELECTOR, value="div[class='flex flex-col px-3 text-sm max-mm:px-0']")
        el = div_matches.find_elements(by=By.CSS_SELECTOR,
                                       value="div[class='flex items-center gap-1 my-1 align-center w-[100%]']")[element]
        driver.execute_script("arguments[0].scrollIntoView();", el)
        time.sleep(0.5)

        el.click()
        time.sleep(1)

        bets_div = driver.find_element(by=By.CSS_SELECTOR, value="div[class='flex flex-col']")

        time.sleep(1)

        pX12 = []
        aX12 = []

        for i in range(3):
            pinn_el = bets_div.find_element(by=By.XPATH, value=f"//*[text()='Pinnacle']//following::p[{i + 1}]")
            pX12.append(pinn_el.text)

        bets_div = driver.find_element(by=By.CSS_SELECTOR, value="div[class='flex flex-col']")

        for i in range(3):
            pinn_ela = bets_div.find_element(by=By.XPATH, value=f"//*[text()='Pinnacle']//following::a[{i + 3}]")
            aX12.append(pinn_ela.text)

        if pX12[0] == "":
            pinn_final_1 = aX12[0]
            pinn_final_X = aX12[1]
            pinn_final_2 = aX12[2]
        else:
            pinn_final_1 = pX12[0]
            pinn_final_X = pX12[1]
            pinn_final_2 = pX12[2]

    except NoSuchElementException:
        pinn_final_1 = "-"
        pinn_final_X = "-"
        pinn_final_2 = "-"

    l1.append(pinn_final_1)
    lX.append(pinn_final_X)
    l2.append(pinn_final_2)

    driver.execute_script("window.history.go(-1)")
    time.sleep(3)

driver.quit()

arrays = [times, loc_names, aw_names, l1, lX, l2]
max_len = max(len(lst) for lst in arrays)

for i, lst in enumerate(arrays):
    if len(lst) < max_len:
        arrays[i] += [np.nan] * (max_len - len(lst))

data = {"Time": times, "Local Team": loc_names, "Away team": aw_names, "1": l1, "X": lX, "2": l2}
df = pd.DataFrame(data)
df.replace("Unibet", "-", inplace=True)
df.to_excel("Match_odds.xlsx", index=False)

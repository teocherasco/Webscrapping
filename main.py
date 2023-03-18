import time
from selenium import webdriver
import pandas as pd
import openpyxl
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

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

driver = webdriver.Chrome("C:\\Users\\PC\\Downloads\\chromedriver_win32\\chromedriver.exe")

url = "https://www.oddsportal.com/football/england/premier-league/"

driver.get(url)
WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler"))).click()

# -----------------------------------------------------------------------------------------------------------

div_match = driver.find_element("xpath", '//*[@id="app"]/div/div[1]/div/main/div[2]/div[5]')
matches = div_match.find_elements(by=By.CSS_SELECTOR, value="div[class='flex items-center gap-1 my-1 align-center w-[100%]']")

for element in range(len(matches)):
    div_matches = driver.find_element("xpath", '//*[@id="app"]/div/div[1]/div/main/div[2]/div[5]')
    elements = div_matches.find_elements("xpath", "./*")

    loc_name = div_matches.find_elements(by=By.CSS_SELECTOR,
                                         value="div[class='relative block truncate whitespace-nowrap group-hover:underline next-m:!ml-auto text-[#000000]']")[element]

    aw_name = div_matches.find_elements(by=By.CSS_SELECTOR,
                                        value="div[class='relative block truncate whitespace-nowrap group-hover:underline text-[#000000]']")[element]

    time_m = div_matches.find_elements(by=By.CSS_SELECTOR, value="p[class='whitespace-nowrap']")[element]

    driver.execute_script("arguments[0].scrollIntoView();", loc_name)
    time.sleep(0.5)

    loc_names.append(loc_name.text)
    aw_names.append(aw_name.text)
    times.append(time_m.text)

# -----------------------------------------------------------------------------------------------------------

div_matches = driver.find_element("xpath", '//*[@id="app"]/div/div[1]/div/main/div[2]/div[5]')

elements = div_matches.find_elements(by=By.CSS_SELECTOR,
                                     value="div[class='flex items-center gap-1 my-1 align-center w-[100%]']")

for element in range(len(elements)):
    try:
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

        l1.append(pinn_final_1)
        lX.append(pinn_final_X)
        l2.append(pinn_final_2)

    except NoSuchElementException:
        pass

    driver.execute_script("window.history.go(-1)")
    time.sleep(3)

driver.quit()

data = {"Time": times, "Local Team": loc_names, "Away team": aw_names, "1": l1, "X": lX, "2": l2}
df = pd.DataFrame(data)
df.replace("Unibet", "-", inplace=True)
df.to_excel("Odds_1X2.xlsx", index=False)

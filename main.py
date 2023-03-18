import time
from selenium import webdriver
import pandas as pd
import openpyxl
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pinn_final_1 = []
pinn_final_X = []
pinn_final_2 = []
l1 = []
lX = []
l2 = []

driver = webdriver.Chrome("C:\\Users\\PC\\Downloads\\chromedriver_win32\\chromedriver.exe")

url = "https://www.oddsportal.com/football/england/premier-league/"

driver.get(url)
WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler"))).click()

div_matches = driver.find_element("xpath", '//*[@id="app"]/div/div[1]/div/main/div[2]/div[5]')

elements = div_matches.find_elements(by=By.CSS_SELECTOR,
                                     value="div[class='flex items-center gap-1 my-1 align-center w-[100%]']")

for element in range(len(elements)):
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
        pinn_el = bets_div.find_element(by=By.XPATH, value=f"//*[text()='Pinnacle']//following::p[{i + 2}]")
        pinn_ela = bets_div.find_element(by=By.XPATH, value=f"//*[text()='Pinnacle']//following::a[{i + 3}]")

        pX12.append(pinn_el.text)
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

    driver.execute_script("window.history.go(-1)")
    time.sleep(3)

driver.quit()

data = {"1": l1, "X": lX, "2": l2}
df = pd.DataFrame(data)
df.replace("Unibet", "-", inplace=True)

df.to_excel("Odds_1X2.xlsx", index=False)

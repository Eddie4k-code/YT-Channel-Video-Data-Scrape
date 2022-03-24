from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import pandas as pd

chrome_driver_path = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get('https://www.youtube.com/c/CHANNEL_NAME/videos')

videos = driver.find_elements(By.CSS_SELECTOR, '#video-title')

df = pd.DataFrame()

title = []
view_list = []
like_list = []
upload_date_list = []

#Grab Titles
headlines = driver.find_elements(By.CSS_SELECTOR, '#video-title')

for e in headlines:
    title.append(e.text)

df['Titles'] = title






#Click Each Video
for i in videos:
    i.click()

    wait = WebDriverWait(driver, 10)
    time.sleep(2)

    '''
    Find View Count
    '''
    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ytd-video-view-count-renderer'))).text

    time.sleep(3)

    #Split the word views from the actual integer
    views = element.split()
    view_list.append(views[0])

    '''
    Find Likes
    '''
    like_element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div[1]/ytd-toggle-button-renderer[1]/a/yt-formatted-string'))).text
    time.sleep(5)
    like_list.append(like_element)

    '''
    Upload Date
    '''
    upload_date = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#info-strings yt-formatted-string'))).text
    time.sleep(2)
    upload_date_list.append(upload_date)




    time.sleep(5)
    driver.back()

df['Views'] = view_list
df['Likes'] = like_list
df['Upload Date'] = upload_date_list


# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('VideoData.xlsx')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')



# Close the Pandas Excel writer and output the Excel file.

writer.save()

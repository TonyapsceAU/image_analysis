import os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service

service = Service(executable_path = "geckodriver")
driver = webdriver.Firefox(service = service)
driver.set_window_position(0, 0)
driver.set_window_size(1284, 1044)

driver.get("file:" + os.getcwd() + "/website.v3/tfJS.html")
upload = driver.find_element('id', "image-upload")
upload.send_keys(os.getcwd() + "\\Training_data\\test\\japanese.jpg")
# upload.send_keys(r"D:\CodeServer\image_analysis\Training_data\test\japanese.jpg")
# driver.implicitly_wait(10)
while len(driver.find_element('id', "label-container").text) == 0:
    time.sleep(0.1)
print(driver.find_element('id', "label-container").text)

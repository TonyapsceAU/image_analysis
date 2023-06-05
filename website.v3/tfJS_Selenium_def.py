import os, time
from selenium import webdriver
# from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

def tfJS(image_path):
    opts = Options()
    opts.add_argument("-headless")
    # assert opts.headless
    driver = webdriver.Firefox(options=opts, service = Service(executable_path = "geckodriver"))
    # os.system("cls")
    driver.set_window_position(0, 0)
    driver.set_window_size(1284, 1044)

    driver.get("file:" + os.getcwd() + "/website.v3/tfJS.html")
    driver.find_element('id', "image-upload").send_keys(os.getcwd() + "\\" + image_path.replace("/", "\\")) #input different image path here

    while len(driver.find_element('id', "label-container").text) == 0:
        time.sleep(0.1)
    class_info = driver.find_element('id', "label-container").text
    print(class_info) #Class information output
    return class_info
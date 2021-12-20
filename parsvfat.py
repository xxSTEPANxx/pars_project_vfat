from selenium import webdriver, common
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver.chrome.service import Service
import time
import os
import pars_Nets_and_projects
import config

from json import dump, load

from selenium.webdriver.support.ui import WebDriverWait


def chek_load(driver, project):
    c = 0
    try:
        while c < 60:
            if driver.find_element_by_class_name('loader--1').get_attribute('style') == 'display: none;':
                break
            if 'Oops something went wrong. Try refreshing the page' in driver.find_element_by_id('log').text:
                break
            time.sleep(1)
            c += 1
    except common.exceptions.NoSuchElementException:
        print(project)

def wait_selenium(driver, param, looking_for):
    wait = WebDriverWait(driver, 10, poll_frequency=1,
                         ignored_exceptions=[ElementNotVisibleException,
                                             ElementNotSelectableException,
                                             NoSuchElementException])
    if param == 0:
        wait.until(EC.element_to_be_clickable((By.XPATH, looking_for)))
    if param == 1:
        wait.until(EC.element_to_be_clickable((By.TAG_NAME, looking_for)))

def open_chrom_with_metamask():
    s = Service(r'C:\Users\ASER\Documents\GitHub\pars_project_vfat\Chrom\chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_extension(r'Chrom/MetaMask_v10.0.2.crx')
    driver = webdriver.Chrome(service=s, options=options)
    driver = metamask_connect(driver)
    driver.switch_to.window(driver.window_handles[1])
    return driver

def metamask_connect(driver):
    seed = config.seed
    parol = config.parol
    driver.switch_to.window(driver.window_handles[0])

    wait_selenium(driver, 0, '//*[@id="app-content"]/div/div[3]/div/div/div/button')
    driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div/div/button').click()


    wait_selenium(driver, 0, '//*[@id="app-content"]/div/div[3]/div/div/div[2]/div/div[2]/div[1]/button')
    driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div/div[2]/div/div[2]/div[1]/button').click()


    wait_selenium(driver, 0,
                  '//*[@id="app-content"]/div/div[3]/div/div/div/div[5]/div[1]/footer/button[2]')
    driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div/div/div[5]/div[1]/foo'
                                  'ter/button[2]').click()

    wait_selenium(driver, 0, '//*[@id="app-content"]/div/div[3]/div/div/form/div[4]/div[2]/div')
    driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div'
                                 '/form/div[4]/div[1]/div/input').send_keys(seed)
    driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div/form/div[4]/div[2]/div').click()
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(parol)
    driver.find_element(By.XPATH, '//*[@id="confirm-password"]').send_keys(parol)
    driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div/form/div[7]/div').click()
    driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div/form/button').click()

    wait_selenium(driver, 0, '//*[@id="app-content"]/div/div[3]/div/div/button')
    driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div/button').click()
    driver.find_element(By.XPATH, '//*[@id="popover-content"]/div/div/section/header/div/button').click()
    return driver


def connect_vfat(driver):
    url = 'https://vfat.tools/alcx/'
    driver.get(url)
    driver.find_element(By.XPATH, '//*[@id="connect_wallet_button"]').click()
    driver.find_element(By.XPATH, '//*[@id="WEB3_CONNECT_MODAL_ID"]/div/div/div[2]/div[1]/div/div[2]').click()
    driver.switch_to.window(driver.window_handles[0])
    driver.refresh()
    wait_selenium(driver, 0, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[4]/div[2]/button[2]')
    driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[4]/div[2]/button[2]').click()
    driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/footer/button[2]').click()
    driver.switch_to.window(driver.window_handles[1])


def get_all_txt(driver, nets):
    with open(r'all_json_files/all_projects_vfat.json', 'r') as file:
        all_projects = load(file)
    for net in list(all_projects)[1:]:
        if len(all_projects[net]) < 1 or net in config.blacklist[nets]:
            continue

        start_project(driver, net, all_projects)

def start_project(driver, net, all_projects, number=0):

    if len(all_projects[net]) >= number + 1:
        if net != 'All':
            switch_network(driver, net, all_projects)

        if not os.path.exists(fr'txt_files_vfat\{net}'):
            os.mkdir(fr'txt_files_vfat\{net}')
        i = number
        for project in all_projects[net][number:]:
            i += 1
            if project == 'https://vfat.tools/percent':
                continue
            driver.get(project)
            chek_load(driver, project)
            with open(fr'txt_files_vfat/{net}/{str(i)}.txt', 'w', encoding='utf-8') as file:
                file.write(driver.find_element(By.XPATH, '//*[@id="log"]').text)
    else:
        print('oops')

def switch_network(driver, net, all_projects):

    url = all_projects[net][1]
    driver.get(url)
    chek_load(driver, url)
    try:
        driver.find_element(By.XPATH, '//*[@id="connect_wallet_button"]').click()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)
        driver.refresh()
        wait_selenium(driver, 1, 'button')
        driver.find_elements(By.TAG_NAME, "button")[1].click()
        driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/button[2]').click()
        driver.switch_to.window(driver.window_handles[1])
    except common.exceptions.NoSuchElementException:
        print(url, 'switch')


def get_nets_and_projects(driver):
    pars_Nets_and_projects.get_all_projects(driver)



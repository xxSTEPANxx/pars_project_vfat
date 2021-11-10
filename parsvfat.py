from selenium import webdriver, common
import time
import os
import Pars_Nets_and_projects
import config

from json import dump, load

from selenium.webdriver.support.ui import WebDriverWait


def metamask_connect(driver):
    seed = config.seed
    parol = config.parol
    driver.switch_to.window(driver.window_handles[0])

    chek_click(driver, 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#initialize/welcome')
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/div/button').click()

    chek_click(driver, 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#initialize/select-action')
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/div[2]/div/div[2]/div[1]/button').click()

    chek_click(driver, 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#initialize/metametrics-opt-in')
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/div/div[5]/div[1]/foo'
                                  'ter/button[2]').click()

    chek_click(driver, 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.'
               'html#initialize/create-password/import-with-seed-phrase')
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div'
                                 '/form/div[4]/div[1]/div/input').send_keys(seed)
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/form/div[4]/div[2]/div').click()
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(parol)
    driver.find_element_by_xpath('//*[@id="confirm-password"]').send_keys(parol)
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/form/div[7]/div').click()
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/form/button').click()

    chek_click(driver, 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#initialize/end-of-flow')
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/button').click()
    driver.find_element_by_xpath('//*[@id="popover-content"]/div/div/section/header/div/button').click()
    return driver


def chek_click(driver, url):
    wait = WebDriverWait(driver, 10)
    wait.until(lambda driver: driver.current_url == url)

def chek_load(driver, project):
    c = 0
    try:
        while c < 60:
            if driver.find_element_by_class_name('loader--1').get_attribute('style') == 'display: none;':
                break
            if 'Oops something went wrong. Try refreshing the page' in driver.find_element_by_id('log').text:
                break
            time.sleep(0.5)
            c += 1
    except common.exceptions.NoSuchElementException:
        print(project)

def connect_vfat(driver):
    url = 'https://vfat.tools/alcx/'
    driver.get(url)
    driver.find_element_by_xpath('//*[@id="connect_wallet_button"]').click()
    driver.find_element_by_xpath('//*[@id="WEB3_CONNECT_MODAL_ID"]/div/div/div[2]/div[1]/div/div[2]').click()
    driver.switch_to.window(driver.window_handles[0])
    driver.refresh()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[2]/div[4]/div[2]/button[2]').click()
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/footer/button[2]').click()
    # time.sleep(2)
    # driver.find_element_by_xpath('//*[@id="popover-content"]/div/div/section/header/div/button').click()
    driver.switch_to.window(driver.window_handles[1])

def get_net(driver, all_projects, net_name):
    url = all_projects[net_name][1][-1]
    driver.get(url)
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="connect_wallet_button"]').click()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1.5)
    driver.refresh()
    time.sleep(1.5)
    # driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/button[2]').click()
    driver.find_elements_by_tag_name('button')[1].click()
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/button[2]').click()
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(1.5)

def start_project(driver, net, all_projects, number=0):
    switch_network(driver, net, all_projects)
    if len(all_projects[net]) >= number + 1:
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
                file.write(driver.find_element_by_xpath('//*[@id="log"]').text)
    else:
        print('oops')

def switch_network(driver, net, all_projects):
    url = all_projects[net][0]
    driver.get(url)
    chek_load(driver, url)
    # try:
    driver.find_element_by_xpath('//*[@id="connect_wallet_button"]').click()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1.5)
    driver.refresh()
    time.sleep(1.5)
    driver.find_elements_by_tag_name('button')[1].click()
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/button[2]').click()
    driver.switch_to.window(driver.window_handles[1])
    # except common.exceptions.NoSuchElementException:
    #     print(url, 'switch')

def open_chrom_with_metamask():
    options = webdriver.ChromeOptions()
    options.add_extension(r'Chrom/MetaMask_v10.0.2.crx')
    driver = webdriver.Chrome(options=options)
    driver = metamask_connect(driver)
    driver.switch_to.window(driver.window_handles[1])
    return driver

def get_nets_and_projects(driver):
    Pars_Nets_and_projects.get_all_projects(driver)



def get_all_txt(driver):
    with open(r'D:\PycharmProjects\Pars_project\pars_project_vfat\all_json_files\all_projects_vfat.json', 'r') as file:
        all_projects = load(file)
    for net in list(all_projects)[4:]:
        if net in config.blacklist:
            continue
        start_project(driver, net, all_projects)

# start_project(driver, 'ARBITRUM')

# # driver.quit()

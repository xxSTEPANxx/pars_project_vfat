from selenium import webdriver
import time
from json import dump, load

from selenium.webdriver.support.ui import WebDriverWait


def metamask_connect(brawser):
    seed = 'word caution limit element all clap swear program connect brief dirt job'
    parol = 'rjkdbh21'
    # options = webdriver.ChromeOptions()
    # options.add_extension('MetaMask_v10.0.2.crx')
    #
    # driver = webdriver.Chrome(options=options)
    brawser.switch_to.window(brawser.window_handles[0])

    chek_click('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#initialize/welcome')
    brawser.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/div/button').click()

    chek_click('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#initialize/select-action')
    brawser.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/div[2]/div/div[2]/div[1]/button').click()

    chek_click('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#initialize/metametrics-opt-in')
    brawser.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/div/div[5]/div[1]/foo'
                                  'ter/button[2]').click()

    chek_click('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.'
               'html#initialize/create-password/import-with-seed-phrase')
    brawser.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div'
                                 '/form/div[4]/div[1]/div/input').send_keys(seed)
    brawser.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/form/div[4]/div[2]/div').click()
    brawser.find_element_by_xpath('//*[@id="password"]').send_keys(parol)
    brawser.find_element_by_xpath('//*[@id="confirm-password"]').send_keys(parol)
    brawser.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/form/div[7]/div').click()
    brawser.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/form/button').click()

    chek_click('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#initialize/end-of-flow')
    brawser.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/button').click()
    brawser.find_element_by_xpath('//*[@id="popover-content"]/div/div/section/header/div/button').click()
    return brawser


def chek_click(url):
    global driver
    wait = WebDriverWait(driver, 10)
    wait.until(lambda driver: driver.current_url == url)

def chek_load():
    c = 0
    while c < 60:
        if driver.find_element_by_class_name('loader--1').get_attribute('style') == 'display: none;':
            print(c)
            break
        if 'Oops something went wrong. Try refreshing the page' in driver.find_element_by_id('log').text:
            print('yes')
            break
        print(c)
        time.sleep(1)
        c += 1


def connect_vfat():
    url = 'https://vfat.tools/alcx/'
    driver.get(url)
    driver.find_element_by_xpath('//*[@id="connect_wallet_button"]').click()
    driver.find_element_by_xpath('//*[@id="WEB3_CONNECT_MODAL_ID"]/div/div/div[2]/div[1]/div/div[2]').click()
    driver.switch_to.window(driver.window_handles[0])
    driver.refresh()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[2]/div[4]/div[2]/button[2]').click()
    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div[2]/footer/button[2]').click()
    # time.sleep(2)
    # driver.find_element_by_xpath('//*[@id="popover-content"]/div/div/section/header/div/button').click()
    driver.switch_to.window(driver.window_handles[1])

def get_net(all_projects, net_name):
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


options = webdriver.ChromeOptions()
options.add_extension('MetaMask_v10.0.2.crx')
driver = webdriver.Chrome(options=options)

driver = metamask_connect(driver)

driver.switch_to.window(driver.window_handles[1])

connect_vfat()

driver.get('https://vfat.tools/cover/')
chek_load()

with open('../Selenium projects/f.txt', 'w', encoding='utf-8') as file:
    file.write(driver.find_element_by_xpath('//*[@id="log"]').text)

# print(driver.find_element_by_class_name('loader--1').get_attribute('style'), 'hi')
# print(type(driver.find_element_by_class_name('loader--1').get_attribute('style')))

with open('../Selenium projects/all_projects_vfat.json', 'r') as file:
    all_projects = load(file)
with open('../Selenium projects/all_nets_vfat.jason', 'r') as file:
    all_nets = load(file)

driver.get('https://vfat.tools/all/')
i = 0
for _ in all_projects['All'][1]:
    i += 1
    driver.get(_)
    chek_load()
    with open('txt_files_vfat/' + str(i) + '.txt', 'w',  encoding='utf-8') as file:
        file.write(driver.find_element_by_xpath('//*[@id="log"]').text)

print('YESSSS')
time.sleep(4)
# driver.quit()

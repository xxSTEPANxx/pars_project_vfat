from selenium import webdriver
from selenium.webdriver.common.by import By
from json import dump, load

def get_all_projects(driver):
    nets_to_find = driver.find_element(By.XPATH, '/html/body/div[3]')
    # nets_to_find = driver.find_element_by_xpath('/html/body/div[3]')
    net_names = nets_to_find.text.split(' - ')[1:]

    links_10 = driver.find_elements(By.TAG_NAME, 'a')

    net_links = [links_10[i].get_attribute('href') for i in range(2, len(net_names) + 2)]

    all_projects_all_nets = {}
    for i in range(len(net_names)):
        url = net_links[i]
        driver.get(url)

        b = driver.find_element(By.XPATH, '//*[@id="log"]')
        b = (b.find_elements(By.LINK_TEXT, 'Various'))
        # b = (b.find_elements_by_link_text('Various'))
        b = [i.get_attribute('href') for i in b]
        all_projects_all_nets[net_names[i]] = b

    with open(r'all_json_files/all_projects_vfat.json', 'w') as file:
        dump(all_projects_all_nets, file, indent=4)


import time
from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://keizaiclub.com/category/%e8%bf%91%e6%9c%aa%e6%9d%a5%e4%ba%88%e6%b8%ac/')

while driver.find_element_by_css_selector('#load_post .next') != 0:
  btn_nuxt = driver.find_element_by_css_selector('#load_post .next')
  btn_nuxt.click()
  time.sleep(5)
time.sleep(5)
driver.quit()
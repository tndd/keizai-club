import time
from selenium import webdriver

driver = webdriver.Chrome()

url_base = 'https://keizaiclub.com/category/%e8%bf%91%e6%9c%aa%e6%9d%a5%e4%ba%88%e6%b8%ac/page/'
page_number = 57

while True:
  url = f'{url_base}{page_number}/'
  driver.get(url)
  time.sleep(3)
  if driver.title != '近未来予測に関する記事一覧':
    break
  articles = driver.find_elements_by_css_selector('#ajax_load_post_list article .title a')
  for art in articles:
    print(art.get_attribute('href'))
    print(art.get_attribute('title'))
  page_number += 1

driver.quit()
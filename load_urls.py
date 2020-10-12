import time
import sys
import os
from selenium import webdriver

driver = webdriver.Chrome()

target = sys.argv[1]
target_en = sys.argv[2]

url_base = f'https://keizaiclub.com/category/{target}/page/'
progress_dir_name = 'loaded_urls'
progerss_file_path = f'./{progress_dir_name}/{target_en}.tsv'

page_number = 1

os.makedirs(progress_dir_name, exist_ok=True)

while True:
  url = f'{url_base}{page_number}/'
  driver.get(url)
  time.sleep(3)
  if 'ページが見つかりませんでした' in driver.title:
    with open(progerss_file_path, 'a') as f:
      f.write(f'QUALIFIED\n')
    break
  articles = driver.find_elements_by_css_selector('#ajax_load_post_list article .title a')
  for art in articles:
    link = art.get_attribute('href')
    title = art.get_attribute('title')
    with open(progerss_file_path, 'a') as f:
      f.write(f'{page_number}\t{link}\t{title}\n')
  page_number += 1
driver.quit()
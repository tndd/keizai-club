import time
import os
from selenium import webdriver

driver = webdriver.Chrome()

def load_links(target, target_en):
  url_base = f'https://keizaiclub.com/category/{target}/page/'
  progress_dir_name = 'loaded_urls'
  progerss_file_path = f'./{progress_dir_name}/{target_en}.tsv'
  os.makedirs(progress_dir_name, exist_ok=True)

  # init link file
  with open(progerss_file_path, 'w') as f:
    f.write('')
  print(f"init: {progerss_file_path}")

  page_number = 1
  while True:
    url = f'{url_base}{page_number}/'
    driver.get(url)
    time.sleep(3)
    if 'ページが見つかりませんでした' in driver.title:
      print(f'QUALIFIED: {target}')
      break
    articles = driver.find_elements_by_css_selector('#ajax_load_post_list article .title a')
    for art in articles:
      link = art.get_attribute('href')
      title = art.get_attribute('title')
      with open(progerss_file_path, 'a') as f:
        f.write(f'{page_number}\t{link}\t{title}\n')
    page_number += 1

# load targets
with open('target_list.tsv', 'r') as f:
  lines = list(map(lambda x: x.strip().split('\t'), f.readlines()))

# execute load from lines
for l in lines:
  load_links(l[0], l[1])

driver.quit()
from logging import error
import os
import json
import glob
import time
import urllib.request
from selenium import webdriver


progress_file_name = 'dl_progress.json'
download_dir_name = 'downloaded'

def init_dl_progress(prog_file_name):
  dl_targets = glob.glob('loaded_urls/*.tsv')

  progress = dict()
  for dl_target in dl_targets:
    with open(dl_target) as f:
      lines = list(map(lambda x: x.strip().split('\t'), f.readlines()))
    for l in lines:
      progress[l[1]] = {
        'group': os.path.splitext(os.path.basename(dl_target))[0],
        'name': l[2],
        'status': False
      }
  with open(prog_file_name, 'w') as f:
    json.dump(progress, f, indent=2)
  print(f"Created progress file: {progress_file_name}")

  return progress

# load progress file
if os.path.exists(progress_file_name):
  with open(progress_file_name) as f:
    progress = json.load(f)
else:
  progress = init_dl_progress(progress_file_name)

# login flow
driver = webdriver.Chrome()
with open('conf.json') as f:
  conf = json.load(f)
driver.get('https://keizaiclub.com/membership-login/')
driver.find_element_by_css_selector('#swpm_user_name').send_keys(conf['username'])
driver.find_element_by_css_selector('#swpm_password').send_keys(conf['password'])
time.sleep(1)
driver.find_element_by_css_selector('.swpm-login-form-submit').click()

# download files
try:
  for url, detail in progress.items():
    if detail['status'] == True:
      continue
    # tmp
    if detail['group'] != 'podcasting':
      continue
    driver.get(url)
    time.sleep(3)
    links = driver.find_elements_by_css_selector('a')
    for l in links:
      if l.text == '音声ダウンロード（MP3)':
        print(f"Downloading: {url}")
        # extract date num
        urls = url.split('/')
        date_num = urls[-5] + urls[-4] + urls[-3]
        file_name = f"{date_num}_{detail['name']}.mp3"
        # create download dir
        group_dir_path = f"./{download_dir_name}/{detail['group']}"
        os.makedirs(group_dir_path, exist_ok=True)
        # download mp3
        try:
          urllib.request.urlretrieve(l.get_attribute('href'), f"{group_dir_path}/{file_name}")
          progress[url]['status'] = True
          print(f"Completed: {file_name}")
          time.sleep(1)
        except:
          print(f"Skiped: {url}")
        break
except Exception as e:
  error(e)
  error(e.message)
finally:
  # save progress
  with open(progress_file_name, 'w') as f:
    json.dump(progress, f, indent=2)
  print(f"Updated: {progress_file_name}")
  driver.quit()
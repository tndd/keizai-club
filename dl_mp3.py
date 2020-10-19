from logging import error
import os
import json
import time
import urllib.request
from selenium import webdriver

from upd_progress import (
  load_progress,
  add_new_progress_from_loaded_urls,
  sync_progress_status_with_downloaded,
  write_progress
)


def login_flow():
  driver = webdriver.Chrome()
  with open('conf.json') as f:
    conf = json.load(f)
  driver.get('https://keizaiclub.com/membership-login/')
  driver.find_element_by_css_selector('#swpm_user_name').send_keys(conf['username'])
  driver.find_element_by_css_selector('#swpm_password').send_keys(conf['password'])
  time.sleep(1)
  driver.find_element_by_css_selector('.swpm-login-form-submit').click()
  return driver


def download_files(driver, progress, download_dir_name):
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
            # delete breaked file
            if os.path.exists(f"{group_dir_path}/{file_name}"):
              os.remove(f"{group_dir_path}/{file_name}")
          break
  except Exception as e:
    error(e)
    error(e.message)
  finally:
    driver.quit()
    return progress


if __name__ == "__main__":
  progress_file_name = 'dl_progress.json'
  download_dir_name = 'downloaded'
  # init progress
  progress = load_progress(progress_file_name)
  progress_updated = add_new_progress_from_loaded_urls(progress)
  progress_synced_status = sync_progress_status_with_downloaded(progress_updated)
  # login
  driver = login_flow()
  # progress dictionaly is updated
  downloaded_progress = download_files(
    driver=driver,
    progress=progress_synced_status,
    download_dir_name=download_dir_name
  )
  # save progress dictionaly to file
  write_progress(
    progress_file_name=progress_file_name,
    progress=downloaded_progress
  )
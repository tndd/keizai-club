import sys
import os
import json
# from selenium import webdriver

# driver = webdriver.Chrome()

dl_target = sys.argv[1]

dl_dir_name = 'downloaded'
os.makedirs(dl_dir_name, exist_ok=True)

with open(f'./loaded_urls/{dl_target}.tsv') as f:
  lines = list(map(lambda x: x.strip().split('\t'), f.readlines()))

progress = dict()
for l in lines:
  progress[l[1]] = {
    'group': dl_target,
    'name': l[2],
    'status': False
  }

with open('dl_progress.json', 'w') as f:
  json.dump(progress, f, indent=2)

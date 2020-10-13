import sys
import os
import json
import glob
# from selenium import webdriver

# driver = webdriver.Chrome()

progress_file_name = 'dl_progress.json'

def init_dl_progress(prog_file_name):
  dl_targets = glob.glob('loaded_urls/*.tsv')
  dl_dir_name = 'downloaded'
  os.makedirs(dl_dir_name, exist_ok=True)

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
  with open('dl_progress.json', 'w') as f:
    json.dump(progress, f, indent=2)

  return progress

# load progress file
if os.path.exists(progress_file_name):
  with open(progress_file_name) as f:
    progress = json.load(f)
else:
  progress = init_dl_progress(progress_file_name)

print(progress)
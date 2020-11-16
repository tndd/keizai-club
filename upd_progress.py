import glob
import os
import json

from pprint import pprint

def load_progress(progress_file_name):
  if os.path.exists(progress_file_name):
    with open(progress_file_name, 'r') as f:
      progress = json.load(f)
  else:
    progress = dict()
  return progress

def add_new_progress_from_loaded_urls(progress):
  dl_dir_name = 'loaded_urls'
  with open('target_list.tsv', 'r') as f:
    dl_targets = list(map(
      lambda x: f"{dl_dir_name}/" + x.strip().split('\t')[1] + '.tsv',
      f.readlines()
    ))
  new_added_progress = []
  for dl_target in dl_targets:
    with open(dl_target) as f:
      lines = list(map(lambda x: x.strip().split('\t'), f.readlines()))
    for l in lines:
      # skip update if already exist key in progress dictionary
      if l[0] in progress.keys():
        continue
      # add new progress
      progress[l[0]] = {
        'group': os.path.splitext(os.path.basename(dl_target))[0],
        'name': l[1].replace('/', '-'),
        'status': False
      }
      new_added_progress.append(l[0])
  print(f'New Added url num: {len(new_added_progress)}')
  pprint(new_added_progress)
  return progress

def sync_progress_status_with_downloaded(progress):
  downloaded_mp3s = glob.glob('downloaded/*/*.mp[3,4]')
  cnt_downloaded_files = 0
  for url, detail in progress.items():
    progress[url]['status'] = False
    for title in downloaded_mp3s:
      if detail['name'] in title and detail['group'] in title:
        progress[url]['status'] = True
        cnt_downloaded_files += 1
        break
  print(f"Synced file num: {cnt_downloaded_files}")
  return progress

def exclude_urls(progress, exclude_urls_file_name):
  with open(exclude_urls_file_name, 'r') as f:
    urls = f.readlines()
  for url in urls:
    try:
      del progress[url.replace('\n', '')]
    except:
      pass
  return progress

def write_progress(progress_file_name, progress):
  # update progress file
  with open(progress_file_name, 'w') as f:
    json.dump(progress, f, indent=2)
  print(f"Updated progress file: {progress_file_name}")

def init_progress():
  progress_file_name = 'dl_progress.json'
  exclude_urls_file_name = 'exclude_urls.txt'
  progress = load_progress(progress_file_name)
  progress_updated = add_new_progress_from_loaded_urls(progress)
  progress_synced_status = sync_progress_status_with_downloaded(progress_updated)
  progress_excluded = exclude_urls(progress_synced_status, exclude_urls_file_name)
  write_progress(progress_file_name, progress_excluded)

if __name__ == "__main__":
  init_progress()

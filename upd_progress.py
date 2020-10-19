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
  dl_targets = glob.glob('loaded_urls/*.tsv')
  new_added_progress = []
  for dl_target in dl_targets:
    with open(dl_target) as f:
      lines = list(map(lambda x: x.strip().split('\t'), f.readlines()))
    for l in lines:
      # skip update if already exist key in progress dictionary
      if l[1] in progress.keys():
        continue
      # add new progress
      progress[l[1]] = {
        'group': os.path.splitext(os.path.basename(dl_target))[0],
        'name': l[2],
        'status': False
      }
      new_added_progress.append(l[1])
  print(f'New Added url num: {len(new_added_progress)}')
  pprint(new_added_progress)
  return progress

def sync_progress_status_with_downloaded(progress):
  downloaded_mp3s = glob.glob('downloaded/*/*.mp3')
  cnt_downloaded_files = 0
  for url, detail in progress.items():
    progress[url]['status'] = False
    for title in downloaded_mp3s:
      if detail['name'] in title:
        progress[url]['status'] = True
        cnt_downloaded_files += 1
        break
  print(f"Synced file num: {cnt_downloaded_files}")
  return progress

def write_progress(progress_file_name, progress):
  # update progress file
  with open(progress_file_name, 'w') as f:
    json.dump(progress, f, indent=2)
  print(f"Updated progress file: {progress_file_name}")


if __name__ == "__main__":
  progress_file_name = 'dl_progress.json'
  progress = load_progress(progress_file_name)
  progress_updated = add_new_progress_from_loaded_urls(progress)
  progress_synced_status = sync_progress_status_with_downloaded(progress_updated)
  write_progress(progress_file_name, progress_synced_status)

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

def update_progress(progress):
  dl_targets = glob.glob('loaded_urls/*.tsv')
  mp3s = glob.glob('downloaded/*/*.mp3')
  new_added_progress = []
  for dl_target in dl_targets:
    with open(dl_target) as f:
      lines = list(map(lambda x: x.strip().split('\t'), f.readlines()))
    for l in lines:
      # skip update if already exist key in progress dictionary
      if l[1] in progress.keys():
        continue
      # judge state
      status = False  # default status is false
      for title in mp3s:
        if l[2] in title:
          status = True
          break
      # add new progress
      progress[l[1]] = {
        'group': os.path.splitext(os.path.basename(dl_target))[0],
        'name': l[2],
        'status': status
      }
      new_added_progress.append(l[1])
  print('New Added urls:')
  pprint(new_added_progress)
  return progress

def write_progress(progress_file_name, progress):
  # update progress file
  with open(progress_file_name, 'w') as f:
    json.dump(progress, f, indent=2)
  print(f"Updated progress file: {progress_file_name}")


if __name__ == "__main__":
  progress_file_name = 'dl_progress.json'
  progress = load_progress(progress_file_name)
  updated_progress = update_progress(progress)
  write_progress(progress_file_name, progress)

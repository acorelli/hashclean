import re
import os
import shutil
import sys
import time

from tqdm.auto import tqdm


script_dir = os.path.dirname(os.path.realpath(__file__))

pattern = r'\[\d+?\] .*?:((.*?),)+?'

# list of safewords to skip processing if found in the filepath
safe_words = []
if '--unsafe' not in sys.argv:
  try:
    with open(os.path.join(script_dir, 'safe_words.txt'), 'r') as f:  
      safe_words = f.read().split('\n')
      if '' in safe_words:
        safe_words.remove('')
      print('Safe words: ', safe_words)
  except Exception as e:
    print(f'Error reading safe_words.txt: {e}')
    print("Please fix/create safe_words.txt or run with the '--unsafe' flag")
    sys.exit(1)

# load file with extensions to check
try:
  with open(os.path.join(script_dir, 'target_extensions.txt')) as f:
    target_ext = f.read().split('\n')
    if '' in target_ext:
        target_ext.remove('')
    print('Targeting: ', target_ext)
except Exception as e:
  print(f'Error reading target_extensions.txt: {e}')
  print(f'Please fix/create target_extensions.txt and retry')
  sys.exit(1)
  
def process_hash_input_file(path):
  if not os.path.exists(path):
    raise Exception('Invalid path to clean_hash.py input file')
  with open(path, 'r') as f:
    content = f.read().split('\n')

  progress_bar = tqdm(total=len(content), desc='Removing duplicate files', unit='File', unit_scale=False)
  for l in content:
    matches = ':'.join(l.split(':')[1:]).split(',')
    print('\x1b[38;2;11;127;255m', end='')
    print(matches[0].strip(), end='')
    print('\x1b[0m')
    
    # find first existing file and remove from list
    # to keep it safe from deletion
    safe = False
    for m in matches:
      ms = m.strip()
      if os.path.exists(ms):
        # remove first existing from list
        print(f'\x1b[38;2;50;255;50mKeeping {ms} safe\x1b[0m')
        matches.remove(m)
        safe = True
        break
    
    if not safe:
      print(f"\x1b[38;2;255;40;40mCould NOT find safe file for entry '{matches[0].strip()}'. skipping\x1b[0m")
      continue
    
    for m in matches:
      m = m.strip()
      safe = False
      for safe_word in safe_words:
        if safe_word.lower() in m.lower():
          print(f'Skipping {m} -- found safeword {safe_word}')
          safe = True
          continue
      if safe:
        continue
      if os.path.exists(m):
        if len(m) > 0:
          # only if targeted extension
          ext = os.path.splitext(m)[1]
          if target_ext is None or ext not in target_ext:
            print(f'\x1b[38;2;255;50;50mSkipping - {m} not a targeted file\x1b[0m')
            continue
          # safety check
          if '-y' in sys.argv:
            # delete file if '-y' in sys.argv
            print(f'\x1b[38;2;255;11;127mDeleting file: \x1b[0m{m} ...')
            os.remove(m)
          else:
            # don't delete if no '-y' flag in sys.argv
            print(f'\x1b[38;2;255;127;11mTEST\x1b[0m - Deleting file: {m} ...')
            continue
    
    print('\x1b[0m')
    progress_bar.update(1)
  
  print('\x1b[38;2;255;187;17mDONE\x1b[0m')
  if not '-y' in sys.argv:
    print("Test run complete. If everything looks good run with a '-y' in the args")
    
  
if __name__=="__main__":
  try:
    process_hash_input_file(sys.argv[1])
  except Exception as e:
    print(f'Error: {e}')
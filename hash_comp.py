import hashlib
import os
import sys

from os import listdir
from os.path import isfile, join
from pprint import pprint
from tqdm.auto import tqdm

script_dir = os.path.dirname(os.path.realpath(__file__))

try:
  # load file with extensions to check
  with open(os.path.join(script_dir, 'target_extensions.txt')) as f:
    target_ext = f.read().split('\n')
    if '' in target_ext:
        target_ext.remove('')
    print('Targeting: ', target_ext)
except Exception as e:
  print(f'Error reading target_extensions.txt: {e}')
  target_ext = None

def calc_hash(filename, hasher=hashlib.sha1()):
  with open(filename, 'rb') as file:
    while True:
      chunk = file.read(4096)  # Read file in chunks
      if not chunk:
        break
      hasher.update(chunk)
  return hasher.hexdigest()

if __name__=="__main__":
  start_dir = os.getcwd()
  if len(sys.argv) > 1:
    dirs = sys.argv[1:]
  else:
    dirs = [os.getcwd()]
    
  hashes = {}
  try:
    n = 0
    t = len(dirs)
    for d in dirs:
      n += 1
      os.chdir(d)
      for root, path, files in os.walk(os.getcwd()):
        progress_bar = tqdm(total=len(files), desc=f'[{n}/{t}] Checking {root}', unit='File', unit_scale=0)
        for file in files:
          file = os.path.join(root, file)
          progress_bar.update(1)
          ext = os.path.splitext(file)[1]
          if target_ext is not None and ext not in target_ext:
            continue
          
          try:
            hv = calc_hash(file, hashlib.blake2b())
          except Exception as e:
            print(f'Unable to process {file}: {e}')
            continue
          
          try:
            if hv not in hashes:
              hashes[hv] = []
            
            hashes[hv].append(os.path.join(d, file))
            if len(hashes[hv]) > 1:
              dots = ''
              if len(hv) > 16:
                dots = '...'
              print(f'{hv[:16]}{dots}', hashes[hv])
          except Exception as e:
            print(f'Error processing {file}: {e}')
          #print(f'{file[:15]}: {hv}')
  except KeyboardInterrupt:
    print('Ctrl-C... stopping & saving')
  except Exception as e:
    print('!'*80)
    print(f'Error checking hashes: {e}')
    print('!'*80)
  
  if len(hashes) > 0:  
    os.chdir(start_dir)
    out_file_base = 'hash_res'
    out_file_ext = 'txt'
    out_suffix = ''
    out_file = f'{out_file_base}.{out_file_ext}'
    while os.path.exists(out_file):
      if out_suffix == '':
        out_suffix = 1
      else:
        out_suffix += 1
      out_file = f'{out_file_base} ({out_suffix}).{out_file_ext}'
    print(f'Saving results to {out_file}')
    with open(out_file, 'w') as f:
      progress_bar = tqdm(total=len(hashes), desc='Writing entries', unit='Entry', unit_scale=0)
      for key, value in hashes.items():
        #print(f'key: {key}, value: {value}')
        #print(len(value))
        progress_bar.update(1)
        try:
          if len(value) > 1:
            f.write(f'[{len(value)}] {key}: ')
            for v in value:
              f.write(f'{v}, ')
            f.write('\n')
        except:
          continue
  else:
    print(f'No hashes found. Exiting')
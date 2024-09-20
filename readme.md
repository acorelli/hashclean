# `hashclean`  
  
:warning: USE AT YOUR OWN RISK  :warning:  
  
A utility to de-duplicate media and other files based on hashing the contents of the file rather than relying on its filename
  
## Usage  

1. Create `safe_words.txt` & `target_extensions.txt` (can rename/copy the `.example` files)  
2. Install requirements: `python -m pip install -r requirements.txt`  
3. Run `hash_comp.py [space-separated list of directories to process (recursive)]`  
  > `python.exe hash_comp.py C:/users/<me>/Documents/Media C:/users/<me>/Media`  
4. Wait for results...  
5. Run `clean_hash.py` on the results file (`hash_res.txt`)  
  > `python.exe clean_hash.py ./hash_res.txt -y`  
    
    - use `-y` to indicate you want to delete files  
    - omit `-y` or add `-t` to run in `test` mode  

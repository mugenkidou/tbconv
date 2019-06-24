# tbconv.py
Convert backup file of [Roland](https://www.roland.com/)  [TB-3](https://www.roland.com/us/products/tb-3/) and [TB-03](https://www.roland.com/us/products/tb-03/) mutually.

---

## Usage
```
$ python tbconv.py INPUT_FILE OUTPUT_FILE [--print]
```
    INPUT_FILE:     File to convert.  
    OUTPUT_FILE:    The result of file conversion.  
    -p(--print):    Print input and output file.  


* `tbconv` detects if input file is for TB-3 or TB-03 automatically, and convert the file mutually.
* Length of TB-3 pattern may be longer than 16 steps, but TB-03's are not. In such case, `tbconv` generate separated two TB-03 files.  
* Before use `tbconv`, please make any necessary backups of TB-3/03. 
* To restore backup files to TB-3/03, see [owner's manual of them](https://www.roland.com/us/support/owners_manuals/t_z/).


## Unittest

1. If you have not installed pytest, please install it

    ```
    $ pip install -r test_requirements.txt
    ```

2. Run pytest

    ```
    $ pytest
    ```

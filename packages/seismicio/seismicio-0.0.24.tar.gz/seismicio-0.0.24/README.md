# Seismic-io
Python package to read and write Seismic-Unix files (.su)

## Install

```
pip install seismic-io
```

## Available Functions

### readsu
Read the _`.su`_ file.

Return two objects for header and traces respectively.

Take _`file_path`_ _string_ as the only param.


**Usage Example:**
```py
from seismicio import readsu
readsu(file_path)
```


### readsuInMemory
Does the same as the _`readsu`_ function but uses in-memory file system.

Take the same arguments and have the same return.


**Usage Example:**
```py
from seismicio import readsuInMemory
readsuInMemory(file_path)
```


### writesu
Write a _`.su`_ file.

Have no return.

**Params:**
 - _`file_path`_: 
_string_
 - _`traces_data`_: 
_array[object]_
 - _`hdr`_:
_array[object]_ of _`Header.getAllHeaders`_


**Usage Example:**
```py
from seismicio import writesu
writesu(file_path)
```


### writesuInMemory
Does the same as the _`writesu`_ function but uses in-memory file system.

Take the same arguments and have the same return.


**Usage Example:**
```py
from seismicio import writesuInMemory
writesuInMemory(file_path)
```

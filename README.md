# ZIPF

## What does it do?
It builds a zipf out of a directory of files, using multiprocessing since with large amounts of files the process can be very long.

## How do I use it?
Here's a small example:
```python
from zipf.zipf import zipf

z = zipf("/path/to/my/directory", ["json"])

z.set_interface(lambda f: f) # function that loads the part of the file that you want. For example, if you have json files you might want to load a specific attribute.
z.set_word_filter(lambda w: w not in [" ", '']) # You might want to filter out some words.

z.run()
```

## What do you plan to add to it in the near future?
I'll add some statistical operation of the zipf, such as calculating median, variance, mean...

## License
This library is released under MIT license.
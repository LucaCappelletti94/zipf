# ZIPF

## What does it do?
It builds a zipf out of a directory of files, using multiprocessing since with large amounts of files the process can be very long.

## How much time does it take to process?
Well, I created a zipf of about 1M text webpages and it took about 10 minutes. For 4k pages it takes about 2 seconds.

## How do I use it?
Here's a small example:
```python
from zipf import zipf

my_zipf = zipf.from_dir(
    path = "path/to/my/dir",
    file_interface = lambda f: f, # function that loads the part of the file that you want. For example, if you have json files you might want to load a specific attribute.
    word_filter = lambda w: w not in [" ", ''], # You might want to filter out some words.
    output_file = "output.json",
    use_cli = True
)

print(my_zipf)
```

## What do you plan to add to it in the near future?
I'll add some statistical operation of the zipf, such as calculating median, variance, mean...

## License
This library is released under MIT license.
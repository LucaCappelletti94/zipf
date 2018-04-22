# ZIPF

[![Docs Status](https://readthedocs.org/projects/zipf/badge/)](https://readthedocs.org/projects/zipf/badge/)

## What does it do?
The zipf package was realized to simplify creations and operations with zipf distributions, like sum, subtraction, mutiplications, divisions, slicing, statical operations such as mean, variance and much more.

## How do I get it?
Just type into your terminal:

`pip install zipf`

## How much time does it take to process?
Well, I created a zipf of about 1M text webpages and it took about 5 minutes. For 4k pages it takes about 1-2 seconds.

## How do I use it?
The (work in progress at the current time) [documentation](http://zipf.readthedocs.io/en/latest/) is now available.

## Creting a zipf using a zipf_factory
Here's a couple of examples:

### Zipf from a list

```python
from zipf.factories import zipf_from_list

my_factory = zipf_from_list()
my_zipf = my_factory.run(["one", "one", "two", "my", "oh", "my", 1, 2, 3])

print(my_zipf)

'''
{
  "one": 0.22222222222222215,
  "my": 0.22222222222222215,
  "two": 0.11111111111111108,
  "oh": 0.11111111111111108,
  "1": 0.11111111111111108,
  "2": 0.11111111111111108,
  "3": 0.11111111111111108
}
'''
```

### Zipf from a text

```python
from zipf.factories import zipf_from_text

my_factory = zipf_from_text()
my_factory.set_word_filter(lambda w: len(w)>3)
my_zipf = my_factory.run("You've got to find what you love. And that is as true for your work as it is for your lovers … Keep looking. Don't settle.")

print(my_zipf)

'''
{
  "your": 0.16666666666666666,
  "find": 0.08333333333333333,
  "what": 0.08333333333333333,
  "love": 0.08333333333333333,
  "that": 0.08333333333333333,
  "true": 0.08333333333333333,
  "work": 0.08333333333333333,
  "lovers": 0.08333333333333333,
  "Keep": 0.08333333333333333,
  "looking": 0.08333333333333333,
  "settle": 0.08333333333333333
}
'''
```

### Zipf from a text file

```python
from zipf.factories import zipf_from_file

my_factory = zipf_from_file()
my_factory.set_word_filter(lambda w: w!="brown")
my_zipf = my_factory.run()

print(my_zipf)

'''
{
  "The": 0.125,
  "quick": 0.125,
  "fox": 0.125,
  "jumps": 0.125,
  "over": 0.125,
  "the": 0.125,
  "lazy": 0.125,
  "dog": 0.125
}
'''
```

### Zipf from webpage

```python
from zipf.factories import zipf_from_url
import json

my_factory = zipf_from_url()
my_factory.set_word_filter(lambda w: int(w)>100)
my_factory.set_interface(lambda r: json.loads(r.text)["ip"])
my_zipf = my_factory.run("https://api.ipify.org/?format=json")

print(my_zipf)

'''
{
  "134": 0.5,
  "165": 0.5
}
'''
```

### Zipf from directory

```python
from zipf.factories import zipf_from_dir
import json

my_factory = zipf_from_dir()
my_factory.set_word_filter(lambda w: len(w)>4)
my_zipf = my_factory.run("path/to/my/directory", ["txt"])

# My directory contains 2 files with the following texts:
# 1) You must not lose faith in humanity. Humanity is an ocean; if a few drops of the ocean are dirty, the ocean does not become dirty.
# 2) Try not to become a man of success, but rather try to become a man of value.

print(my_zipf)

'''
{
  "ocean": 0.20000000000000004,
  "become": 0.20000000000000004,
  "dirty": 0.13333333333333336,
  "faith": 0.06666666666666668,
  "humanity": 0.06666666666666668,
  "Humanity": 0.06666666666666668,
  "drops": 0.06666666666666668,
  "success": 0.06666666666666668,
  "rather": 0.06666666666666668,
  "value": 0.06666666666666668
}
'''
```

## Batch operations

## License
This library is released under MIT license.

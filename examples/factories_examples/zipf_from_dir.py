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
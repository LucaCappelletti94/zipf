from zipf.factories import zipf_from_file

my_factory = zipf_from_file()
my_factory.set_word_filter(lambda w: w!="brown")
my_zipf = my_factory.run("path/to/my/file.txt")

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
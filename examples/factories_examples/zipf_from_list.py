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
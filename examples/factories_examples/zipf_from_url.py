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
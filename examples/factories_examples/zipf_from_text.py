from zipf.factories import zipf_from_text

my_factory = zipf_from_text()
my_factory.set_word_filter(lambda w: w != "find")
my_zipf = my_factory.run("You've got to find what you love. And that is as true for your work as it is for your lovers … Keep looking. Don't settle.")

print(my_zipf)

'''
{
  "is": 0.07692307692307696,
  "as": 0.07692307692307696,
  "for": 0.07692307692307696,
  "your": 0.07692307692307696,
  "You": 0.03846153846153848,
  "ve": 0.03846153846153848,
  "got": 0.03846153846153848,
  "to": 0.03846153846153848,
  "what": 0.03846153846153848,
  "you": 0.03846153846153848,
  "love": 0.03846153846153848,
  "And": 0.03846153846153848,
  "that": 0.03846153846153848,
  "true": 0.03846153846153848,
  "work": 0.03846153846153848,
  "it": 0.03846153846153848,
  "lovers": 0.03846153846153848,
  "Keep": 0.03846153846153848,
  "looking": 0.03846153846153848,
  "Don": 0.03846153846153848,
  "t": 0.03846153846153848,
  "settle": 0.03846153846153848
}
'''
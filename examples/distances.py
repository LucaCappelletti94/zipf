from zipf import zipf

my_first_zipf=zipf.load("my_first_zipf.json")
my_second_zipf=zipf.load("my_second_zipf.json")

print("Kullback-Leibler: %s"%my_first_zipf.kullback_leibler(my_second_zipf))
print("Jensen-Shannon: %s"%my_first_zipf.jensen_shannon(my_second_zipf))
print("Hellinger: %s"%my_first_zipf.hellinger(my_second_zipf))
print("Total Variation: %s"%my_first_zipf.total_variation(my_second_zipf))
print("Bhattacharyya: %s"%my_first_zipf.bhattacharyya(my_second_zipf))
print("Mahalanobis: %s"%my_first_zipf.mahalanobis(my_second_zipf))

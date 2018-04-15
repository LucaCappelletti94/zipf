from zipf.zipf import zipf

z = zipf("/path/to/my/directory", ["json"])

z.set_interface(lambda f: f) # function that loads the part of the file that you want. For example, if you have json files you might want to load a specific attribute.
z.set_word_filter(lambda w: w not in [" ", '']) # You might want to filter out some words.

z.run()
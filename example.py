from zipf import zipf

my_zipf = zipf.from_dir(
    path = "path/to/my/dir",
    file_interface = lambda f: f, # function that loads the part of the file that you want. For example, if you have json files you might want to load a specific attribute.
    word_filter = lambda w: w not in [" ", ''], # You might want to filter out some words.
    output_file = "output.json",
    use_cli = True
)

print(my_zipf)
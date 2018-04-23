zipf
====

The zipf package was realized to simplify creations and operations with zipf distributions, like:

* Sum/subtract two zipfs.
* Multiply/divide a zipfs by a zipf or a number.
* Slice a zipf.
* KL divergence (entropy) of two zipfs.
* JS divergence of two zipfs.
* Statistical operations such as:
    - mean
    - variance
    - median

Currently exists factories to create a zipf from:

* A list.
* A text.
* A text file.
* An url to a webpage.
* A directory containing one or more directories containing text files.

It is also possible to calculate in batch operations like the `Jensen–Shannon divergence (JSD) <https://en.wikipedia.org/wiki/Jensen%E2%80%93Shannon_divergence>`_.
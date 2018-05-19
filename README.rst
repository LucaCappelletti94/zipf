====
ZIPF
====

|travis| |coveralls| |sonar_quality| |sonar_maintainability| |code_climate_maintainability| |pip|

--------------------------------------
What does it do?
--------------------------------------
The zipf package was realized to simplify creations and operations with zipf distributions, like sum, subtraction, multiplications, divisions, statical operations such as mean, variance and much more.

--------------------------------------
How do I get it?
--------------------------------------
Just type into your terminal:

.. code:: shell

    pip install zipf


--------------------------------------
Calculating distances and divergence
--------------------------------------
I wrote another package called `dictances`_ which calculates various distances and divergences between discrete distributions such as zipf. Here's an example:

.. code:: python

    from zipf import Zipf
    from dictances import *

    a = zipf.load("my_first_zipf.json")
    b = zipf.load("my_second_zipf.json")

    euclidean(a, b)
    chebyshev(a, b)
    hamming(a, b)
    kullback_leibler(a, b)
    jensen_shannon(a, b)


--------------------------------------
Creating a zipf using a zipf_factory
--------------------------------------
Here's a couple of examples:

Zipf from a list
-------------------------
.. code:: python

    from zipf.factories import ZipfFromList

    my_factory = ZipfFromList()
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


Zipf from a text
-------------------------
.. code:: python

    from zipf.factories import ZipfFromText

    my_factory = ZipfFromText()
    my_factory.set_word_filter(lambda w: len(w) > 3)
    my_zipf = my_factory.run(
        """You've got to find what you love.
           And that is as true for your work as it is for your lovers.
           Keep looking. Don't settle.""")

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


Zipf from a k-sequence
-------------------------
.. code:: python

    from zipf.factories import ZipfFromKSequence

    sequence_fraction_len = 5
    my_factory = ZipfFromKSequence(sequence_fraction_len)
    my_zipf = my_factory.run(
        "ACTGGAAATGATGGDTGATDGATGAGTDGATGGGGGAAAGDTGATDGATDGATGDTGGGGADDDGATAGDTAGTDGAGAGAGDTGATDGAAAGDTG")

    print(my_zipf)

    '''
    {
      "TGGGG": 0.1,
      "ACTGG": 0.05,
      "AAATG": 0.05,
      "ATGGD": 0.05,
      "TGATD": 0.05,
      "GATGA": 0.05,
      "GTDGA": 0.05,
      "GAAAG": 0.05,
      "DTGAT": 0.05,
      "DGATD": 0.05,
      "GATGD": 0.05,
      "ADDDG": 0.05,
      "ATAGD": 0.05,
      "TAGTD": 0.05,
      "GAGAG": 0.05,
      "AGDTG": 0.05,
      "ATDGA": 0.05,
      "AAGDT": 0.05,
      "G": 0.05
    }
    '''



Zipf from a text file
-------------------------
.. code:: python

    from zipf.factories import ZipfFromFile

    my_factory = ZipfFromFile()
    my_factory.set_word_filter(lambda w: w != "brown")
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



Zipf from webpage
-------------------------
.. code:: python

    from zipf.factories import ZipfFromUrl
    import json

    my_factory = ZipfFromUrl()
    my_factory.set_word_filter(lambda w: int(w) > 100)
    my_factory.set_interface(lambda r: json.loads(r.text)["ip"])
    my_zipf = my_factory.run("https://api.ipify.org/?format=json")

    print(my_zipf)

    '''
    {
      "134": 0.5,
      "165": 0.5
    }
    '''



Zipf from directory
-------------------------
.. code:: python

    from zipf.factories import ZipfFromDir
    import json

    my_factory = ZipfFromDir(use_cli=True)
    my_factory.set_word_filter(lambda w: len(w) > 4)
    my_zipf = my_factory.run("path/to/my/directory", ["txt"])

    '''
    My directory contains 2 files with the following texts:

    - You must not lose faith in humanity.
      Humanity is an ocean; if a few drops of the ocean are dirty,
      the ocean does not become dirty.
    - Try not to become a man of success,
      but rather try to become a man of value.
    '''

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


--------------------------------------
Options in creating a zipf
--------------------------------------

Some built in options are available, and you can read the options of any factory object by printing it:

.. code:: python

    from zipf.zipf.factories import ZipfFromList
    print(ZipfFromList())

    '''
    {
      "remove_stop_words": false, # Removes stop words (currently only Italian's)
      "minimum_count": 0, # Removes words that appear less than 'minimum_count'
      "chain_min_len": 1, # Chains up words, starting by a min of 'chain_min_len'
      "chain_max_len": 1, # and ending to a maximum of 'chain_max_len'
      "chaining_character": " ", # The character to interpose between words
      "chain_after_filter": false, # The chaining is done after filtering
      "chain_after_clean": false # The chaining is done after cleaning
    }
    '''

--------------------------------------
License
--------------------------------------
This library is released under MIT license.

.. |travis| image:: https://travis-ci.org/LucaCappelletti94/zipf.png
   :target: https://travis-ci.org/LucaCappelletti94/zipf

.. |coveralls| image:: https://coveralls.io/repos/github/LucaCappelletti94/zipf/badge.svg?branch=master
    :target: https://coveralls.io/github/LucaCappelletti94/zipf

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=zipf.lucacappelletti&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/zipf.lucacappelletti

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=zipf.lucacappelletti&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/zipf.lucacappelletti

.. |pip| image:: https://badge.fury.io/py/zipf.svg
    :target: https://badge.fury.io/py/zipf

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/c758496736a2c9cecbff/maintainability
   :target: https://codeclimate.com/github/LucaCappelletti94/zipf/maintainability
   :alt: Maintainability

.. _dictances: https://github.com/LucaCappelletti94/dictances
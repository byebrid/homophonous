# Wordsmith\.py

A python tool to generate homophonous sentences and phrases.

## Example
From a python terminal:
```
>>> from wordsmith import wordsmith
>>> phrase = 'Ice cream'
>>> phrases = wordsmith(phrase)
>>> for phrase in phrases:
...     print(phrase)
ai scream
ay scream
aye scream
eye scream
i scream
i. scream
ice cream
ice creme
```

Alternatively, from the command line:
```
$ python wordsmith.py "ice cream" # Note you need the required packages
```

----------------------------------------------------------------

## Requirements
* `pip install` using the provided requirements.txt file.
* This has the special requirement that you download the **Carnegie Mellon Pronouncing Dictionary** (CMPD) as sourced from the Natural Language Toolkit. See instructions on their website [here](https://www.nltk.org/data.html) for details on how to download the data.
* Uses static typing, so python >= 3.5 recommended.

----------------------------------------------------------------

## What it does
1) Given some phrase, we first tokenize the words:
```
'ice cream' -> ['ice', 'cream']
```

2) We then find these words in the CMPD and list their possible pronunciations:
```
[[['AY1', 'S']], [['K', 'R', 'IY1', 'M']]]
```

Note that, in this case, each word only had a single pronunciation but some may have multiple.

3) We then form every possible combination of these pronunciations to form every uniqe pronunciation of the original phrase:
```
[['AY1', 'S', 'K', 'R', 'IY1', 'M']]
```
Again, in this case, we only have a single pronunciation, but if both words had 2 pronunciations, you would expect a total of 4 unique pronunciations of the phrase.

4) We finally go through every possilbe partitioning of each pronunciation of the phrase, and match the pronunciations of each partition with a word if possible. If every partition can be matched with a word, then we have found a new phrase with the exact same pronunciation as the original. There are obviously a lot of ways to partition even a small list, but here are the first few from our example:
```
# This won't match with anything from the CMPD
[['AY1', 'S', 'K', 'R', 'IY1', 'M']]

# This will get matched with 'i scream', among other new phrases
[['AY1'], ['S', 'K', 'R', 'IY1', 'M']] 

# This will get matched with 'ice cream', among other new phrases
[['AY1', 'S'], ['K', 'R', 'IY1', 'M']] # Note this one will get matched with ''

# and so on....
```

5) At this point, it's simply a matter of cleaning up nested lists, etc. to finally extract our complete list of homophonous phrases:
```
['ai scream', 'ay scream', 'aye scream', 'eye scream', 'i scream', 'i. scream', 'ice cream', 'ice creme']
```

I really need a better example lol.

----------------------------------------------------------------

## Todo
* Add mapping of phonemes that sound very similar. I've been surprised by some words having phonemes that I can't even distinguish. Probably will do this with something like equivalence classes, not sure how best to make it customisable though.
* Make more efficient... somehow. I think for words with a single pronunciation that will appear in every phrase pronunciation, I should perhaps be a bit more clever about avoiding partitioning that same word's phonemes once for every phrase pronunciation.


#!python
import os
import io
import pickle
import operator
from collections import Counter, defaultdict

def get_all_files(directory):
    relativeFileList = []
    for dirpath, dirs, files in os.walk(directory):
        relativeFileList += [ (dirpath.replace(directory, '')) + ('' if dirpath == directory else '/') + filename for filename in files]
    return relativeFileList

"""
method to generate a count of all words in all the articles
in order to get a list of most frequent stopwords in the articles

An arbitrary count of top 5000 words are chosen as stopwords but should be
modified to reduce the number of stopwords
"""
def generate_stopwords(corpus_dir, lang):
	file_dir = corpus_dir +"/" +lang
	filelist = get_all_files(file_dir)
	wordcount = defaultdict(int)
	for filename in filelist:
		f = io.open(file_dir +'/' +filename, "r", encoding = "utf-16")
		temp = Counter(f.read().split())
		for key in temp:
			wordcount[key] += temp[key]

	sorted_wordcount = sorted(wordcount.items(), key = operator.itemgetter(1), reverse = True)
	return sorted_wordcount[:5000]


# stopwords = generate_stopwords('/scratch-local/users/dhruvils/Part2-TextExtraction/data/articles', 'en')
# pickle.dump(dict(stopwords), open('en.pickle', 'w'))

# words = pickle.load(open('en.pickle', 'r'))
# print words
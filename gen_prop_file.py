#!python
import os

def get_all_files(directory):
	relativeFileList = []
	for dirpath, dirs, files in os.walk(directory):
		relativeFileList += [ (dirpath.replace(directory, '')) + ('' if dirpath == directory else '/') + filename for filename in files]
	return relativeFileList

def generate_prop_file(directory):
	filelist = get_all_files(directory)
	output = "trainFileList = "
	for filename in filelist:
		output += "train/" + filename.replace(",", "") + ","

	output = output[:-1]

	output += "\nserializeTo = ner-model-second.ser.gz\n\
map = word=0,answer=1\n\
\n\
useClassFeature=true\n\
useWord=true\n\
useNGrams=true\n\
noMidNGrams=true\n\
maxNGramLeng=6\n\
usePrev=true\n\
useNext=true\n\
useSequences=true\n\
usePrevSequences=true\n\
maxLeft=1\n\
useTypeSeqs=true\n\
useTypeSeqs2=true\n\
useTypeySequences=true\n\
wordShape=chris2useLC\n\
useDisjunctive=true\n\
inputEncoding=utf-16\n\
outputEncoding=utf-16"

	f = open("train-second.prop", "w")
	f.write(output)
	f.close()

# directory = "train/"
directory = "train/"
generate_prop_file(directory)
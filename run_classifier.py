#! python

import os

def get_all_files(directory):
	relativeFileList = []
	for dirpath, dirs, files in os.walk(directory):
		relativeFileList += [ (dirpath.replace(directory, '')) + ('' if dirpath == directory else '/') + filename for filename in files]
	return relativeFileList

def run_classifier(directory):
	filelist = get_all_files(directory)

	for filename in filelist:
		command = "(java -cp stanford-ner/stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier ner-model-second.ser.gz -inputEncoding utf-16 -testFile test/%s > output-gaz/classified_%s)" %(filename, filename)
		os.system(command)

run_classifier("./test")
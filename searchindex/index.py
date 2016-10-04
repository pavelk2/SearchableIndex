import os
from performance import timeit
import re

class Index:
	def __init__(self, source_filepath = None):
		# dictionary containing normalized frequencies of words appearing in documents
		self.words = {}
		# dictionary containing document titles
		self.documents = {}
		# parse the source file to index the corpus 
		if source_filepath:
			self.indexSourceFile(source_filepath)

	#@timeit
	def indexSourceFile(self, source_filepath):
		# check if source file is available
		if not os.path.isfile(str(source_filepath)):
			print("The source file '%s' does not exist." % source_filepath)
			return False
		# open the source file and read row by row
		with open(source_filepath,'rb') as tsvin:
			for row in tsvin:
				# we expect that each row contains docID, title, and full text
				[docID, title, full_text] = row.split('\t')
				#  store word frequencies normalized by document size in searchable index
				self.addDocument(docID, title, full_text)
	
	def addDocument(self, docID, title, full_text):
		# store structured information about the document
		self.documents[docID] = {}
		self.documents[docID]['title'] = title
		# split document into words skipping punctuation
		words = re.findall(r'\w+', full_text.lower())
		document_size = len(words)
		# get a dictionary with word frequencies
		bag_of_words = self.getBagOfWords(words)
		# add information of word frequencies in the document to the word index
		for word in bag_of_words.keys():
			if word not in self.words:
				self.words[word] = {}
			# normalized word frequency dividing by the document size and store in the index
			self.words[word][docID] = 1.0*bag_of_words[word]/document_size
	
	@staticmethod
	def getBagOfWords(words):
		# for each word from the document we calculate the amount of time it occurs in this document
		bag_of_words = {}
		if type(words) is list:
			for word in words:
				if word not in bag_of_words:
					bag_of_words[word] = 0
				bag_of_words[word] +=1
		return bag_of_words

	def isEmpty(self):
		return self.documents == {} or self.words == {}

import re

from index import Index
from performance import timeit

class SearchableIndex(Index):
	#@timeit
	def search(self, query_string, max_documents_to_return = 10):
		keywords = self.getKeywords(query_string)
		# get all documents where all keywords occur
		results_unranked = self.getDocumentsByKeywords(keywords)
		# calculate rank for each document based on keyword frequencies
		results_ranked = [(docID, self.getDocumentRank(docID, keywords)) for docID in results_unranked]
		# sort documents according to their ranks (higher ranks first)
		results_ranked.sort(key=(lambda tup: tup[1]), reverse=True)
		# get top-k results
		results_ranked_sorted_top_k = results_ranked[:max_documents_to_return]
		# return list of tuples [..,(docID, title, rank),..]
		return [(result[0], self.documents[result[0]]['title'], result[1]) for result in results_ranked_sorted_top_k]

	def getDocumentsByKeywords(self, keywords):
		# retrieve documents containing all documents as an intersection of lists of documents containing each keyword
		return set.intersection(*[set(self.words[keyword].keys() if keyword in self.words else {}) for keyword in keywords])
	
	@staticmethod
	def getKeywords(query_string):
		# we clean up the search query and remove duplicate keywords as they only introduce more computation time
		return list(set(re.findall(r'\w+', query_string.strip().lower())))
	def getDocumentRank(self, docID, keywords):
		# how many times each keyword occurs in the document
		document_keywords_frequencies = [self.words[keyword][docID] for keyword in keywords if keyword in self.words]
		# if keywords are not in the document we might get an empty list
		if len(document_keywords_frequencies)>0:
			# product of keyword frequencies
			return reduce(lambda freq_keyword_1, freq_keyword_2: freq_keyword_1*freq_keyword_2, document_keywords_frequencies)
		else:
			return 0

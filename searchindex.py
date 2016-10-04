#!/usr/bin/env python2.7

import sys
from searchindex.search import SearchableIndex

DEFAULT_CORPUS = "wikipedia_example.tsv"
DEFAULT_QUERY = "Ludwig van Beethoven"

def main():
	# if source file is not give the DEFAULT_CORPUS is used
	source_input = DEFAULT_CORPUS
	if sys.argv[1:]:
	   source_input = sys.argv[1]
	# the given file is indexed
	corpus = SearchableIndex(source_input)
	
	if not corpus.isEmpty():
		# we allow a user to perform an unlimited number of sequential search queries
		while True:
			# if search query is not given the default is used
			keyword_string = raw_input("\nsearch> ") or DEFAULT_QUERY
			results = corpus.search(keyword_string)
			
			if len(results) == 0:
				print("No documents were found")
			for document in results:
				print "%s %s" % (document[0], document[1]) 
main()

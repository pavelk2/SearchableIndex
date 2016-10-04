import unittest
from searchindex.search import SearchableIndex

class SearchIndexTestCase(unittest.TestCase):
    def setUp(self):
        self.corpus = SearchableIndex("wikipedia_example.tsv")
        # [("query","the top document expected")]
        self.query_options = [
        	("Berlin", "Olympiastadion Berlin"),
        	("The", "The Warriors"),
        	("Ludwig van Beethoven", "Christian Gottlob Neefe"),
        	("STRING_WHICH_MOST_LIKELY_DOESNOT_APPEAR ANOTHER_STRANGE_STRING", None)
        ]

class SearchKeywordTestCase(SearchIndexTestCase):
    def runTest(self):
    	for query in self.query_options:
    		results = self.corpus.search(query[0])
    		self.assertEqual(results[0][1] if len(results)>0 else None , query[1],
                         'SearchIndex: incorrect search for query [%s]' % query[0])
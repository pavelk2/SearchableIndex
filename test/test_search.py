import unittest
from searchindex.search import SearchableIndex

class SearchTestCase(unittest.TestCase):
    def setUp(self):
    	self.corpus = SearchableIndex()
    	self.corpus_documents = [
    		("1", "Jupiter", "Jupiter is the fifth planet from the Sun and the largest in the Solar System. It is a giant planet with a mass one-thousandth that of the Sun, but two and a half times that of all the other planets in the Solar System combined"),
    		("2", "Saturn", "Saturn is the sixth planet from the Sun and the second-largest in the Solar System, after Jupiter"),
    		("3", "Earth", "Earth is the third planet from the Sun, the densest planet in the Solar System, the largest of the Solar System's four terrestrial planets, and the only astronomical object known to harbor life.")
    		]
    	for document in self.corpus_documents:
    		self.corpus.addDocument(document[0], document[1], document[2])

class GetKeywordsTestCase(SearchTestCase):
	def runTest(self):
		query_string_options = [
			("A Dog",["a","dog"]),
			("the the",["the"]),
			("        key   ",["key"]),
			(" ",[])
		]
		for query in query_string_options:
			self.assertEqual(self.corpus.getKeywords(query[0]), query[1], 'GetKeywords: Incorrect parsing of query')

class DocumentByKeywordsTestCase(SearchTestCase):
    def runTest(self):
    	documents = self.corpus.getDocumentsByKeywords(["jupiter"])
    	self.assertEqual(documents, {'1','2'}, 'DocumentByKeywords: Incorrect matching of documents by single keyword')
    	documents = self.corpus.getDocumentsByKeywords(["jupiter", "saturn"])
    	self.assertEqual(documents, {'2'}, 'DocumentByKeywords: Incorrect matching of documents by multiple keywords')

class DocumentRankTestCase(SearchTestCase):
    def runTest(self):
    	document_saturn_the_rank = self.corpus.getDocumentRank("2",["the"])
    	self.assertEqual(document_saturn_the_rank, 4.0/18, 'DocumentRank: Incorrect document rank calculation for a given keyword')
    	document_earth_the_rank = self.corpus.getDocumentRank("3",["AbCdEf"])
    	self.assertEqual(document_earth_the_rank, 0.0, 'DocumentRank: Incorrect document rank keyword which is absent in the document')

class SearchTestCase(SearchTestCase):
    def runTest(self):
    	documents = self.corpus.search("jupiter")
    	self.assertEqual(len(documents), 2, 'Search: Incorrect number of documents retrieved')
    	self.assertEqual(documents[0][1], "Saturn", 'Search: Incorrect ranking of documents retrieved')
 
if __name__ == '__main__':
    unittest.main()
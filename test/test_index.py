import unittest
from searchindex.index import Index
import re

class CorpusTestCase(unittest.TestCase):
    def setUp(self):
        self.corpus_documents = [
            ("1", "Jupiter", "Jupiter is the fifth planet from the Sun and the largest in the Solar System. It is a giant planet with a mass one-thousandth that of the Sun, but two and a half times that of all the other planets in the Solar System combined"),
            ("2", "Saturn", "Saturn is the sixth planet from the Sun and the second-largest in the Solar System, after Jupiter"),
            ("3", "Earth", "Earth is the third planet from the Sun, the densest planet in the Solar System, the largest of the Solar System's four terrestrial planets, and the only astronomical object known to harbor life.")
            ]
        self.corpus = Index()

class DefaultCorpusTestCase(CorpusTestCase):
    def runTest(self):
        self.assertEqual(self.corpus.words, {},
                         'Default: incorrect index of words')
        self.assertEqual(self.corpus.documents, {},
                         'Default: incorrect index of documents')

class BagOfWordsTestCase(CorpusTestCase):
    def runTest(self):
        words = re.findall(r'\w+', self.corpus_documents[1][2].lower())
        bagofwords = self.corpus.getBagOfWords(words)
        self.assertEqual(len(bagofwords.keys()), 15,
                         'Bag_of_words: incorrect number of words identified')
        self.assertEqual(bagofwords, {'and': 1, 'after': 1, 'from': 1, 'in': 1, 'sixth': 1, 'is': 1, 'largest': 1, 'system': 1, 'planet': 1, 'second': 1, 'jupiter': 1, 'solar': 1, 'sun': 1, 'the': 4, 'saturn': 1},
                         'Bag_of_words: incorrect bag of words identified')
        bagofwords = self.corpus.getBagOfWords("string_instead_of_list")
        self.assertEqual(bagofwords, {},
                         'Bag_of_words: string ')

class AddDocumentTestCase(CorpusTestCase):
    def runTest(self):
        self.corpus.addDocument(self.corpus_documents[1][0],self.corpus_documents[1][1],self.corpus_documents[1][2])
        self.assertEqual(len(self.corpus.words.keys()), 15,
                         'Add Document: incorrect number of words in the index')
        self.assertEqual(self.corpus.words["saturn"]["2"], 1.0/18,
                         'Add Document: incorrect frequencies of words occurring multiple times')
        self.assertEqual(self.corpus.words["the"]["2"], 4.0/18,
                         'Add Document: incorrect frequencies of words occurring 1 time')

if __name__ == '__main__':
    unittest.main()
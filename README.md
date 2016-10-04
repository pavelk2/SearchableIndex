# SEARCHABLE INDEX
----
**Execution**

```bash
# Download the corpus file
wget CORPUSFILEURL
bunzip2 wikipedia_example.tsv.bz2
# Run the program
./run wikipedia_example.tsv
```
> Python 2.7 is used for the implementation

**Testing**

```bash
# Unit tests
python2.7 -m unittest test.test_index
python2.7 -m unittest test.test_search

# Integration test (requires wikipedia_example.tsv)
python2.7 -m unittest test.test_integration
```
## 1. Conceptual Approach
The problem is decomposed into 2 challenges: 

* **Indexing.** Approach: Inverted index with word frequencies normalized by document size. *Implemented in corpus.py*.
* **Searching.** Approach: Intersection of lists of documents containing each keyword from search query. Search output is top-K from this intersection which is sorted by products of keyword frequencies. *Implemented in search.py*

#### Assumptions made

* **Indexing**
	* the corpus file structure is fixed (id, title, fulltext separated with tabs).
	* the corpus file can fit all into the memory
	* punctuation should not be indexed
	* the same term occurring 1 time in a small document has higher rank than occuring in a bigger document (*frequency / document_size*)
	* words in the index are not stemmed ("run" and "running" are different)

	
* **Searching**
	* is not case sensitive ("Berlin" and "berlin" are equal)
	* search query contains usually more than 1 keyword 	
	* judges keywords as a set and not as a sequence ("The Facebook" and "Facebook The" are equal)
	* no other characters than latin are used

#### Trade-offs
**Performance during Search has higher priority than during Indexing**, so some operations which could be done during Search (normalizing word frequencies by document size) instead are done during indexing.

Because of the time constraints given for this challenge **[record-level inverted index](https://en.wikipedia.org/wiki/Inverted_index)** is implemented not allowing phrase search, rather than word-level inverted index.

**If we assume** queries contain a **single keyword** only we could store for each word **sorted lists** of documents they occur in (making search complexity close to O(1)).
## 2. Performance

#### Runtime performance*
 

* **Indexing** – 1 seconds
* **Searching**
	* 1 rare keyword (e.g. "Berlin") – 1.7 ms
	* 2 rare keywords (e.g. "Berlin Germany") – 1.7ms
	* 1 popular keyword (e.g. "a") – 291ms
	* 1 popular keyword (e.g. "the") – 293ms
	* 2 popular keywords (e.g. "a the") – 299ms

1 doc: 0.1 ms
226 docs: 0.7 ms
86251 docs: 266 ms
84317 docs: 266 ms

> **With the given example of corpus file (~14MLN words) on 
MacBook PRO 2012 2,5 GHz Intel Core i5, 8GB RAM.*

> To see the runtime performance during program execution you can to uncomment #@timeit in *searchindex/index.py* and *searchindex/search.py*

#### Order of complexity 

* **Indexing** O(N), where N - the number of words in corpus
* **Searching** O(N), where N - number of documents associated with a given query.

#### Bottlenecks

Search queries containing **popular words** (such as articles *'a'*, *'the'*), occurring in most of the documents, are executed significantly slower (for each document keyword frequencies products should be calculated and later the list should be sorted to get the top-K in *search()* function).
## 3. Future work

The direction and priorities of the future work depends a lot on the domain where this search index is applied and specific features it should support. Here below we do not assume any particular domain and present features / components to be developed as following:


1. **Phrase search**. Implement word level inverted index storing positions of words in documents to allow phrase search.
2. **Popular words**. Apply TF-IDF approach, where
3. **Index storage (file/DB)**. Indexing corpus is a time consuming operation and we should be able to store our index on a disk rather than in memory all the time.
4. **Changes in indexed documents**. The corpus is not a stable entity and we need ways not only to add new documents but change existing ones.
5. **Encoding**. Enable support for queries in unicode. 
6. **Ranking**. Now when we search for 'Berlin' the main article only appears the 9th. We should utilize document titles in ranking.


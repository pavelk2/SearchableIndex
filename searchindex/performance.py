# timeit is used as a decorator 
# around methods: 
# - Index.indexSourceFile() and 
# - SearchableIndex.search()
# to measure execution time
import time                                                

def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print "-- '%s()' is executed in %.1f ms--" % (method.__name__, 1000*(te-ts))
        return result

    return timed

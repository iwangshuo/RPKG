import nltk

tagged = nltk.corpus.brown.tagged_sents()[0]
entity = nltk.chunk.ne_chunk(tagged)
print(entity)
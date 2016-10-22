# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 17:25:22 2016

@author: Risto
"""

from os import chdir
import glob
chdir(r"C:\Users\Risto\Documents\GitHub\opentartu")
#turn into utf-8 by opening in notepad++ and encoding->Convert to utf-8 BOM

import word2vec

#Run word2phrase to group up similar words "Los Angeles" to "Los_Angeles"
word2vec.word2phrase('pealkirjad.txt', 'word2vec/phrases', verbose=True)   
#This will create a riigiteenused-phrases that we can use as a better input 
#for word2vec. Note that you could easily skip this previous step and use
# the origial data as input for word2vec.Train the model using the 
#word2phrase output.
word2vec.word2vec('word2vec/phrases', 'word2vec/pealkirjad.bin', size=100, verbose=True)
#That generated a riigiteenused.bin file containing the word vectors in a
# binary format. Do the clustering of the vectors based on the trained model.
#That created a text8-clusters.txt with the cluster for every word in the
# vocabulary
model = word2vec.load('word2vec/pealkirjad.bin')

#cosine sim of a word
indexes, metrics = model.cosine('teenus')
model.vocab[indexes] #sim words
model.generate_response(indexes, metrics) #with metrics
model.generate_response(indexes, metrics).tolist()

#other words
indexes, metrics = model.cosine('esitama')
model.generate_response(indexes, metrics).tolist()

#Analogies
indexes, metrics = model.analogy(pos=['teenus', 'teade'], neg=['esitama'], n=10)
indexes, metrics
model.generate_response(indexes, metrics).tolist()

#clusters
clusters = word2vec.load_clusters('riigiteenused/riigiteenused-clusters.txt')
clusters[b'teenus']
clusters.get_words_on_cluster(90).shape
clusters.get_words_on_cluster(90)[:10]

#most similar
from gensim.models import Word2Vec
model = Word2Vec.load_word2vec_format('word2vec/pealkirjad.bin', binary=True)
model.most_similar(positive=['teenus', 'esitama'], negative=['taotlus'])

from matplotlib import pylab
from sklearn.decomposition import PCA

def plot(words):
    %matplotlib inline
    embeddings = [model[w] for w in words]
    
    pca = PCA(n_components=2) 
    two_d_embeddings = pca.fit_transform(embeddings)
    
    pylab.figure(figsize=(5,5))  # in inches
    for i, label in enumerate(words):
        x, y = two_d_embeddings[i,:]
        pylab.scatter(x, y)
        pylab.annotate(label, xy=(x, y), xytext=(5, 2),fontsize=10, textcoords='offset points', ha='right', va='bottom')
        pylab.xlabel("principal component 1")
        pylab.ylabel("principal component 2")
    #pylab.savefig("word2vec.jpg")
    #pylab.close() 
    pylab.show()

plot("andmine loa kinnitamine valimine".split())
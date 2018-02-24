from gensim.models import Word2Vec
from gensim.parsing import preprocessing
import numpy as np
from scipy import spatial
import pickle

with open('docvectors.pickle', 'rb') as f:
    docvectors = pickle.load(f)

model = Word2Vec.load('w2v_model2')


def preprocess_sentence(sentence):
    sentence = preprocessing.strip_punctuation(sentence)
    sentence = preprocessing.stem_text(sentence)
    sentence = preprocessing.remove_stopwords(sentence)
    sentence = sentence.split()
    return sentence


def get_jokes(question):
    """ Return 5 jokes """
    rated = []

    # Transform question into vector
    question = preprocess_sentence(question)
    try:
        question.remove('joke')
        question.remove('tell')
        question.remove('give')
        question.remove('say')
        question.remove('talk')
        question.remove('provide')
    except:
        pass
    curr_vec = np.zeros(100)
    for token in question:
        try:
            vector = model.wv[token]
        except KeyError:
            vector = np.zeros(100)
        curr_vec = np.add(curr_vec, vector)
    questionvector = np.divide(curr_vec, len(question))

    # Compare questionvector with all docvectors and sort by similarity
    for vec, sentence in docvectors:
        try:
            result = 1 - spatial.distance.cosine(questionvector, vec)
            rated.append((result, sentence))
        except ValueError:
            pass
    result = sorted(rated, key=lambda x: x[0], reverse=True)
    result = ['[{}] {}'.format(round(r[0], 2), r[1]) for r in result[:5]]
    result = ['Ok. Here are 5 jokes for you:'] + result
    result = '\n\n'.join(result)
    return result

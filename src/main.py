import numpy as np

from src import gensim_test


def numberarray(length, number):
    array = []
    for i in range(0, length):
        array.append(number)
    return array


#
# array = numberarraywithlengthandnumber(10, 3)
# for tmp in array :
#     print tmp

LabeledSentence = gensim_test.models.doc2vec.LabeledSentence

from sklearn.cross_validation import train_test_split

with open('../yewu.txt', 'r') as infile:  # 0
    yewu_reviews = infile.readlines()
with open('../chanpin.txt', 'r') as infile:  # 1
    chanpin_reviews = infile.readlines()
with open('../qita.txt', 'r') as infile:  # 2
    qita_reviews = infile.readlines()
with open('../pingtai.txt', 'r') as infile:  # 3
    pingtai_reviews = infile.readlines()
with open('../fuwu.txt', 'r') as infile:  # 4
    fuwu_reviews = infile.readlines()
with open('../reviews.txt', 'r') as infile:
    unsup_reviews = infile.readlines()

# use 1 for positive sentiment, 0 for negative
y = np.concatenate((np.zeros(len(yewu_reviews)),
                    np.ones(len(chanpin_reviews)),
                    numberarray(len(qita_reviews), 2),
                    numberarray(len(pingtai_reviews), 3),
                    numberarray(len(fuwu_reviews), 4)
                    ))                               #产生不同大小不同数字的数列代表不同类型，并把它们拼接在一起

x_train, x_test, y_train, y_test = train_test_split(np.concatenate((yewu_reviews,
                                                                    chanpin_reviews,
                                                                    qita_reviews,
                                                                    pingtai_reviews,
                                                                    fuwu_reviews)), y, test_size=0.2)


# # Do some very minor text preprocessing
# def cleanText(corpus):
#     punctuation = """.,?!:;(){}[]"""
#     corpus = [z.lower().replace('\n', '') for z in corpus]
#     corpus = [z.replace('<br />', ' ') for z in corpus]
#
#     # treat punctuation as individual words
#     for c in punctuation:
#         corpus = [z.replace(c, ' %s ' % c) for z in corpus]
#     corpus = [z.split() for z in corpus]
#     return corpus
#
#
# x_train = cleanText(x_train)
# x_test = cleanText(x_test)
# unsup_reviews = cleanText(unsup_reviews)


# Gensim's Doc2Vec implementation requires each document/paragraph to have a label associated with it.
# We do this by using the LabeledSentence method. The format will be "TRAIN_i" or "TEST_i" where "i" is
# a dummy index of the review.

def labelizeReviews(reviews, label_type):
    labelized = []
    for i, v in enumerate(reviews):
        label = '%s_%s' % (label_type, i)
        labelized.append(LabeledSentence(v, [label]))
    return labelized


x_train = labelizeReviews(x_train, 'TRAIN')
x_test = labelizeReviews(x_test, 'TEST')
unsup_reviews = labelizeReviews(unsup_reviews, 'UNSUP')

# Step 2

size = 400

# instantiate our DM and DBOW models
model_dm = gensim_test.models.Doc2Vec(min_count=1, window=10, size=size, sample=1e-3, negative=5, workers=3)
model_dbow = gensim_test.models.Doc2Vec(min_count=1, window=10, size=size, sample=1e-3, negative=5, dm=0, workers=3)

# build vocab over all reviews
model_dm.build_vocab(np.concatenate((x_train, x_test, unsup_reviews)))
model_dbow.build_vocab(np.concatenate((x_train, x_test, unsup_reviews)))

# We pass through the data set multiple times, shuffling the training reviews each time to improve accuracy.
all_train_reviews = np.concatenate((x_train, unsup_reviews))
for epoch in range(10):
    perm = np.random.permutation(all_train_reviews.shape[0])
    model_dm.train(all_train_reviews[perm])
    model_dbow.train(all_train_reviews[perm])


# Get training set vectors from our models
def getVecs(model, corpus, size):
    vecs = [np.array(model[z.labels[0]]).reshape((1, size)) for z in corpus]
    return np.concatenate(vecs)


train_vecs_dm = getVecs(model_dm, x_train, size)
train_vecs_dbow = getVecs(model_dbow, x_train, size)

train_vecs = np.hstack((train_vecs_dm, train_vecs_dbow))

# train over test set
x_test = np.array(x_test)

for epoch in range(10):
    perm = np.random.permutation(x_test.shape[0])
    model_dm.train(x_test[perm])
    model_dbow.train(x_test[perm])

# Construct vectors for test reviews
test_vecs_dm = getVecs(model_dm, x_test, size)
test_vecs_dbow = getVecs(model_dbow, x_test, size)

test_vecs = np.hstack((test_vecs_dm, test_vecs_dbow))

# Step 3
from sklearn.linear_model import SGDClassifier

lr = SGDClassifier(loss='log', penalty='l1')
lr.fit(train_vecs, y_train)

print 'Test Accuracy: %.2f' % lr.score(test_vecs, y_test)

# Step 4

# Create ROC curve
from sklearn.metrics import roc_curve, auc
# %matplotlib inline
import matplotlib.pyplot as plt

pred_probas = lr.predict_proba(test_vecs)[:, 1]

fpr, tpr, _ = roc_curve(y_test, pred_probas)
roc_auc = auc(fpr, tpr)
plt.plot(fpr, tpr, label='area = %.2f' % roc_auc)
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.legend(loc='lower right')

plt.show()


# Step 5

# from NNet import NeuralNet
#
# nnet = NeuralNet(50, learn_rate=1e-2)
# maxiter = 500
# batch = 150
# _ = nnet.fit(train_vecs, y_train, fine_tune=False, maxiter=maxiter, SGD=True, batch=batch, rho=0.9)
#
# print 'Test Accuracy: %.2f'%nnet.score(test_vecs, y_test)

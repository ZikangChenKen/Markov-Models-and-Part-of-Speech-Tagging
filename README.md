# Markov-Models-and-Part-of-Speech-Tagging
One class of tagging algorithms is stochastic taggers. Such taggers generally resolve tagging ambiguities by using a training corpus to compute the probabilities that constitute the parameters of a statistical model, such as the HMM POS tagger that we will see below. The trained tagger is then applied to a test corpus that is different from the training corpus. The accuracy of the POS tagger is quantiﬁed by computing the percentage of all tags in the test set where the tagger and the “true” tags agree. The question, of course, is: How do we know the true tags? One way is to use a human-tagged gold standard test set, where experts do manual tagging of the corpus. Various sources of such data exist (alas, not freely available), such as the Penn Treebank and WSJ Corpus. In this repo, we will develop a stochastic POS tagger based on hidden Markov models (HMMs).

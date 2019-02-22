from nltk import word_tokenize, sent_tokenize


class SentenceFilter:

    def __init__(self,text):
        self.text = text
        self.logic_sentences = []
        self.description_sentences = []

    def filter_sentences(self):
        conditional_conjunctions = ['because', 'before', 'but', 'even if', 'if', 'if only', 'once', 'only if','only'
                                    'on the condition that', 'provided' , 'since', 'therefore', 'unless',
                                    'until', 'when', 'then']
        tokenized_sentences = [token for token in sent_tokenize(self.text)]
        print(tokenized_sentences)

        for sent in tokenized_sentences:
            lower_sent = sent.lower()
            print(sent)
            for word in conditional_conjunctions:
                if word in word_tokenize(lower_sent):
                    self.logic_sentences.append(sent)
                    break

        self.description_sentences = list(set(tokenized_sentences) - set(self.logic_sentences))
        print(self.description_sentences)

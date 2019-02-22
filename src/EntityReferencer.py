from nltk import word_tokenize, sent_tokenize, pos_tag, ne_chunk, RegexpParser,ne_chunk,Tree


class EntityReferencer:

    def __init__(self,description_list):
        self.description_list = description_list
        self.referencing_Dic = {}

    def refer_entities(self):

        tagged_sentences = [pos_tag(word_tokenize(token)) for token in self.description_list]
        print(tagged_sentences)
        words = []
        for word_token in tagged_sentences:
            noun_list = []
            for tag, pos in word_token:
                if (pos == 'NNP' or pos == 'NNS') & (tag not in noun_list):
                    noun_list.append(tag)

            words.append(noun_list)
        for nounList in words:
            for noun in nounList:
                pos = pos_tag(word_tokenize(noun))
                if pos[0][1] == "NNS":
                    self.referencing_Dic[pos[0][0]] = ""
                    for word in nounList:
                        if word != pos[0][0]:
                            if self.referencing_Dic[pos[0][0]] != "":
                                self.referencing_Dic[pos[0][0]] = self.referencing_Dic[pos[0][0]]+ " and " +word
                            else:
                                self.referencing_Dic[pos[0][0]] = word

        print(self.referencing_Dic)

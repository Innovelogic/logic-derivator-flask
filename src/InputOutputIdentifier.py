from nltk import word_tokenize, sent_tokenize
import re
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer


class InputOutputIdentifier:
    outputIndicators = ['then', 'will', 'activate','generate', 'create', 'give', 'turn', 'operate', 'start','unlock','to','ring']
    inputIndicators = ['and','or','if','only','when','either','all']

    def __init__(self, entity_set,text):
        self.entity_set = entity_set
        self.text = text
        self.input_set = set()
        self.output_set = set()
        self.neighbour_dic = {}

    def neighbourhood_based_identification(self):
        # ps = PorterStemmer()
        lemma = WordNetLemmatizer()
        sentences = re.split(r'[,.]', self.text)
        for entity in self.entity_set:
            self.neighbour_dic[entity] = []
            for sentence in sentences:
                r1 = re.search(r"(?:[a-zA-Z'-]+[^a-zA-Z'-]+){0,3}" + entity + "(?:[^a-zA-Z'-]+[a-zA-Z'-]+){0,3}",sentence)
                if r1 is None:
                    continue
                else:
                    for i in word_tokenize(r1.group()):
                        self.neighbour_dic[entity].append(i)
                    # self.neighbour_dic[entity]= self.neighbour_dic[entity]+word_tokenize(r1.group())

        for entity in self.entity_set:
            neighbours = self.neighbour_dic[entity]
            # print(neighbours)

            stem_neighbours = []
            #print(neighbours)
            for neighbour in neighbours:
                stem_neighbours.append(lemma.lemmatize(neighbour, pos = 'v'))
            #print(stem_neighbours)
            for stem_neighbour in stem_neighbours:
                if stem_neighbour in InputOutputIdentifier.inputIndicators:  # check whether a stem word is inside input indicators
                    self.input_set.add(entity)
                    break

                elif stem_neighbour in InputOutputIdentifier.outputIndicators:  # check whether a stem word is inside output indicators
                    self.output_set.add(entity)
                    break




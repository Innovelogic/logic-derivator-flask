import EntityExtractor,InputOutputIdentifier
from EntityExtractor import *
from InputOutputIdentifier import *
from EntityReferencer import *
from SentenceFilter import *
import re,nltk

from boolean_expression_creator import BooleanExpressionCreator as bEC
from truth_table_creator import TruthTableCreator as tTCreator
from relations_extractor import RelationsExtractorSecond as rES
from sentence_generator import SentenceGenerator as sG



def conversion_method(sentences,input_output_identifier):

    # print("Example :", example_sentence)
    # print("Inputs :", input_output_identifier.input_set)
    # print("Outputs :", input_output_identifier.output_set)

    input_output_dic = {}
    x = ord('A')
    for input in input_output_identifier.input_set:
        input_output_dic['I' + chr(x)] = input
        x = x + 1

    x = ord('Z')
    for output in input_output_identifier.output_set:
        input_output_dic['O' + chr(x)] = output
        x = x - 1
    print(input_output_dic)
    conversion = sentences
    for word in input_output_dic:
        conversion = conversion.replace(input_output_dic[word], input_output_dic[word]+" [" + word+"]")

    return conversion

def do_conversion(given_text):
    # Create sentence filter object
    sentence_filter = SentenceFilter(given_text)

    # Filtering sentences for description sentences and to logic sentences
    sentence_filter.filter_sentences()

    if sentence_filter.description_sentences:
        # Create referencer object
        entity_referencer = EntityReferencer(sentence_filter.description_sentences)
    else:
        # Create referencer object
        entity_referencer = EntityReferencer(sentence_filter.logic_sentences)

    # Refer entities
    entity_referencer.refer_entities()

    # Replace logic sentences with references
    sample_sentences = " ".join(sentence for sentence in sentence_filter.logic_sentences)
    for word in entity_referencer.referencing_Dic:
        sample_sentences = sample_sentences.replace(word, entity_referencer.referencing_Dic[word])


    entity_extractor = EntityExtractor(sample_sentences)
    entity_extractor.extraction_verb_based()
    print(entity_extractor.entitySet)

    print(sample_sentences)
    input_output_identifier = InputOutputIdentifier(entity_extractor.entitySet,sample_sentences)
    input_output_identifier.neighbourhood_based_identification()

    print("Example :",given_text)
    print("Inputs :",input_output_identifier.input_set)
    print("Outputs :",input_output_identifier.output_set)
    # results =[list(input_output_identifier.input_set),list(input_output_identifier.output_set)]


    # First Phase #
    total_inputs_count = len(input_output_identifier.input_set)
    total_outputs_count = len(input_output_identifier.output_set)

    # ff = open('dummy_input_first.txt')
    #ff = conversion_method(sample_sentences, input_output_identifier)
    ff = "If the IC=1 or IB=1 is giving a signal, then OZ=1 is sounded. If the IB=1 or IA=1 is giving a signal, then OY=1 is sounded. If two or more IA=1 and IB=1 and IC=1 are giving a signal, then OX=1 is sounded."


    sentences_ff = nltk.tokenize.sent_tokenize(ff)
    inputs_names, outputs_names = sG.inputs_outputs_name_extractor(sentences_ff)  # Getting Inputs and outputs name
    # Ex:- ["A", "B", "C"] for inputs and ["Z", "Y"] for outputs  # When inputs count less than total inputs count,
    # sentence generator will fill inputs for the inputs which are haven't values.

    # print(inputs_names)
    # print(outputs_names)

    #  Checks the inputs outputs conts from sentences regex search for every inputs and outputs
    if total_inputs_count > len(inputs_names):
        print("Inputs names are not completed")
    elif total_inputs_count < len(inputs_names):
        print("Inputs count is wrong")

    if total_outputs_count > len(outputs_names):
        print("Outputs names are not completed")
    elif total_outputs_count < len(outputs_names):
        print("Outputs count is wrong")

    for i in sentences_ff:
        value = sG.inputs_counter_checker(total_inputs_count, i)
        # print(value)
        if 0 < len(re.findall("^ONLY", i)):
            "ToDo - ONLY keyword"
            pos_tagged_sentence = sG.nltk_applier(i)
            # print(nla_output)
            result, sub_result, rule = sG.rules_checker(pos_tagged_sentence)
            if result.height() > 2:
                # print(result, sub_result, rule)
                print("RULE number is = ", rule)
                rule_number = int(rule[5:7])  # getting integer value of the rule string ex:- RULE 05: => 05
                new_sentences = sG.sentence_generator(i, pos_tagged_sentence, result, sub_result, total_inputs_count,
                                                      total_outputs_count, inputs_names, outputs_names, rule_number)
        if value:
            "Write on the output without any change"
            "ToDo"
        else:
            "ToDo - can't write"

    # # Second Phase #
    # #
    # fs = open('dummy_input_second.txt')
    # fs = fs.read()

    sentences_fs = nltk.tokenize.sent_tokenize(ff)

    # print(sentences[0])

    inputs, outputs = rES.sentence_inputs_outputs_cont(sentences_fs[0])

    empty_truth_table = tTCreator.truth_table_generator(inputs, outputs)

    truth_table = tTCreator.initial_tuple_inputs_insert(inputs, empty_truth_table)

    for i in range(len(sentences_fs)):
        inputs_array, outputs_array = rES.relations_extractor(inputs, outputs, sentences_fs[i])
        if i == 0:
            truth_table = tTCreator.header_tuple_adder(inputs, outputs, inputs_array, outputs_array, truth_table)
        truth_table = rES.output_writer(inputs, outputs, inputs_array, outputs_array, truth_table)

    print("Truth Table : ", truth_table)

    boolean_expression = bEC.boolean_expression_generator(truth_table)
    print("Boolean Expression : ", boolean_expression)
    results = [given_text,"Boolean Expression : " + boolean_expression]
    return results
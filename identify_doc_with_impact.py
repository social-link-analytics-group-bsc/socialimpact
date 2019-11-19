from collections import defaultdict
from nltk import word_tokenize, pos_tag, corpus
from nltk.tokenize import sent_tokenize
from utils import normalize, remove_url_from_text, lemmatize_words, remove_non_ascii, remove_extra_spaces

import csv
import nltk
import pathlib
import pdftotext
import os
import re
import spacy


def build_impact_dictionary(file_dir):
    impact_words_file_name = pathlib.Path(file_dir, 'impact_words.csv')
    impact_words, i_verbs, i_nouns = [], [], []
    with open(str(impact_words_file_name), 'r') as f:
        file = csv.DictReader(f, delimiter=',')
        for line in file:
            if line['pos'] == 'verb':
                lemma_words = ' '.join(lemmatize_words(normalize(line['word']), pos=corpus.wordnet.VERB))
                i_verbs.append(lemma_words)
            if line['pos'] == 'noun':
                lemma_words = ' '.join(lemmatize_words(normalize(line['word']), pos=corpus.wordnet.NOUN))
                i_nouns.append(lemma_words)
    impact_words = [i_verb + ' ' + i_noun for i_verb in i_verbs for i_noun in i_nouns if i_verb != i_noun]
    return impact_words


def get_processed_files(file_dir):
    processed_files_file_name = pathlib.Path(file_dir, 'processed_files.txt')
    processed_file_names = []
    try:
        with open(str(processed_files_file_name), 'r') as f:
            for line in f.readlines():
                processed_file_names.append(line[:-1])
    except:
        pass
    return processed_file_names


def record_processed_file(file_dir, processed_file_name):
    processed_files_file_name = pathlib.Path(file_dir, 'processed_files.txt')
    with open(str(processed_files_file_name), 'a+') as f:
        f.write(str(processed_file_name)+'\n')


if __name__ == '__main__':
    # download stopwords and corpus
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')
    # load spacy english model
    s_nlp = spacy.load('en')
    # define data directory
    data_dir = 'data'
    output_dir = 'output'
    docs_with_occurrences = 0
    # load impact words
    print('Building impact dictionary...')
    impact_words = build_impact_dictionary(data_dir)
    print(impact_words)
    # get already processed files if there are any
    print('Getting the name of the already processed files...')
    processed_files = get_processed_files(output_dir)
    print(f'Found {len(processed_files)} files which have been already processed and will be ignored...')
    # collect pdfs
    file_extension = '.pdf'
    pdf_file_names = []
    print('Searching for pdf files...')
    for root_name, dir_names, file_names in os.walk(data_dir):
        for file_name in file_names:
            # check if file_name is a pdf
            if file_name.endswith(file_extension):
                # found a pdf
                file_path = pathlib.Path(root_name, file_name)
                if str(file_path) not in processed_files:
                    pdf_file_names.append((file_name, file_path))
    total_pdfs = len(pdf_file_names)
    print(f'Found {total_pdfs} pdf files...')
    # search occurrences of impact words
    processed_data = dict()
    pos_tags = {'nouns': ['NN', 'NNS', 'NNP', 'NNPS'],
                'verb': ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']}
    # loop through all pdf files
    for i, name_and_path in enumerate(pdf_file_names):
        pdf_file_name, file_path = name_and_path
        print(f'({i+1}/{total_pdfs}) Looking for mention of impact in the pdf file: {file_path}')
        processed_data[pdf_file_name] = {'path': file_path, 'impact_occurrences': []}
        with open(file_path, 'rb') as f:
            pdf = pdftotext.PDF(f)
        # loop over pdf pages
        pdf_pages = len(pdf)
        for page_num in range(0, pdf_pages):
            page_text = remove_url_from_text(pdf[page_num])
            # iterate over sentences and clean them
            sentences = sent_tokenize(page_text)
            clean_sentences = []
            for sentence in sentences:
                normalized_sentence = normalize(sentence)
                # process sentence dependency
                sentence_to_nlp = remove_non_ascii(sentence)
                sentence_to_nlp = remove_extra_spaces(sentence_to_nlp)
                nlp_sentence = s_nlp(' '.join(sentence_to_nlp))
                sentence_dependencies = defaultdict(list)
                for nlp_token in nlp_sentence:
                    token_text, token_tag, token_dependency_type, token_dependent_text, token_dependent_tag = \
                        nlp_token.text, nlp_token.tag_, nlp_token.dep_, nlp_token.head.text, nlp_token.head.tag_
                    if token_tag[0] == 'N' and token_dependency_type == 'dobj' and token_dependent_tag[0] == 'V':
                        lemma_dependent = ' '.join(lemmatize_words(token_dependent_text))
                        lemma_token = ' '.join(lemmatize_words(token_text, pos=corpus.wordnet.NOUN))
                        sentence_dependencies[lemma_dependent].append(lemma_token)
                tagged_tokens = pos_tag(normalized_sentence)
                lemma_tokens = []
                for tagged_token in tagged_tokens:
                    token, tag = tagged_token
                    if tag[0] == 'N':
                        lemma_token = lemmatize_words(token, pos=corpus.wordnet.NOUN)
                        lemma_tokens.append(' '.join(lemma_token))
                    if tag[0] == 'V':
                        lemma_token = lemmatize_words(token, pos=corpus.wordnet.VERB)
                        lemma_tokens.append(' '.join(lemma_token))
                lemma_sentence = ' '.join(lemma_tokens)
                occurrences = set()
                for impact_word in impact_words:
                    impact_tokens = word_tokenize(impact_word)
                    reg_verb, reg_noun = impact_tokens[0], ' '.join(impact_tokens[1:])
                    #if reg_verb == 'provide':
                    #    pass
                    reg_exp = r'^[\w\s]+{verb}\s[\w\s]*{noun}[\w\s]*$'.format(verb=reg_verb, noun=reg_noun)
                    if re.search(reg_exp, lemma_sentence):
                        if sentence_dependencies.get(reg_verb):
                            if reg_noun in sentence_dependencies[reg_verb]:
                                occurrences.add(impact_word)
                    #occurrences_counter = 0
                    #for impact_token in impact_tokens:
                    #    if impact_token in lemma_tokens:
                    #        occurrences_counter += 1
                    #if occurrences_counter == len(impact_tokens):
                    #    occurrences.append(impact_word)
                    #    break
                if len(occurrences) > 0:
                    found_sentence = ' '.join(sentence_to_nlp)
                    found_impact_word = ', '.join(occurrences)
                    print(f'Impact found =======\nSentence: {found_sentence}\nImpact word: {found_impact_word}\n')
                    processed_data[pdf_file_name]['impact_occurrences'].append(
                        {
                            'page': page_num + 1,
                            'sentence': found_sentence,
                            'found_tokens': found_impact_word
                        }
                    )


                #clean_sentences.append(' '.join(normalized_sentence))
            # iterate over clean sentences and find occurrences
            #for clean_sentence in clean_sentences:
            #    sentence_tokens = word_tokenize(clean_sentence)




                #nouns, verbs = [], []

                    # take only nouns and verbs
                #    token, tag = tagged_token
                #    if tag in pos_tags['nouns']:
                #        nouns.append(token)
                #    if tag in pos_tags['verb']:
                #        verbs.append(token)
                # found_tokens = []
                # for verb in verbs:
                #     lemma = ' '.join(lemmatize_verbs(verb.split()))
                #     if lemma in impact_words['verb']:
                #         found_tokens.append(verb)
                # if len(found_tokens) > 0:
                #     found_nouns = []
                #     for noun in nouns:
                #         base_noun = ' '.join(stem_words(noun.split()))
                #         if base_noun in impact_words['noun']:
                #             found_nouns.append(noun)
                #     found_tokens.extend(found_nouns)
                #     print(f'Found {len(found_tokens)} potential occurrence of impact')
                #     processed_data[pdf_file_name]['impact_occurrences'].append(
                #         {
                #             'page': page_num,
                #             'sentence': clean_sentence,
                #             'found_tokens': ', '.join(found_tokens)
                #         }
                #     )
        if len(processed_data[pdf_file_name]['impact_occurrences']) > 0:
            docs_with_occurrences += 1
        record_processed_file(output_dir, file_path)
    print(f'Found occurrences in {docs_with_occurrences} of the {len(pdf_file_names)} pdfs')
    # save results in a csv file
    print('Recording results in a CSV file...')
    output_file_name = 'output/impacts_found.csv'
    with open(output_file_name, 'w', encoding='utf-8') as f:
        headers = ['file', 'path', 'page', 'sentence', 'impact mention']
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for file_name, metadata in processed_data.items():
            for occurrence in metadata['impact_occurrences']:
                record_to_save = {
                    'file': file_name,
                    'path': metadata['path'],
                    'page': occurrence['page'],
                    'sentence': occurrence['sentence'],
                    'impact mention': occurrence['found_tokens']
                }
                writer.writerow(record_to_save)
    print(f'Processed finished successfully. Please find the results in {output_file_name}')
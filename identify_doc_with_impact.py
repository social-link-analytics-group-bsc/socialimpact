from collections import defaultdict
from nltk import word_tokenize, pos_tag
from nltk.tokenize import sent_tokenize
from utils import normalize, remove_url_from_text, lemmatize_verbs, stem_words

import csv
import nltk
import pathlib
import pdftotext
import os


def build_impact_dictionary(file_dir):
    impact_words_file_name = pathlib.Path(file_dir, 'impact_words.csv')
    impact_words, i_verbs, i_nouns = [], [], []
    with open(str(impact_words_file_name), 'r') as f:
        file = csv.DictReader(f, delimiter=',')
        for line in file:
            base_word = ' '.join(stem_words(normalize(line['word'])))
            if line['pos'] == 'verb':
                i_verbs.append(base_word)
            if line['pos'] == 'noun':
                i_nouns.append(base_word)
    for i_verb in i_verbs:
        for i_noun in i_nouns:
            impact_word = i_verb + ' ' + i_noun
            impact_words.append(impact_word)
    return impact_words


if __name__ == '__main__':
    # download stopwords and corpus
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')
    # define data directory
    data_dir = 'data'
    docs_with_occurrences = 0
    # load impact words
    print('Building impact dictionary...')
    impact_words = build_impact_dictionary(data_dir)
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
                pdf_file_names.append((file_name, file_path))
    print(f'Found {len(pdf_file_names)} pdf files...')
    # search occurrences of impact words
    processed_data = dict()
    pos_tags = {'nouns': ['NN', 'NNS', 'NNP', 'NNPS'],
                'verb': ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']}
    # loop through all pdf files
    for pdf_file_name, file_path in pdf_file_names:
        print(f'Looking for mention of impact in the pdf file: {file_path}')
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
                clean_sentences.append(' '.join(normalized_sentence))
            # iterate over clean sentences and find occurrences
            for clean_sentence in clean_sentences:
                sentence_tokens = word_tokenize(clean_sentence)
                base_sentence = ' '.join(stem_words(sentence_tokens))
                #tagged_sentence = pos_tag(sentence_tokens)
                #nouns, verbs = [], []
                #for tagged_token in tagged_sentence:
                    # take only nouns and verbs
                #    token, tag = tagged_token
                #    if tag in pos_tags['nouns']:
                #        nouns.append(token)
                #    if tag in pos_tags['verb']:
                #        verbs.append(token)
                found_tokens = []
                for verb in verbs:
                    lemma = ' '.join(lemmatize_verbs(verb.split()))
                    if lemma in impact_words['verb']:
                        found_tokens.append(verb)
                if len(found_tokens) > 0:
                    found_nouns = []
                    for noun in nouns:
                        base_noun = ' '.join(stem_words(noun.split()))
                        if base_noun in impact_words['noun']:
                            found_nouns.append(noun)
                    found_tokens.extend(found_nouns)
                    print(f'Found {len(found_tokens)} potential occurrence of impact')
                    processed_data[pdf_file_name]['impact_occurrences'].append(
                        {
                            'page': page_num,
                            'sentence': clean_sentence,
                            'found_tokens': ', '.join(found_tokens)
                        }
                    )
        if len(processed_data[pdf_file_name]['impact_occurrences']) > 0:
            docs_with_occurrences += 1
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
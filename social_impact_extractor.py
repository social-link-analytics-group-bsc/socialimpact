from nltk.tokenize import sent_tokenize
from utils import remove_extra_spaces

import click
import csv
import pathlib
import re


@click.command()
@click.option('--input_file_path', help='Path to CSV file that contains mentions of social impact')
@click.option('--column_name', help='Column name that should be analyzed in the CSV file')
@click.option('--source_name', help='Name of the data source')
@click.option('--overwrite_output', help='Whether or not the output file should be overwritten', default=False,
              is_flag=True)
def extract_sentence(input_file_path, column_name, source_name, overwrite_output):
    output_dir = 'output'
    # social impact sentences
    si_sentence_list, no_si_sentence_list = [], []
    # iterate over row to identify sentences that contains '____'
    print(f"Iterating over evidence and searching for sentences of social impact...")
    with open(str(input_file_path), 'r') as f:
        file = csv.DictReader(f, delimiter=',')
        for line in file:
            evidence = line[column_name]
            sentence_list = sent_tokenize(evidence)
            for sentence in sentence_list:
                # remove extra spaces
                sentence = ' '.join(remove_extra_spaces(sentence.split()))
                if re.search(r'[_]{2,}', sentence):
                    # remove special characters
                    sentence = re.sub(r'[_]{2,}', '', sentence)
                    si_sentence_list.append(sentence)
                else:
                    no_si_sentence_list.append(sentence)
    print(f"Found {len(si_sentence_list)} sentences of social impact")
    output_file_name = pathlib.Path(output_dir, 'output_sentence_extractor.csv')
    print(f"Saving social impact sentence into the file {str(output_file_name)}")
    # Save found sentences in csv file
    if overwrite_output:
        write_type = 'w+'
    else:
        write_type = 'a+'
    with open(output_file_name, write_type, encoding='utf-8') as f:
        headers = ['sentence', 'source', 'label']
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for si_sentence in si_sentence_list:
            record_to_save = {
                'sentence': si_sentence,
                'source': source_name,
                'label': 'social_impact'
            }
            writer.writerow(record_to_save)
        for no_si_sentence in no_si_sentence_list:
            record_to_save = {
                'sentence': no_si_sentence,
                'source': source_name,
                'label': 'no_social_impact'
            }
            writer.writerow(record_to_save)
    print('Process finished successfully')


if __name__ == '__main__':
    extract_sentence()

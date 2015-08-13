#!/usr/bin/env python3

__author__ = 'Anton Melnikov'
# http://ostensible.me

from collections import OrderedDict
import json
from pprint import pprint

from phoneme import Phoneme, FeatureValue


def print_distinctive_features(phoneme: Phoneme):
    for feature, value in phoneme:
        if value is FeatureValue.yes:
            output_value = '+'
        elif value is FeatureValue.no:
            output_value = '-'
        elif value is FeatureValue.both:
            output_value = '±'
        else:
            # this feature is unspecified, skip it
            continue

        print('{}{}'.format(output_value, feature))

def show_phoneme(symbol, phonemes):
    phoneme = phonemes[symbol]
    print(phoneme.name)
    print_distinctive_features(phoneme)

def show_intersection(symbols, phonemes):
    first, *rest = symbols
    current_intersection = phonemes[first]
    for symbol in rest:
        next_phoneme = phonemes[symbol]
        current_intersection = current_intersection.intersection(next_phoneme)
        print(current_intersection.parent_similarity)

    print_distinctive_features(current_intersection)
    pprint(list(current_intersection.get_positive_features()))

def process_input(input_to_process: str, phonemes):
    if ' ' in input_to_process:
        symbols = input_to_process.split()
        show_intersection(symbols, phonemes)
    else:
        show_phoneme(input_to_process, phonemes)

def initialise():
    with open('phonemes.json') as phonemes_file:
        phoneme_dict = json.load(phonemes_file, object_pairs_hook=OrderedDict)

    phonemes = {symbol: Phoneme.from_symbol(symbol, phoneme_dict)
                for symbol in phoneme_dict}

    return phonemes

if __name__ == '__main__':

    phonemes = initialise()

    while True:
        user_input = input('> ')
        try:
            process_input(user_input, phonemes)
        except KeyError as e:
            print(e, 'is not in the database')

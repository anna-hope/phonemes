#!/usr/bin/env python3

__author__ = 'Anton Melnikov'
# http://ostensible.me

from collections import Counter
from itertools import chain
from enum import Enum
import json
from pprint import pprint


class FeatureValue(Enum):
    """
    enum for values of phonological features
    """
    yes = 1
    no = 0
    both = 2
    unspecified = -1


class PhonemeElement:

    def __init__(self, symbol, name, features, is_complete=True,
                 parent_phonemes: set=None, feature_counter: Counter=None,
                 parent_similarity=1.0):
        """
        :param is_complete: indicates whether the object represents a complete phoneme
        """
        self.value = self.parse_features(features)

        self.symbol = symbol
        self.name = name
        self.is_complete = is_complete

        if parent_phonemes:
            self.parent_phonemes = parent_phonemes
        if not parent_phonemes:
            self.parent_phonemes = Counter((self.symbol,))

        if feature_counter:
            self.feature_counter = feature_counter
        else:
            self.feature_counter = Counter(self.value)

        # the count of how similar the parent phonemes are
        self.parent_similarity = parent_similarity


    def __repr__(self):
        return self.symbol

    def __str__(self):
        return self.symbol

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        if other:
            return self.value == other.value
        else:
            # the other must be None
            return False

    def __len__(self):
        return len(self.value)

    def __contains__(self, item):
        return item in self.value

    def __iter__(self):
        return iter(self.value)



    @classmethod
    def from_symbol(cls, symbol: str, phonemes: dict):
        phoneme = phonemes[symbol]
        name = phoneme['name']
        features = cls.parse_features(phoneme['features'])
        return cls(symbol, name, features)


    @staticmethod
    def parse_features(features_dict) -> frozenset:
        if isinstance(features_dict, frozenset):
            return features_dict

        features = []
        for feature, value in features_dict.items():

            # values can be True, False, 0 or ±

            if value is True:
                feature_value = FeatureValue.yes
            elif value is False:
                feature_value = FeatureValue.no
            elif value is 0:
                feature_value = FeatureValue.unspecified
            elif value == '±':
                feature_value = FeatureValue.both
            else:
                raise ValueError('{} is not recognised'.format(value))

            features.append((feature, feature_value))

        features_set = frozenset(features)
        return features_set


    @property
    def features(self):
        return self.value

    @property
    def strength(self):
        return self.parent_similarity * sum(self.parent_phonemes.values())


    def get_positive_features(self):
        for feature, value in self:
            if value == FeatureValue.yes or value == FeatureValue.both:
                yield feature


    def similarity_ratio(self, other):
        max_feature_value = max(self.feature_counter.values())
        similarity_count = 0
        for feature in other.features:
            this_feature_score = self.feature_counter[feature]
            difference = max_feature_value - this_feature_score
            similarity_count += this_feature_score - difference

        similarity_ratio = similarity_count / sum(self.feature_counter.values())
        return similarity_ratio

    def partial_equals(self, other, threshold=0.7):
        similarity_ratio = self.similarity_ratio(other)

        if similarity_ratio >= threshold:
            return True
        else:
            return False

    def intersection(self, other):
        if self == other:
            return self
        elif other:
            if other.symbol in self.parent_phonemes:
                return self

            intersection = self.value.intersection(other.value)

            # create new parents
            new_parents = Counter(chain(self.parent_phonemes, other.parent_phonemes))

            new_symbol = '/'.join(new_parents)
            new_feature_counter = self.feature_counter + other.feature_counter

            combined_similarity = self.similarity_ratio(other)

            partial_phoneme = PhonemeElement(new_symbol, 'partial phoneme',
                                             intersection, is_complete=False,
                                             parent_phonemes=new_parents,
                                             feature_counter=new_feature_counter,
                                             parent_similarity=combined_similarity)
            return partial_phoneme

        else:
            return None

    def pick_closest(self, other_phonemes):
        closest = max(other_phonemes, key=lambda phoneme: self.similarity_ratio(phoneme))
        return closest

def show_phoneme(symbol, phonemes):
    phoneme = phonemes[symbol]
    print(phoneme.name)
    pprint(sorted(phoneme.get_positive_features()))

def show_intersection(symbols, phonemes):
    first, *rest = symbols
    current_intersection = phonemes[first]
    for symbol in rest:
        next_phoneme = phonemes[symbol]
        current_intersection = current_intersection.intersection(next_phoneme)
        print(current_intersection.parent_similarity)

    print(sorted(current_intersection.get_positive_features()))

def process_input(input_to_process: str, phonemes):
    if ' ' in input_to_process:
        symbols = input_to_process.split()
        show_intersection(symbols, phonemes)
    else:
        show_phoneme(input_to_process, phonemes)

if __name__ == '__main__':

    with open('phonemes.json') as phonemes_file:
        phoneme_dict = json.load(phonemes_file)

    phonemes = {symbol: PhonemeElement.from_symbol(symbol, phoneme_dict) 
                for symbol in phoneme_dict}

    while True:
        user_input = input('> ')
        try:
            process_input(user_input, phonemes)
        except KeyError as e:
            print(e, 'is not in the database')

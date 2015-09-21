__author__ = 'Anton Melnikov'


from collections import Counter, OrderedDict
from enum import Enum
from itertools import chain
from pprint import pprint


class FeatureValue(Enum):
    """
    enum for values of phonological features
    """
    yes = 1
    no = 0
    both = 2
    unspecified = -1

class FeatureValueDict(OrderedDict):
    pass


class Phoneme:

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
            self.parent_phonemes = {symbol}

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
        return iter(self.value.items())



    @classmethod
    def from_symbol(cls, symbol: str, phonemes: dict):
        """
        Initialise a Phoneme object from its IPA symbol, using a dictionary of IPA symbols and features
        :param symbol:
        :param phonemes:
        :return:
        """
        phoneme = phonemes[symbol]
        name = phoneme['name']
        features = cls.parse_features(phoneme['features'])
        return cls(symbol, name, features)


    @staticmethod
    def parse_features(features_dict) -> FeatureValueDict:

        if isinstance(features_dict, FeatureValueDict):
            return features_dict

        features = FeatureValueDict()
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

            features[feature] = feature_value

        return features


    @property
    def features(self):
        return self.value


    def get_positive_features(self):
        for feature, value in self:
            if value == FeatureValue.yes or value == FeatureValue.both:
                yield feature

    def similarity_ratio(self, other):
        """
        computes the similarity between this Phoneme object and another
        :param other: Phoneme
        :return:
        """
        similarity_count = 0
        for feature, feature_value in self:
            other_feature = other.value[feature]

            if other_feature == feature_value:
                similarity_count += 1

            # add 0.5 if either of the features is ± and the other is + or -
            elif other_feature == FeatureValue.both or feature_value == FeatureValue.both:
                if (other_feature != FeatureValue.unspecified
                    and feature_value != FeatureValue.unspecified):
                    similarity_count += 0.5

        similarity_ratio = similarity_count / len(self.features)
        return similarity_ratio


    def partial_equals(self, other, threshold=0.7):
        """
        returns True if this Phoneme object's similarity to another Phoneme object
        is equal to or above the given threshold of similarity
        :param other: Phoneme
        :param threshold: similarity threshold
        :return:
        """
        similarity_ratio = self.similarity_ratio(other)

        if similarity_ratio >= threshold:
            return True
        else:
            return False

    def intersection(self, other):
        """
        Returns an 'intersection phoneme' between this Phone object and another
        :param other: Phoneme
        :return: Phoneme
        """
        if self == other:
            return self
        elif other:
            if other.symbol in self.parent_phonemes:
                return self

            intersection = FeatureValueDict(set(self).intersection(set(other)))

            # create new parents
            new_parents = set(chain(self.parent_phonemes, other.parent_phonemes))

            new_symbol = '/'.join(new_parents)

            combined_similarity = self.similarity_ratio(other)

            partial_phoneme = Phoneme(new_symbol, 'partial phoneme',
                                             intersection, is_complete=False,
                                             parent_phonemes=new_parents,
                                             parent_similarity=combined_similarity)
            return partial_phoneme

        else:
            return None

    def pick_closest(self, other_phonemes):
        """
        Picks the closest Phoneme object (using the similarity ratio) from an iterable of Phoneme objects
        :param other_phonemes: iterable of Phonemes
        :return: Phoneme
        """
        closest = max(other_phonemes, key=lambda phoneme: self.similarity_ratio(phoneme))
        return closest
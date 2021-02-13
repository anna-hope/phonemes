__author__ = 'Anton Melnikov'

from collections import OrderedDict
import json
from pathlib import Path

from .phoneme import Phoneme, FeatureValue

this_path = Path(__file__)
phonemes_path = Path(this_path.parent.parent, 'phonemes.json')

with phonemes_path.open(encoding='utf-8') as phonemes_file:
    phoneme_dict = json.load(phonemes_file, object_pairs_hook=OrderedDict)

phonemes = {symbol: Phoneme.from_symbol(symbol, phoneme_dict)
            for symbol in phoneme_dict}




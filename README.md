This repository hosts a representation of [Jason Riggle's](http://hum.uchicago.edu/~jriggle/) [chart of phonological features](https://dl.dropboxusercontent.com/u/5956329/Riggle/PhonChart_v1212.pdf) version **12.12** in a machine-readable JSON format.
 
The keys in the JSON file are the phonemes' IPA symbols. The values are their English-language name and the binary features from the chart linked above (see the JSON file for an example).

Additionally, this repository provides a script (phonemeviewer.py) which lets you view the phoneme features from the provided JSON file and see what positive (+ or ±) features each phoneme has. Additionally, when given a list of phonemes, the script calculates the 'similarity' between these phonemes and lists the features that every phoneme in the list shares (if any).

Example usage:

    > ð
	voiced dental fricative
	+cons
	-son
	-syl
	-labial
	+coronal
	+ant
	-dist
	+dorsal
	-pharyngeal
	+voice
	-SG
	-CG
	+cont
	-strident
	-lateral
	-del_rel
	-nasal

    > ð ʃ
	0.782608695652174
	-del_rel
	+coronal
	-son
	-syl
	-pharyngeal
	-CG
	-labial
	-SG
	-lateral
	+cont
	-nasal
	+cons
	['coronal', 'cont', 'cons']

The script was written for Python 3.4+, but will probably run on Python 3.3 if the backported enum package from 3.4 is installed. You may use http://ipa.typeit.org/full/ to type the IPA symbols into the script.

Please report any inconsistencies you may find between the JSON file and Jason Riggle's chart, or, better yet, please fix them and create pull requests. Please do not report any errors you may find in Jason Riggle's chart here. Instead, send your comments directly to the author; there is a non-zero chance of him responding to them. Additionally, please let me know if this repository references an outdated version of Jason Riggle's chart.

Big thanks to Rafael Abramovitz for helping me with the creation of a machine-readable version of the chart.

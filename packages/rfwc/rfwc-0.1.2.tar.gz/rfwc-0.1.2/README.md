[![PyPI version](https://badge.fury.io/py/rfwc.svg)](https://badge.fury.io/py/rfwc)
[![Supported Python
versions](https://img.shields.io/pypi/pyversions/rfwc.svg)](https://pypi.org/project/rfwc)
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/DanielYakubov/Red-Flagger-Word-Catcher/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/DanielYakubov/Red-Flagger-Word-Catcher/tree/main)



# Red Flagger Word Catcher 🙅🚩

A simple, dependency-free software that does keyword-based abuse flagging. It is designed with a philosophy of sensitivity and a focus on recall rather than precision. It detects from a term list that contain terms that are discovered through lexicons and corpora containing hate speech, chatbot system abuse, toxicity, violence, and/or general profinity/obscenity. 

## 🚨🚨 Important Note on Keyword Detection Systems 🚨🚨

We highly discourage the use of keyword systems as the only line of defense for toxicity and/or abuse detection. Problems associated with keyword detection systems range from performance issues to socially harmful false positives in cases like reclaimation. This system is encouraged to be used in conjunction with a review process and/or a stronger classification systems such as a deep learning model. 

Examples of suggested, more robust use cases:
- Keyword detection as part of an ensemble.
- Keyword detection -> Deep learning classification on positives (Useful when there's a lot of data and not a lot of compute).
- Using detected keywords as BOW features and then training classical models on said features.

For performance, see `evaluation/`.

## Usage 🔨

For basic usage, all you have to do is:

`$ pip install rfwc`

```
from rfwc import RedFlagger

rf = RedFlagger()
document = "Something hateful"
hate_words = rf.detect_abuse(document)
```

There's also a method to get a bag-of-words from the wordlist:

```
...

hate_bow = rf.get_abuse_vector(document)
```

The library is designed to work with other word lists that are not built-in to the library. This can be managed with the `add_words` and `remove_words` methods. To get the current word list, there is the `get_wordlist` method.

## Directory 📁

- `abuse_flagger/` contains the package code and the main logic.
- `data_building/` contains the code and documentation of how the initial dataset was created.
- `evaluation/` contains the evaluation of the keyword system on the test splits of the corpora used to discover the keywords.

## Dataset Obscurity 😶‍🌫️

The word list is obscured as a base16 representation of the list of hate words. We did not feel comfortable exposing this list and we discourage any non-base16 representations of the wordlist being uploaded elsewhere. For details on dataset creation, see `README.md` in `data_building/`.

## Other Resouces 📚

We acknowledge that there are other great resources and link some of them below:

- [Weaponized Word](https://weaponizedword.org)
- [HurtLex](https://github.com/valeriobasile/hurtlex/tree/master)
- [HateBase](https://hatebase.org)

## Contributions 🤝

We welcome contributions for both the word list and the software using a fork-and-pull model. For additions to the word list, please ensure there are no duplicates or overlaps and that the additional data is obscured in base16. For any new features for the RedFlagger, open an issue for discussion first before opening a pull request.


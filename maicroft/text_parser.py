# -*- coding: utf-8 -*-

import re

from nltk import RegexpParser
from textblob import TextBlob, Word
from textblob.taggers import PatternTagger
from textblob.sentiments import NaiveBayesAnalyzer

from maicroft.words.utility_text_sets import stopwords
from maicroft.words import utility_text_sets

pattern_tagger = PatternTagger()
naive_bayes_analyzer = NaiveBayesAnalyzer()

NOUN = "n"
VERB = "v"
ADV = "r"
ADJ = "a"

class TextParser:
    """
    Utility class for processing text content.
    """

    substitutions = utility_text_sets.substitutions

    # Skip if any of these is the *only* attribute - for instance,
    # "I'm a big fan of Queen" makes sense, but "I'm a fan" doesn't.
    skip_lone_attributes = [
        "fan", "expert", "person", "advocate", "customer",
    ]

    # A select set of attributes we want to exclude.
    skip_attributes = utility_text_sets.skip_attributes

    # A select set of attributes we want to include.
    include_attributes = [
        "geek", "nerd", "nurse", "cook", "student", "consultant", "mom", "dad",
        "marine", "chef", "sophomore", "catholic", "mod",
        # TODO - These make sense only when accompanied by
        # at least another noun
        #"person","enthusiast","fanboy","player","advocate",
    ]

    # Super awesome logic - if noun ends in any of these, it's *probably*
    # something we want to include/exclude. TODO - This is terrible logic,
    # see if we can implement actual NLP.
    include_attribute_endings = (
        "er", "or", "ar", "ist", "an", "ert", "ese", "te", "ot"
    )
    exclude_attribute_endings = ("ing","fucker")

    # "Filler" words (in sentences such as "I think...", "I guess...", etc.)
    skip_verbs = ["were", "think", "guess", "mean"]
    skip_prepositions = ["that"]
    skip_adjectives = ["sure", "glad", "happy", "afraid", "sorry", "certain"]
    skip_nouns = [
        "right", "way", "everything", "everyone", "things", "thing",
        "mine", "stuff", "lot"
    ]

    # Should _N include conjunctions?
    grammar = r"""
        # adverb* verb adverb*
        # - really think, strongly suggest, look intensely
        _VP:
            {<RB.*>*<V.*>+<RB.*>*}

        # determiner adjective noun(s)
        # - a beautiful house, the strongest fighter
        _N0:
            {(<DT>*<JJ.*>*<NN.*>+(?!<POS>))+}
        _N:
            {<_N0>+}

        # noun to/in noun
        # - newcomer to physics, big fan of Queen, newbie in gaming
        _N_PREP_N:
            {<_N>((<TO>|<IN>)<_N>)+}

        # my adjective noun(s)
        # - my awesome phone
        POSS:
            {<PRP\$><_N>}

        # I verb in* adjective* noun
        # - I am a great chef, I like cute animals,
        # - I work in beautiful* New York, I live in the suburbs
        ACT1:
            {<PRP><_VP><IN>*<_N>}

        # Above + to/in noun
        # - I am a fan of Jaymay, I have trouble with flannel
        ACT2:
            {<PRP><_VP><IN>*<_N_PREP_N>}
    """

    chunker = RegexpParser(grammar)

    def clean_up(self, text):
        """
        Removes unnecessary words from text and replaces common
        misspellings/contractions with expanded words.

        """

        for original, rep in self.substitutions:
            text = re.sub(original, rep, text, flags=re.I)
        return text

    def normalize(self, word, tag="N"):
        """
        Normalizes word using given tag. If no tag is given, NOUN is assumed.

        """

        kind = NOUN
        if tag.startswith("V"):
            kind = VERB
        elif tag.startswith("RB"):
            kind = ADV
        elif tag.startswith("J"):
            kind = ADJ
        return Word(word).lemmatize(kind).lower()

    def pet_animal(self, word):
        """
        Returns word if word is in a predefined list of pet animals.

        """

        word = word.lower()
        if re.match(r"\b(dog|cat|hamster|fish|pig|snake|rat|parrot)\b", word):
            return word # TODO:// make the pet_animal function smarter
        else:
            return None

    def family_member(self, word):
        """
        Returns normalized word if word is in a predefined list
        of family members.

        """

        word = word.lower()
        if re.match(r"\b(mom|mother|mum|mommy)\b", word):
            return "mother"
        elif re.match(r"\b(dad|father|pa|daddy)\b", word):
            return "father"
        elif re.match(r"\b(brother|sister|son|daughter)s?\b", word):
            return word
        else:
            return None

    def relationship_partner(self, word):
        """
        Returns word if word is in a predefined list of relationship partners.
        """
        word = word.lower()
        if re.match(r"\b(ex-)*(boyfriend|girlfriend|so|wife|husband)\b", word):
            return word
        else:
            return None

    def gender(self, word):
        """
        Returns normalized word if word is in a predefined list of genders.
        """
        word = word.lower()
        if re.match(r"\b(girl|woman|female|lady|she)\b", word):
            return "female"
        elif re.match(r"\b(guy|man|male|he|dude)\b", word):
            return "male"
        else:
            return None

    def orientation(self, word):
        """
        Returns word if word is in a predefined list of sexual orientations.

        """

        word = word.lower()
        if re.match(r"\b(gay|straight|bi|bisexual|homosexual)\b", word):
            return word
        else:
            return None

    def process_verb_phrase(self, verb_tree):
        """
        Returns list of (word,tag) tuples given a verb tree.

        """

        if verb_tree.label() != "_VP":
            return None
        verb_phrase = [(w.lower(), t) for w, t in verb_tree.leaves()]
        return verb_phrase

    def process_noun_phrase(self, noun_tree):
        """
        Returns list of (word,tag) tuples given a noun tree.

        """

        if noun_tree.label() != "_N":
            return []
        if any(
            n in self.skip_nouns+stopwords
                for n, t in noun_tree.leaves() if t.startswith("N")
        ):
            return []

        noun_phrase = [(w.lower(), t) for w, t in noun_tree.leaves()]
        return noun_phrase

    def process_npn_phrase(self, npn_tree):
        """
        Given a phrase of the form noun-preposition-noun, returns noun
        and preposition-noun phrases.

        """

        if npn_tree.label() != "_N_PREP_N":
            return None
        noun_phrase = []
        prep_noun_phrase = []
        for i in range(len(npn_tree)):
            node = npn_tree[i]
            # we have hit the prepositions in a prep noun phrase
            if type(node) is tuple:
                w, t = node
                w = w.lower()
                prep_noun_phrase.append((w, t))
            else:
                if prep_noun_phrase:
                    prep_noun_phrase += self.process_noun_phrase(node)
                else:
                    noun_phrase = self.process_noun_phrase(node)
        return (noun_phrase, prep_noun_phrase)

    def process_possession(self, phrase):
        """
        Given a phrase, checks and returns a possession/belonging
        (my <word>) if exists.
        """

        noun_phrase = []

        for i in range(len(phrase)):
            node = phrase[i]
            if type(node) is tuple: # word can only be pronoun
                w, t = node
                if t == "PRP$" and w.lower() != "my":
                    return None
            else: # type has to be nltk.tree.Tree
                if node.label() == "_N":
                    noun_phrase = self.process_noun_phrase(node)
                else: # what could this be?
                    pass
        if noun_phrase:
            return {
                "kind" : "possession",
                "noun_phrase" : noun_phrase
            }
        else:
            return None

    def process_action(self, phrase):
        """
        Given a phrase, checks and returns an action
        (I <verb-phrase>) if exists.
        """

        verb_phrase = []
        prepositions = []
        noun_phrase = []
        prep_noun_phrase = []

        for i in range(len(phrase)):
            node = phrase[i]
            if type(node) is tuple: # word is either pronoun or preposition
                w, t = node
                if t == "PRP" and w.lower() != "i":
                    return None
                elif t == "IN":
                    prepositions.append((w.lower(), t))
                else: # what could this be?!
                    pass
            else:
                if node.label() == "_VP":
                    verb_phrase = self.process_verb_phrase(node)
                elif node.label() == "_N":
                    noun_phrase = self.process_noun_phrase(node)
                elif node.label() == "_N_PREP_N":
                    noun_phrase, prep_noun_phrase = (
                        self.process_npn_phrase(node)
                    )
        if noun_phrase:
            return {
                "kind" : "action",
                "verb_phrase" : verb_phrase,
                "prepositions" : prepositions,
                "noun_phrase" : noun_phrase,
                "prep_noun_phrase" : prep_noun_phrase
            }
        else:
            return None

    def extract_chunks(self, text):
        """
        Given a block of text, extracts and returns useful chunks.

        TODO - Should sentiments be excluded here?

        """
        chunks = []
        sentiments = []
        text = self.clean_up(text)
        blob = TextBlob(text, pos_tagger=pattern_tagger, analyzer=naive_bayes_analyzer)

        for sentence in blob.sentences:

            if (not sentence.tags or
                not re.search(r"\b(i|my)\b", str(sentence),re.I)
            ):
                continue

            tree = self.chunker.parse(sentence.tags)

            for subtree in tree.subtrees(
                filter=lambda t: t.label() in ['POSS', 'ACT1', 'ACT2']
            ):
                phrase = [(w.lower(), t) for w, t in subtree.leaves()]
                phrase_type = subtree.label()

                if not any(
                    x in [
                        ("i", "PRP"), ("my", "PRP$")
                    ] for x in [(w, t) for w, t in phrase]
                ) or (
                    phrase_type in ["ACT1", "ACT2"] and (
                        any(
                            word in self.skip_verbs for word in [
                                w for w, t in phrase if t.startswith("V")
                            ]
                        ) or any(
                            word in self.skip_prepositions for word in [
                                w for w, t in phrase if t == "IN"
                            ]
                        ) or any(
                            word in self.skip_adjectives for word in [
                                w for w, t in phrase if t == "JJ"
                            ]
                        )
                    )
                ):
                    continue

                if subtree.label() == "POSS":
                    chunk = self.process_possession(subtree)
                    if chunk:
                        chunks.append(chunk)
                elif subtree.label() in ["ACT1", "ACT2"]:
                    chunk = self.process_action(subtree)
                    if chunk:
                        chunks.append(chunk)

        return (chunks, sentiments)

    def ngrams(self, text, n=2):
        """
        Returns a list of ngrams for given text.
        """
        return [" ".join(w) for w in TextBlob(text).ngrams(n=n)]

    def noun_phrases(self, text):
        """
        Returns list of TextBlob-derived noun phrases.
        """

        return TextBlob(text).noun_phrases

    def common_words(self, text):
        """
        Given a text, splits it into words and returns as a list
        after excluding stop words.
        """

        return [
            word for word in list(TextBlob(text).words) if (
                word not in stopwords and word.isalpha()
            )
        ]

    def total_word_count(self, text):
        """
        Returns total word count of a given text.
        """
        return len(list(TextBlob(text).words))

    def unique_word_count(self, text):
        """
        Returns unique word count of a given text.
        """
        return len(set(list(TextBlob(text).words)))

    def longest_word(self, text):
        """
        Returns longest word in a given text.
        """
        return max((list(TextBlob(text).words)), key=len)

    @staticmethod
    def test_sentence(sentence):
        """
        Prints TextBlob-derived tags for a given sentence.
        For testing purposes only.
        """

        print(TextBlob(sentence).tags)

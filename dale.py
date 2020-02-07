#!/usr/bin/env python
#
# Dale-Chall Approximate Calculator
# (C) 2020 Marquis Kurt. All rights reserved.
#

import json
import argparse
import sys
from string import ascii_letters, digits, ascii_uppercase
from functools import reduce

def get_corpus():
    """Import the list of easy words defined by Dale-Chall in the corpus.json
    file."""
    with open('corpus.json', 'r') as corpus_file:
        return json.load(corpus_file)

class DaleChallCalculator(object):

    def __init__(self):
        self.text = ""
        self.word_count = 0
        self.sentence_count = 0
        self.difficult_words = 0
        self.easy_words = 0
        self.words = []
        self.score = 0
        self.asl = 0

    def get_average_sentence_length(self):
        self.asl = self.word_count / self.sentence_count
        return self.word_count / self.sentence_count

    def get_word_count(self):
        words = []
        texts = list(self.text)
        current_character = ""
        current_word = ""

        while len(texts) > 0:
            current_character = texts.pop(0)

            acceptable = ascii_letters + digits + "'" + "-"

            if current_character not in acceptable:
                words.append(current_word)
                current_word = ""
            else:
                current_word += current_character

        while "" in words:
            words.remove("")

        self.words = words

        self.word_count = len(words)
        return self.word_count

    def get_sentence_count(self):
        characters = list(self.text)
        current_character = ""
        current_sentence = ""
        sentences = []

        while len(characters) > 0:
            current_character = characters.pop(0)

            if current_character in "!?.":
                sentences.append(current_sentence + current_character)
                current_sentence = ""
            else:
                if current_character == "\n":
                    continue
                elif current_sentence == "" and current_character == " ":
                    continue

                current_sentence += current_character
        
        self.sentence_count = len(sentences)
        return sentences

    def get_easy_words(self):
        easy = []
        difficult = []
        new = []

        endings = ["s", "ies", "ing", "n", "ed", "ied", "ly", "er", "ier", "est", "iest"]

        for word in self.words:
            if word.lower() in get_corpus():
                easy.append(word)
            elif word.isdigit():
                easy.append(word)
            elif word in easy:
                easy.append(word)
            elif word in new:
                easy.append(word)
                new.remove(word)
            elif "-" in word:
                temp = word.lower().split("-")
                easy_hyphen = list(map(lambda a: a in get_corpus(), temp))
                if (reduce(lambda a, b: a and b, easy_hyphen)):
                    easy.append(word)
            else:
                for ending in endings:
                    if word.endswith(ending):
                        if word[:(-1*len(ending))] in get_corpus():
                            easy.append(word)
                        else:
                            continue
                    else:
                        continue
                difficult.append(word)
                new.append(word)

        for word in difficult:
            if word.lower() not in easy:
                easy.append(word)
                difficult.remove(word)
        self.easy_words = len(easy)
        self.difficult_words = len(difficult)
        return easy, difficult

    def run_calculation(self):
        percentage = self.difficult_words / self.word_count * 100
        self.score = (0.0496 * self.asl) + (0.1579 * percentage) + 3.6365
        return self.score
    
    def calculate(self):
        results = {}
        results['stats'] = {}
        results['data'] = {}

        results['data']['sentences'] = self.get_sentence_count()
        results['stats']['sentence_count'] = self.sentence_count
        results['stats']['word_count'] = self.get_word_count()
        results['stats']['average_sentence_length'] = self.get_average_sentence_length()
        results['data']['easy_words'], results['data']['difficult_words'] = self.get_easy_words()
        results['stats']['easy_words'] = self.easy_words
        results['stats']['difficult_words'] = self.difficult_words
        results['stats']['raw_score'] = self.run_calculation()
        return results

def create_arguments():
    """Create an argument parser that will parse arguments passed to the CLI."""
    parser = argparse.ArgumentParser()
    parser.description = "Calculate an approximate Dale-Chall readability score."
    parser.add_argument("-i", "--input", help="The input file to read from.")
    parser.add_argument("-e", "--export-data", nargs="*", default=False, help="Whether to export the data properties to a JSON file.")
    return parser

# Start main execution here if run directly.
if __name__ == "__main__":

    # Get the arguments passed from the command line.
    args = create_arguments().parse_args(sys.argv[1:])

    # Exit out of the program if we didn't pass in an input file.
    if not args.input:
        print("No input detected. Aborting.")
        sys.exit()

    # Create our calculator.
    calc = DaleChallCalculator()

    # Copy the text input from the file we defined as the input.
    with open(args.input, 'r') as text:
        calc.text = ''.join(text.readlines())
    
    result = calc.calculate()

    # Make the JSON data file if requested.
    if args.export_data:
        with open('result.json', 'w+') as out:
            out.writelines(json.dumps(result, indent=4, ensure_ascii=False))

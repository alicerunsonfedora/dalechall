#!/usr/bin/env python
#
# Dale-Chall Approximate Calculator
# (C) 2020 Marquis Kurt.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#

import os
import json
import argparse
import sys
from string import ascii_letters, digits, ascii_uppercase
from functools import reduce

def get_corpus():
    """Import the list of easy words defined by Dale-Chall in the corpus.json
    file."""
    with open(os.getcwd() + '/data/corpus.json', 'r') as corpus_file:
        return json.load(corpus_file)

def get_scrabble():
    """Import the Scrabble Tournament Word List (TWL06) and turn it into a list
    of words, lowercased."""
    with open(os.getcwd() + "/data/scrabble.json", 'r') as scrabble_file:
        json_data = json.load(scrabble_file)
        return list(map(lambda e: e.lower(), json_data))

class DaleChallCalculator(object):
    """The primary class responsible for calculating the readability score of
    a given text."""

    def __init__(self):
        self.text = ""
        self.word_count = 0
        self.sentence_count = 0
        self.difficult_words = 0
        self.easy_words = 0
        self.words = []
        self.sentences = []
        self.score = 0
        self.asl = 0
        self.corpus = get_corpus()
        self.scrabble_words = get_scrabble()
        self.percentage = 0

    def get_average_sentence_length(self):
        """Get the average sentence length by dividing the word count
        but the sentence count."""

        # If this wasn't calculated already, calculate it now.
        if self.sentence_count == 0 and self.word_count == 0:
            self.get_sentence_count()
            self.get_word_count()

        # Store the ASL in our class
        self.asl = self.word_count / self.sentence_count
        return self.asl

    def get_word_count(self):
        """Get the count of words."""
        words = []
        texts = list(self.text)
        current_character = ""
        current_word = ""

        # Create an acceptable list of characters for a word.
        acceptable = ascii_letters + digits + "'" + "-"

        # Iterate through every character and create the word manually.
        while len(texts) > 0:
            # Grab the current character.
            current_character = texts.pop(0)

            # If the character is an unacceptable character, treat it as the
            # end of the word and push this word onto the list.
            if current_character not in acceptable:
                words.append(current_word)
                current_word = ""
            else:
                # Otherwise, just add the letter to the word.
                current_word += current_character

        # Remove all empty strings.
        while "" in words:
            words.remove("")

        while "-" in words:
            words.remove("-")

        # Store the words to this class.
        self.words = words

        # Store the count as the length of the list.
        self.word_count = len(words)
        return self.word_count

    def get_sentence_count(self):
        characters = list(self.text)
        current_character = ""
        current_sentence = ""
        possible_sentence_end = False
        sentences = []
        honorifics = ["Dr.", "Esq.", "Hon.", "Jr.", "Mr.", "Mrs.", "Ms.",
                      "Messrs.", "Mmes.", "Msgr.", "Prof.", "Rev.", "Rt.",
                      "Hon.", "Sr.", "St."]

        # Iterate through all of the characters and construct the sentence manually.
        while len(characters) > 0:

            # Grab the current character.
            current_character = characters.pop(0)

            # If we think we've reached a sentence end, check if the sentence isn't ending
            # on an honorific (titles). If we are, just keep going. Otherwise, push the
            # sentence onto the list of sentences.
            if possible_sentence_end:
                if current_character == " ":
                    split_sentence = current_sentence.split(" ")
                    last_word = split_sentence[-1:][0]

                    if last_word in honorifics:
                        current_sentence += current_character
                    else:
                        sentences.append(current_sentence)
                        current_sentence = ""

                    possible_sentence_end = False

            # If we find punctionation that typically ends sentences, mark that we might be
            # at the end of a sentence.
            elif current_character in "!?.":
                possible_sentence_end = True
                current_sentence += current_character

            else:

                # Skip this character if it's a newline character.
                if current_character == "\n":
                    continue

                # Skip this character if we have empty strings for both the sentence
                # and character. This prevents adding spaces to the beginning of sentences.
                elif current_sentence == "" and current_character == " ":
                    continue

                # Add the character to the current sentence.
                current_sentence += current_character

        # If we were at the possible end of the sentence when we arrived on the last character
        # of the text, push what the sentence was as a sentence.
        if possible_sentence_end:
            sentences.append(current_sentence)

        # Store the sentences and sentence count to this class.
        self.sentence_count = len(sentences)
        self.sentences = sentences
        return sentences

    def is_easy_word(self, word):
        """Determine whether a word is considered 'easy'."""
        possible_endings = ["s", "ies", "ing", "n", "ed", "ied", "ly", "er", "ier", "est", "iest"]
        print(word)

        # Grab all of the first words of a sentence.
        word_matrix = list(map(lambda a: a.split(" "), self.sentences))
        first_words = list(map(lambda a: a[0], word_matrix))

        # Is the word in the Dale Chall familiar words list?
        if word.lower() in self.corpus:
            return True

        # Is the word actually a number?
        elif word.isdigit():
            return True

        # Is there a hyphen in the word?
        elif "-" in word:

            # Break up the word and see if its components are also easy words.
            split_word = word.lower().split("-")
            return reduce(lambda a, b: a and b, map(self.is_easy_word, split_word))

        # Is the first letter a capital letter?
        elif word[0] in ascii_uppercase:
            lower_word = word.lower()

            if lower_word in first_words:
                return lower_word not in self.scrabble_words
            else:
                return lower_word not in self.scrabble_words

        # Does the word have any of the applicable endings?
        else:
            for ending in possible_endings:

                # Check if the word, without its ending, is in the familiar list.
                if word.endswith(ending):
                    return word[:(-1*len(ending))] in self.corpus

        # If all else fails, return that the word isn't easy.
        return False

    def get_easy_words(self):
        """Determine which words are easy and which words are difficult."""
        easy = [word for word in self.words if self.is_easy_word(word)]
        difficult = [word for word in self.words if not self.is_easy_word(word)]

        processed_words = []

        # Check over the difficult words and see if any have repeated before.
        for word in difficult:

            # If this word is already not in the easy list, check if this word repeats multiple
            # times.
            if word not in easy and word not in processed_words:

                # Get all instances of this word.
                all_word_instances = [w for w in self.words if w.lower() == word.lower()]

                # If there is more than one occurrence of this word, add all but one of the instances
                # of this word to the easy list.
                if len(all_word_instances) > 1:
                    add_to_easy = all_word_instances[1:]
                    easy += all_word_instances

                    print(add_to_easy)
                    for w in add_to_easy:
                        difficult.remove(w)

                    # Finally, add back the first instance of this word.
                    difficult.append(all_word_instances[0])
                    if all_word_instances[0] in easy:
                        easy.remove(all_word_instances[0])

                    processed_words.append(word)

        # Store the word count into the class.
        self.easy_words = len(easy)
        self.difficult_words = len(difficult)

        return easy, difficult

    def run_calculation(self):
        """Based off of the word counts, calculate the Dale Chall score."""
        self.percentage = (float(self.difficult_words) / float(self.word_count)) * 100
        self.score = (0.0496 * self.asl) + (0.1579 * self.percentage) + 3.6365
        return self.score

    def calculate(self):
        """Create a dictionary and start writing test results, performing the
        necessary calculations."""
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
        results['stats']['difficult_word_percentage'] = self.percentage
        return results

def create_arguments():
    """Create an argument parser that will parse arguments passed to the CLI."""
    parser = argparse.ArgumentParser()
    parser.description = "Calculate an approximate Dale-Chall readability score."
    parser.add_argument("-i", "--input", help="The input file to read from.")
    parser.add_argument("-e", "--export-data", nargs="*", default="result", help="The path to the JSON file containing the results.")
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

    # Print our test results.
    print("Here is a summary of your text sample:\n")
    print("Total sentence count: %s" % (result["stats"]["sentence_count"]))
    print("Total word count: %s" % (result["stats"]["word_count"]))
    print("Total difficult word count: %s" % (result["stats"]["difficult_words"]))
    print("Raw score: %s" % (result["stats"]["raw_score"]))
    print("\nTo figure out the grade level, refer to the grade chart.")
    print("Note: Results may not be accurate. To get a better understanding of the calculations,\
        \nrun this tool again with --export-data.")

    # Make the JSON data file if requested.
    if args.export_data:
        with open(args.export_data[0], 'w+') as out:
            out.writelines(json.dumps(result, indent=4, ensure_ascii=False))

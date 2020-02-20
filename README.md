# Dale.py

[![MPL](https://img.shields.io/github/license/alicerunsonfedora/dalechall)](LICENSE.txt)

A quick, dirty implementation of the Dale Chall readability test for Python 2 and Python 3. This test uses data from the Dale Chall Familiar words list and the Scrabble Tournament words list to determine the difficulty of a word.

## Requirements

- Python 2.7 or [Python 3](https://www.python.org/downloads/) (most macOS and Linux computers come with Python preinstalled, but Python 3 is recommended)

## Usage

First, download this archive or clone the repository from GitHub:

```
git clone https://github.com/alicerunsonfedora/dalechall
```

In the Terminal, run `dale.py` from the folder with the following arguments:

- `-i`/`--input`: (Required) The text file containing the sample you want to analyze.

Optionally, if you want to have all of the statistics and data in a separate file:

- `-e`/`--export-data`: The path to where you want the script to export the statistical data/words to as a JSON file.

## Credits

This project is licensed under the Mozilla Public License v2.0. Details can be found in LICENSE.txt.

The following materials were used to make this calculator possible:

- The Dale Chall familiar words list can be found here: https://natomasunified.org/als/content/uploads/sites/13/2013/10/High-Frequency-Words.pdf
- The Scrabble Tournament list used can be found here: https://scrabutility.com/TWL06.txt

The example text file is an excerpt from Mozilla's magazine titled "With Great Tech Comes Great Responsibility" ([PDF](https://foundation.mozilla.org/documents/58/Mozilla_Zine.pdf) | [Web](https://foundation.mozilla.org/en/initiatives/great-tech-great-responsibility/)).
# Footnote_Term_Project
This project was created by Brandon Hall, Teresa Hoang, Dalton Minger, Gautam Naidu, Brandon Philips, and Chelsey Randolph

The Objectives of the Footnote Project
- A program that will read the text and for each unfamiliar word (provided by the user) find its definition and generate a footnote, inserting it into the book. 
- An index into your document of the words/phrases that have footnotes.
  - Word with page number(s) the word appears on 
- A new table of contents listing the chapter names of the document.

Language/Libraries Used for Our Implementation
Language: 
  - Python 3
External Libraries: 
  - NLTK
    - RegexpTokenizer
    - Wordnet
  - CSV
  - JSON
  - UrlLib.Request
  
Book: 
  - Flatlands by Edwin A. Abbott (http://www.geom.uiuc.edu/~banchoff/Flatland/)

5 Central Methods
- Build_table(Sections, Page_numbers)
- Build_index(Index_words)
- Build_footer(Footer_words)
- Define_word(Word)
- Output_annotated_file(Str_list)

flatland.txt = Flatland Book
source_code_FINAL.py = My additions to Brandon's code
unfamiliar_terms.csv = terms we used for our footnotes



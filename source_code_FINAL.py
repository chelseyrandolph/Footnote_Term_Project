 #!/usr/bin/env python3
 
import nltk, csv
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import wordnet

import json
import urllib.request

API_KEY = '047a2c8b-b944-406e-8dc7-4ea44b447d2d'

def define_word(word):
    with urllib.request.urlopen("https://www.dictionaryapi.com/api/v3/references/collegiate/json/{}?key={}".format(word, API_KEY)) as request:
        print("Retrieving definition of '{0}'...".format(word))
        res = json.loads(request.read())
        if type(res) == list and len(res) >= 1 and 'shortdef' in res[0]:
            return ' '.join(res[0]['shortdef'])
        else:
            try:
                result = wordnet.synsets(word)[0].definition()
                return result
            except:
                return ''

def output_annotated_file(str_list):
    with open('201-annotated.txt', 'w') as file:
        file.write(''.join(str_list))

def build_footer(footer_words):
    footer = "\n\n===---------------------------------------------------------------===\n"
    for word in footer_words:
        word_def = define_word(word)
        if word_def is None:
            print("The standard Merriam-Webster Dictionary does not have a definition for: \"" + word + "\"")
        else:
            footer += word + " - " + word_def + "\n"
    footer += "===---------------------------------------------------------------===\n\n\n\n\n"
    return footer

def str_append(character, number):
    new_str = []
    i = 0
    while i < number:
        new_str.append(character)
        i += 1
    return ''.join(new_str)

def build_table(sections, page_numbers):
    table = "\n\n\n\nTABLE OF CONTENTS\n\n"
    for section in sections:
        page_number = page_numbers[sections.index(section)]
        if("PART" in section):
            line = section
            table += line + "\n"
        else:
            dots = str_append('.', 95-len(section))
            line = section + " " + dots + " " + str(page_number)
            table += line + "\n"
    return table + '\n\n'

def build_index(index_words):
    i = 0
    index = "INDEX\n\n"
    for word in index_words[0]:
        word_line = word + ": " + str(index_words[1][i]) + "\n"
        index += word_line
        i += 1
    return index + "\n\n\n\n"

if __name__ == '__main__':
    try:
        flatland_text = open("201.txt", "r").read()
    except:
        print('Could not find the file \'201.txt\' (The file name for Flatland).\nPlease make sure it is in the current directory and try again')
        quit()

    gutenberg_header_tokenizer = RegexpTokenizer(r'\A.+?\*{3}[\w\d\s]*?START[\w\d\s]*?\*{3}') # This tokenizer pulls out just the Project Gutenberg file header for safekeeping
    gutenberg_license_tokenizer = RegexpTokenizer(r'End of the Project Gutenberg.+\Z') # This tokenizer pulls out just the Project Gutenberg license for safekeeping
    forward_information_tokenizer = RegexpTokenizer(r'\A.+?22\..+?(?=PART\s+I)') # This tokenizer pulls out just the forward information including table of contents
    flatland_sections_tokenizer = RegexpTokenizer(r'((?:PART\s+I{1,2}:.+?Section\s+\d+\.\s+.+?|.+?)(?=PART\s+I{1,2}:.+?Section\s+\d+\.\s+.+|Section\s+\d+\.\s+.+|\Z))') # This tokenizer splits the sections into their own strings

    gutenberg_header = gutenberg_header_tokenizer.tokenize(flatland_text)[0]
    gutenberg_license = gutenberg_license_tokenizer.tokenize(flatland_text)[0]

    flatland_text = flatland_text[len(gutenberg_header):-len(gutenberg_license)] # Strips the header and license from the text to make footnote processing easier

    forward_information = forward_information_tokenizer.tokenize(flatland_text)[0]

    flatland_text = flatland_text[len(forward_information):] # Strips the table of contents and forward information from the text to make footnote processing easier

    forward_information = forward_information[:forward_information.index('CONTENTS:')] # Trim out the old table of contents since we we'll be replacing it

    #accounting for all the beginning lines in the header and forward information
    gutenberg_header_lines = gutenberg_header.splitlines()
    forward_information_lines = forward_information.splitlines()

    line_number = len(gutenberg_header_lines) + len(forward_information_lines) + 31 #track line numbers (31 is the length of the table of contents)

    sections = flatland_sections_tokenizer.tokenize(flatland_text)

    unfamiliar_terms_set = set()

    with open("unfamiliar_terms.csv") as unfamilar_terms_data:
        unfamiliar_terms_rows = csv.reader(unfamilar_terms_data, delimiter=',')
        for row in unfamiliar_terms_rows:
            unfamiliar_terms_set.add(row[0].lower())

    unfamiliar_terms_list = list(unfamiliar_terms_set)

    words, rows = len(unfamiliar_terms_list), 2
    index_words = [[0 for x in range(words)] for y in range(rows)] 
    index_words[0] = sorted(unfamiliar_terms_list)

    section_headers = []
    line_numbers = []
    sectionNum = 0 

    for section in sections:
        section_lines = section.splitlines()
        footer_words = []
        if("PART" in section.splitlines()[0]):
            section_headers.append(section.splitlines()[0])
            section_headers.append(section.splitlines()[9])
        else:
            section_headers.append(section.splitlines()[0])
        for line in section_lines:
            line_number += 1 
            for i in range(0, len(section_headers)):
                if line == section_headers[i]:
                    line_numbers.append(line_number)
            line_words = nltk.word_tokenize(line)
            for word in line_words:
                word_ignore_case = word.lower()
                if word_ignore_case in unfamiliar_terms_list:
                    footer_words.append(word_ignore_case)
                    unfamiliar_terms_list.remove(word_ignore_case) #Avoiding repeated footer definitions
                if word_ignore_case in index_words[0]: 
                    word_list_index = index_words[0].index(word_ignore_case)
                    if index_words[1][word_list_index] == 0: #first time word has been found
                        index_words[1][word_list_index] = str(line_number)
                    else: #word has be found before, append index to existing line numbers
                        index_words[1][word_list_index] += ", " + str(line_number)
        if len(footer_words) > 0:
            footer = build_footer(footer_words)
            footer_lines = footer.splitlines()
            line_number += len(footer_lines)
            sections[sectionNum] = section + footer

        sectionNum += 1

    #building table of contents
    table_of_contents = build_table(section_headers, line_numbers)

    #building index
    index = build_index(index_words)

    output_annotated_file([gutenberg_header, forward_information, table_of_contents, ''.join(sections), index, gutenberg_license])



def convert_dictionary(el_dictionary):
    dictionary = {}

    for i in el_dictionary[1:]:
        str = i.split(" - ")
        english_word = str[0]

        latin_words = str[1].split(", ")
        for char in latin_words:
            dictionary[char] = dictionary.get(char, "") + english_word + ", "
    result = [len(dictionary.keys())]

    for char in dictionary.keys():
        result.append((char, dictionary[char].rstrip(', ')))

    return result

"""Create a function called word_split() which takes in a string **phrase** and a set **list_of_words**.
The function will then determine if it is possible to split the string in a way in which words can be made from
the list of words.
You can assume the phrase will only contain words found in the list if it is completely splittable."""


def word_split(phrase, arr, output=None):
    if not output:
        output = []

    # If the phrase is empty, we have successfully split the words
    if not phrase:
        return output

    for word in arr:
        if phrase.startswith(word):
            output.append(word)

            return word_split(phrase[len(word):], arr, output)

    return output


print(word_split('themanran', ['the', 'ran', 'man']))

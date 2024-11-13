import os

"""
A class that contains a bunch of static methods for general text utility purposes in the automedia project.
"""


class TextUtils:
    """
    Constructor
    """
    def __init__(self):
        pass

    @staticmethod
    def write_txt(path, input_string: str):
        with open(path, 'w') as file:
            file.write(input_string)

    @staticmethod
    def read_txt(path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"File at path does not exist: {path}")

        with open(path, 'r') as file:
            file_contents = file.read()
        return file_contents

    @staticmethod
    def split_single_words(input_string):
        return input_string.split(' ')

    @staticmethod
    def cut_words(input_string, char_capacity, split_around=' '):
        """
        Cuts down the number of characters in the input string to the closest word below the specified char capacity.
        :param input_string: The string input to cut down on
        :param char_capacity: An int that is more than the number of characters of the first word in the input_string.
        :param split_around: Optional variable to input a specific character to split around. Default is a space char.
        :return:
        """
        counted_characters = 0

        all_split_words = input_string.split(split_around)
        result = all_split_words[0]

        # If the first word happens to go over the character capacity, return an empty string.
        if len(result) > char_capacity:
            return ""

        # Add to counted characters
        counted_characters = counted_characters + len(result)

        # Iterate and add up the words.
        for word in all_split_words[1:]:
            counted_characters = counted_characters + len(word) + 1  # +1 for the space character
            if counted_characters > char_capacity:
                break  # exit out loop, you've cut enough
            else:
                result = f"{result}{split_around}{word}"

        return result

    @staticmethod
    def split_partition_sentences(input_string, char_capacity):
        """
        Partitions an input string into sections and stores the sections in an ordered list.
        Critical for dividing up text to speech data.
        :param input_string:
        :param char_capacity:
        :return: an array of characters that is split into the char_capacity
        """
        counted_characters = 0
        output_split_sentences = []

        sentences = input_string.split('. ')
        partition = ""

        for sentence in sentences:
            counted_characters = counted_characters + len(sentence) + 2  # 2 for the additional period and space.

            if counted_characters > char_capacity:
                output_split_sentences.append(f"{partition}.")
                partition = f"{sentence}. "
                counted_characters = len(partition) + 2
            else:
                partition = f"{partition}. {sentence}"

        try:
            # Cut the period and space character in the first entry.
            output_split_sentences[0] = output_split_sentences[0][2:]
        except IndexError:
            # Special case when you actually don't need to split the strings. Just return as a list with one entry
            if not output_split_sentences:
                output_split_sentences.append(input_string)

        return output_split_sentences

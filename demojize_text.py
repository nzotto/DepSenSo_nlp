"""
    Nicola Zotto

    Convert emojis to text using the emoji library
"""

import emoji

## :) = :smile:
def demojize(text):
    """
    Convert all emojis in the passed string in text format (i.e. :emoji:)
    :param text: string to be demojized
    :return: demojized string
    """
    if text is not None:
        try:
            demoemojized_text = emoji.demojize(text)
        except Exception as e:
            print(e)
            return False
        return demoemojized_text

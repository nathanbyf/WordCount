__author__ = "codesse"
from functools import reduce
from itertools import islice, permutations


class HighScoringWords:
    MAX_LEADERBOARD_LENGTH = (
        100  # the maximum number of items that can appear in the leaderboard
    )
    MIN_WORD_LENGTH = 3  # words must be at least this many characters long
    letter_values = {}
    valid_words = []
    leaderboard = {}

    def __init__(self, validwords="wordlist.txt", lettervalues="letterValues.txt"):
        """
        Initialise the class with complete set of valid words and letter values by parsing text files containing the data
        :param validwords: a text file containing the complete set of valid words, one word per line
        :param lettervalues: a text file containing the score for each letter in the format letter:score one per line
        :return:
        """
        with open(validwords) as f:
            self.valid_words = f.read().splitlines()

        with open(lettervalues) as f:
            for line in f:
                (key, val) = line.split(":")
                self.letter_values[str(key).strip().lower()] = int(val)

    def rank_scores(self, temp_scores):
        """
        Ranks the top MAX_LEADERBOAD_LENGTH words from the stored scores.
        :return: The list of top MAX_LEADERBOAD_LENGTH words.
        """
        scores_ranked = dict(
            sorted(temp_scores.items(), key=lambda item: item[1], reverse=True)
        )

        top_scores = dict(islice(scores_ranked.items(), self.MAX_LEADERBOARD_LENGTH))

        return top_scores

    def build_leaderboard_for_word_list(self, **kwargs):
        """
        Build a leaderboard of the top scoring MAX_LEADERBOAD_LENGTH words from the complete set of valid words.
        :return: The list of top words.
        """

        if kwargs.get("words"):
            word_list = kwargs["words"]
        else:
            word_list = self.valid_words

        temp_scores = {}
        for word in word_list:
            scores = [self.letter_values[letter] for letter in word]

            total_score = reduce(lambda a, b: a + b, scores)

            temp_scores[word] = total_score

        self.leaderboard = self.rank_scores(temp_scores)

        top_words = list(self.leaderboard.keys())

        return top_words

    def build_leaderboard_for_letters(self, starting_letters):
        """
        Build a leaderboard of the top scoring MAX_LEADERBOARD_LENGTH words that can be built using only the letters contained in the starting_letters String.
        The number of occurrences of a letter in the startingLetters String IS significant. If the starting letters are bulx, the word "bull" is NOT valid.
        There is only one l in the starting string but bull contains two l characters.
        Words are ordered in the leaderboard by their score (with the highest score first) and then alphabetically for words which have the same score.
        :param starting_letters: a random string of letters from which to build words that are valid against the contents of the wordlist.txt file
        :return: The list of top buildable words.
        """

        combs = permutations(starting_letters)

        possible_words = ["".join(comb) for comb in combs]

        leaderboard_input = [
            word for word in possible_words if word in self.valid_words
        ]

        return self.build_leaderboard_for_word_list(words=leaderboard_input)


def start_game():
    """
    Starts both leaderboard games to rank the words in the given file, and then rank words produced from the rearrangement of a given anagram.
    :return: The list of top words from the given file, the list of top words formed from the anagram.
    """
    game = HighScoringWords()

    top_words = game.build_leaderboard_for_word_list()

    leaderboard_for_word = game.build_leaderboard_for_letters("cinema")

    return top_words, leaderboard_for_word


start_game()

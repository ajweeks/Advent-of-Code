
f = open("day_04_input.txt")
fileStr = f.read()

phrases = fileStr.splitlines()

part_2 = True


def is_anagram(word1, word2):
    if len(word1) == len(word2):
        w1 = sorted(word1)
        w2 = sorted(word2)
        for i in range(len(w1)):
            if w1[i] != w2[i]:
                return False
        return True
    return False


def valid_phrase_count():
    valid_phrases = 0
    for i in range(len(phrases)):
        words = phrases[i].split()
        valid = True
        for j in range(len(words)):
            for k in range(len(words)):
                if j != k:
                    if words[j] == words[k] or (is_anagram(words[j], words[k]) if part_2 else False):
                        valid = False

        if valid:
            valid_phrases += 1

    return valid_phrases


print(valid_phrase_count())


# Whoops, wrote this before reading the problem, keep it around for another day
# def is_palindrome(word):
#     for i in range(int(len(word) / 2)):
#         if word[i] != word[len(word) - i - 1]:
#             return False
#     return True

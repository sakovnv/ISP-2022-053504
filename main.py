import re


def input_nums():
    k = input("Input k ")
    n = input("Input n ")
    if k == "":
        k = 10
    if n == "":
        n = 4
    k = int(k)
    n = int(n)
    return [k, n]


def input_string():
    string = input("Input string: ")
    string = re.sub('[,.!?\n]', '', string)
    return string


def get_words_list(string: str):
    words = string.split()
    return words


def get_words_amount(words: list):
    words_count = {}
    for item in words:
        if words_count.__contains__(item):
            continue
        words_count[item] = words.count(item)
    return words_count


def get_average_words_amount(words: list, words_count: dict):
    return len(words) / len(words_count)


def get_median_words_amount(words_amount: dict):
    words = words_amount.values()
    words = list(words)
    if len(words) % 2 == 0:
        med = (words[int(len(words) / 2 - 1)] + words[int(len(words) / 2)]) / 2
    else:
        med = words[len(words) // 2]
    return med


def get_ngrams(words: list, string: str, n: int):
    n_gram = {}
    for item in words:
        for i in range(len(item)):
            if i + n > len(item):
                break
            if not n_gram.__contains__(item[i:i + n]):
                n_gram[item[i: i + n]] = string.count(item[i:i + n])
    return n_gram


def show_top_ngrams(n_gram: dict, k: int):
    n_gram = sorted(n_gram, key=n_gram.get)
    n_gram.reverse()
    for i in range(k if len(n_gram) > k else len(n_gram)):
        print(n_gram[i])


def main():
    k, n = input_nums()
    string = input_string()

    words = get_words_list(string)
    words_amount = get_words_amount(words)

    print("Words amount: " + str(words_amount))
    average_words_amount = get_average_words_amount(words, words_amount)

    print("Average words amount: " + str(average_words_amount))
    median_words_amount = get_median_words_amount(words_amount)

    print("Median words amount: " + str(median_words_amount))
    n_grams = get_ngrams(words, string, n)
    show_top_ngrams(n_grams, k)


if __name__ == '__main__':
    main()

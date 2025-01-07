def generate_passwords(info_list, password_length, string_cutoff_length):
    words_cut = get_words_cut(info_list, string_cutoff_length)
    print(len(words_cut))
    words_cut_possibilities = get_words_cut_possibilities(words_cut, password_length)
    password_list = combine_words_cut(words_cut_possibilities, password_length)
    print(len(password_list))

    return password_list



def get_words_cut(info_list, string_cutoff_length):
    words_cut = []

    for info in info_list:
        for i in range(0, len(info), string_cutoff_length):
            if i + string_cutoff_length > len(info) - 1:
                words_cut.append(info[i:])
            else:
                words_cut.append(info[i:i + string_cutoff_length])

    return words_cut


def get_words_cut_possibilities(words_cut, password_length):
    possibilities = []
    for i in range(len(words_cut)):
        possibilities.append(get_shifted_list(words_cut, i))
    return possibilities


def get_shifted_list(words_cut, i):
    shifted_list = []
    for j in range(i, len(words_cut)):
        shifted_list.append(words_cut[j])
    for j in range(0, i):
        shifted_list.append(words_cut[j])
    return shifted_list


def combine_words_cut(words_cut_possibilities, password_length):
    password_list = []
    password = ""

    for words_cut in words_cut_possibilities:
        for word_cut in words_cut:
            password += word_cut
            if len(password) >= password_length:
                password_list.append(password)
                password = ""

    return password_list


# Example usage
info_list = ["Philipe", "Barakat", "26042002", "April", "Chico"]
password_length = 14
string_cutoff_length = 2
passwords = generate_passwords(info_list, password_length, string_cutoff_length)
print(passwords)

def generate_passwords(info_list, password_length, string_cutoff_length):
    from itertools import combinations
    passwords = []

    # Generate all possible combinations of the info_list
    for combo in combinations(info_list, 2):
        combined_info = ''.join(combo)

        # Cut off the string if it is longer than the cutoff length
        if len(combined_info) > string_cutoff_length:
            combined_info = combined_info[:string_cutoff_length]

        # Generate passwords by appending characters until the desired length is reached
        while len(combined_info) < password_length:
            combined_info += combined_info[:password_length - len(combined_info)]

        passwords.append(combined_info[:password_length])

    return passwords

# Example usage
info_list = ["example", "password", "test"]
password_length = 10
string_cutoff_length = 2
passwords = generate_passwords(info_list, password_length, string_cutoff_length)
print(passwords)
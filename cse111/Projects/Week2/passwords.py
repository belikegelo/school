
# Enhanced features:
# - I did comments in every function to be more organized
# - try and except are used to handle missing files safely.
# - Case-sensitive and insensitive for checking .txt



LOWER = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
         "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

UPPER = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
         "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

SPECIAL = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_",
           "=", "+", "[", "]", "{", "}", "|", ";", ":", "'", "\"", ",",
           ".", "<", ">", "?", "/", "\\", "`", "~"]

def word_in_file(word, filename, case_sensitive=False):
    """
    Return True if the word is found in the file. Then if
    case_sensitive is False, compare using lowercase.
    """
    try:
        target = word if case_sensitive else word.lower()

        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                # blank line
                if line == "":
                    continue

                if not case_sensitive:
                    line = line.lower()

                if line == target:
                    return True

        return False

    except FileNotFoundError:
        return False


def word_has_character(word, character_list):
    """
    Return True if the word contains at least one character
    from the character_list.
    """
    for character in word:
        if character in character_list:
            return True

    return False

def word_complexity(word):
    """
    Return a complexity score from 0 to 4.
    1 point for lowercase, uppercase, digits, and special characters.
    """
    complexity = 0

    if word_has_character(word, LOWER):
        complexity += 1

    if word_has_character(word, UPPER):
        complexity += 1

    if word_has_character(word, DIGITS):
        complexity += 1

    if word_has_character(word, SPECIAL):
        complexity += 1

    return complexity


def password_strength(password, min_length=10, strong_length=16):
    """
    Return password strength from 0 to 5.
    """

    # Check wordlist, case insensitive
    if word_in_file(password, "wordlist.txt", case_sensitive=False):
        print("Password is a dictionary word and is not secure.")
        return 0

    # Check toppasswords, case sensitive
    if word_in_file(password, "toppasswords.txt", case_sensitive=True):
        print("Password is a commonly used password and is not secure.")
        return 0

    # Check if too short
    if len(password) < min_length:
        print("Password is too short and is not secure.")
        return 1

    # Check if long enough 
    if len(password) >= strong_length:
        print("Password is long, length trumps complexity this is a good password")
        return 5

    # Otherwise, score based on character complexity
    complexity = word_complexity(password)
    return 1 + complexity

def main():
    while True:
        password = input("Enter a password to test (q to quit): ")

        if password == "q" or password == "Q":
            break

        strength = password_strength(password)
        print(f"Password strength: {strength}")


if __name__ == "__main__":
    main()
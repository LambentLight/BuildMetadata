YES = ["true", "yes", "y", "si", "s", "1"]
NO = ["false", "no", "n", "0"]
GTAV = ["gtav", "gta", "v"]
RDR2 = ["rdr2", "rdr", "2", "red"]
COMMON = ["common", "shared", "both", "none", "s"]
GAMES = [GTAV[0], RDR2[0], COMMON[0]]


def ensure_input(message, default=None):
    """
    Asks the user to input something until he actually does it.
    """
    # Save the user input somewhere
    user_input = ""

    # While the user input is not empty
    while not user_input:
        # Ask the user to input the text
        new_input = input(message)
        # And save it trimmed
        user_input = new_input.strip()

        # If user_input is empty and there is a default value, return it
        if not user_input and default is not None:
            return str(default)

    # Finally, return the input of the user
    return user_input


def parse_game(source):
    """
    Chooses between Grand Theft Auto V and Red Dead Redemption 2.
    """
    if source.lower() in GTAV:
        return "gtav"
    elif source.lower() in RDR2:
        return "rdr2"
    elif source.lower() in COMMON:
        return "common"
    else:
        return "gtav"


def parse_bool(source, default=False):
    """
    Parses a string as a bool by using common words.
    """
    if source.lower() in YES:
        return True
    elif source.lower() in NO:
        return False
    else:
        return default


def parse_int(string, default):
    """
    Parses the string as a int by using a default value if is not possible.
    """
    # If the string is not numeric
    if not string.isnumeric():
        return default
    # Otherwise, return the string as int
    else:
        return int(string)

import os
from colorama import Fore, Back, Style

def log_message(text, log_level, text_color, text_back, letter_color, letter_back, text_case, letter_case):
    if os.name == "nt":
        from colorama import init
        init()

    letter_reg = {
        "upper": log_level.upper(),
        "lower": log_level.lower(),
        "capitalize": log_level.capitalize(),
        "title": log_level.title(),
    }
    text_reg = {
        "upper": text.upper(),
        "lower": text.lower(),
        "capitalize": text.capitalize(),
        "title": text.title(),
    }
    
    color_fore = {
        "black": Fore.BLACK,
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "light-red": Fore.RED + Style.BRIGHT,
        "light-green": Fore.GREEN + Style.BRIGHT,
        "light-yellow": Fore.YELLOW + Style.BRIGHT,
        "light-blue": Fore.BLUE + Style.BRIGHT,
        "light-magenta": Fore.MAGENTA + Style.BRIGHT,
        "light-cyan": Fore.CYAN + Style.BRIGHT,
        "dim-red": Fore.RED + Style.DIM,
        "dim-green": Fore.GREEN + Style.DIM,
        "dim-yellow": Fore.YELLOW + Style.DIM,
        "dim-blue": Fore.BLUE + Style.DIM,
        "dim-magenta": Fore.MAGENTA + Style.DIM,
        "dim-cyan": Fore.CYAN + Style.DIM,
        "white": Fore.WHITE,
    }
    color_back = {
        "black": Back.BLACK,
        "red": Back.RED,
        "green": Back.GREEN,
        "yellow": Back.YELLOW,
        "blue": Back.BLUE,
        "magenta": Back.MAGENTA,
        "cyan": Back.CYAN,
        "light-red": Back.RED + Style.BRIGHT,
        "light-green": Back.GREEN + Style.BRIGHT,
        "light-yellow": Back.YELLOW + Style.BRIGHT,
        "light-blue": Back.BLUE + Style.BRIGHT,
        "light-magenta": Back.MAGENTA + Style.BRIGHT,
        "light-cyan": Back.CYAN + Style.BRIGHT,
        "dim-red": Back.RED + Style.DIM,
        "dim-green": Back.GREEN + Style.DIM,
        "dim-yellow": Back.YELLOW + Style.DIM,
        "dim-blue": Back.BLUE + Style.DIM,
        "dim-magenta": Back.MAGENTA + Style.DIM,
        "dim-cyan": Back.CYAN + Style.DIM,
        "white": Back.WHITE,
    }

    letter_output = letter_reg.get(letter_case, log_level)
    text_output = text_reg.get(text_case, text)

    letter_output = f"[{color_fore.get(letter_color, '')}{color_back.get(letter_back, '')}{letter_output}{Style.RESET_ALL}] "
    text_output = f"{color_fore.get(text_color, '')}{color_back.get(text_back, '')}{text_output}{Style.RESET_ALL}"

    output = letter_output + text_output + Style.RESET_ALL

    return output

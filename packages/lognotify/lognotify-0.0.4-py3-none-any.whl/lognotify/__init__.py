from .log_message import log_message

# 0_o

def info(*, text, text_color=None, text_back=None,letter_color="cyan", letter_back=None, text_case=None, letter_case="upper"):
    return log_message(text, "Info", text_color, text_back, letter_color, letter_back, text_case, letter_case)

def note(*, text, text_color=None, text_back=None,letter_color="light-cyan", letter_back=None, text_case=None, letter_case="upper"):
    return log_message(text, "Note", text_color, text_back, letter_color, letter_back, text_case, letter_case)

def warning(*, text, text_color=None, text_back=None, letter_color="yellow", letter_back=None, text_case=None, letter_case="upper"):
    return log_message(text, "Warning", text_color, text_back, letter_color, letter_back, text_case, letter_case)

def error(*, text, text_color=None, text_back=None, letter_color="light-red", letter_back=None, text_case=None, letter_case="upper"):
    return log_message(text, "Error", text_color, text_back, letter_color, letter_back, text_case, letter_case)

def debug(*, text, text_color=None, text_back=None, letter_color="green", letter_back=None, text_case=None, letter_case="upper"):
    return log_message(text, "Debug", text_color, text_back, letter_color, letter_back, text_case, letter_case)

def critical(*, text, text_color=None, text_back=None, letter_color="red", letter_back=None, text_case=None, letter_case="upper"):
    return log_message(text, "Critical", text_color, text_back, letter_color, letter_back, text_case, letter_case)


def custom(*, text, text_color=None, text_back=None, log_level, letter_color, letter_back=None, text_case=None, letter_case="upper"):
    return log_message(text, log_level, text_color, text_back, letter_color, letter_back, text_case, letter_case)
import os


def msg_wrapper(msg, symbol="="):
    try:
        cols, _ = os.get_terminal_size()
    except OSError:
        cols = 80  # Default width if terminal size is unavailable
    symbol_nums = max((cols - (len(msg) + 2)) // 2, 0)
    return symbol * symbol_nums + f" {msg} " + symbol * symbol_nums
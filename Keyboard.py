import shutil
import re

terminal_width, _ = shutil.get_terminal_size()

class Keyboard():
    # key codes
    # 0 - unused
    # 1 - not in string
    # 2 - in string, wrong position
    # 3 - in string, right position
    def __init__(self):
        self.keyboard_rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
        self.letter_dict = {char: 0 for row in self.keyboard_rows for char in row}

    def print_keyboard(self):
        for row in self.keyboard_rows:
            formatted_row = []
            for char in row:
                if self.letter_dict[char] == 0:
                    formatted_row.append(f"\033[0;37m{char}\033[0m")  # White
                elif self.letter_dict[char] == 1:
                    formatted_row.append(f"\033[0;90m{char}\033[0m")  # Dark grey
                elif self.letter_dict[char] == 2:
                    formatted_row.append(f"\033[0;33m{char}\033[0m")  # Orange
                elif self.letter_dict[char] == 3:
                    formatted_row.append(f"\033[0;32m{char}\033[0m")  # Green

            formatted_row = " ".join(formatted_row)
            visible_char_count = len(re.sub(r'\033\[[0-9;]+m', '', formatted_row))
            padding = (terminal_width - visible_char_count) // 2
            print(" " * padding + formatted_row)


import requests
from os import system, name
from Keyboard import Keyboard
import shutil
import re


terminal_width, _ = shutil.get_terminal_size()

class GameBoard():
    def __init__(self):
        self.keyboard = Keyboard()
        self.word = requests.get("https://random-word-api.vercel.app/api?words=1&length=5").text.split('"')[1]
        self.user_input = ""
        self.prev_guess_padding = ["_ _ _ _ _"]*6
        self.prev_guess = []
        self.guess_count = 0

    def print_keyboard(self):
        self.keyboard.print_keyboard()

    def center_print(self, prompt):
        print(f"\n{prompt.center(terminal_width)}")

    def get_user_input(self):
        padding = (terminal_width - 8) // 2
        input_prompt = f"\n{' ' * padding}> "
        user_input = input(input_prompt).strip().lower()
        if user_input == "quit":
            exit()
        if len(user_input) == 5 and user_input.isalpha():
            if user_input in self.prev_guess:
                self.center_print("You've already guessed that!")
            else:
                if self.validate_user_input():
                    self.guess_count += 1
                    self.user_input = user_input
                    self.prev_guess.append(user_input)
                    self.prev_guess_padding.pop()
        else:
            self.center_print("Please enter a valid 5-letter word.")

    def validate_user_input(self):
        return not "Your search did not return any results." in requests.get(f"http://wordnetweb.princeton.edu/perl/webwn?s={self.user_input}").text

    def check_user_input(self):
        for index, char in enumerate(self.user_input):
            if char in self.word:
                if self.keyboard.letter_dict[char] <= 2:
                    self.keyboard.letter_dict[char] = 2
            else:
                self.keyboard.letter_dict[char] = 1
            if char == self.word[index]:
                self.keyboard.letter_dict[char] = 3
        if self.user_input == self.word:
            return True

    def display_previous_guesses(self):
        print()
        for guess in self.prev_guess:
            formatted_guess = []
            for char in guess:
                if self.keyboard.letter_dict[char] == 0:
                    formatted_guess.append(f"\033[0;37m{char}\033[0m")  # White
                elif self.keyboard.letter_dict[char] == 1:
                    formatted_guess.append(f"\033[0;90m{char}\033[0m")  # Dark grey
                elif self.keyboard.letter_dict[char] == 2:
                    formatted_guess.append(f"\033[0;33m{char}\033[0m")  # Orange
                elif self.keyboard.letter_dict[char] == 3:
                    formatted_guess.append(f"\033[0;32m{char}\033[0m")  # Green
            formatted_guess = " ".join(formatted_guess)
            visible_char_count = len(re.sub(r'\033\[[0-9;]+m', '', formatted_guess))
            padding = (terminal_width - visible_char_count) // 2
            print(" " * padding + formatted_guess)
        for guess_padding in self.prev_guess_padding:
            print(guess_padding.center(terminal_width))
        print()

    def clear_screen(self):
        system("cls") if name == "nt" else system('clear')

    def lose_screen(self):
        self.clear_screen()
        self.display_previous_guesses()
        self.print_keyboard()
        self.center_print("You lost! Better luck next time!")

    def win_screen(self):
        self.clear_screen()
        self.display_previous_guesses()
        self.print_keyboard()
        self.center_print("You won!")
